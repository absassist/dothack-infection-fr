"""Extraction / reinsertion des mails de DESKTOP.PRG (avec deplacement du texte en fin de fichier)."""
import sys,struct,json,re; sys.path.insert(0,'tools'); sys.path.insert(0,'.')
import relocs, fontpatch as fp
from elf import v2o, b as ELF
B=0x400800
SJ={b'\x83\xa2':'%0',b'\x83\xa9':'%1',b'\x83\xb0':'%2',b'\x83\xb6':'%3',b'\x83\xa6':'%4',b'\x81\x9b':'%5',b'\x81\xa2':'%6',b'\x81\xa0':'%7',b'\x81\x7e':'%8',b'\x81\x65':'%D'}
def dec(raw):
    out='';i=0
    while i<len(raw):
        c=raw[i]
        if c>=0x80 or c<0x20:
            out+=SJ.get(raw[i:i+2],'<%02x%02x>'%(raw[i],raw[i+1] if i+1<len(raw) else 0)); i+=2
        else: out+=chr(c); i+=1
    return out
def cstr(prg,a):
    o=a-B; return prg[o:prg.index(b'\0',o)]
def records(prg):
    tg=relocs.sites('desktop.prg',prg)
    s2t={s[1]:t for t,ss in tg.items() for s in ss if s[0]=='w'}
    out=[]
    for fo in sorted(s2t):
        if fo+0x10 in s2t and fo+4 in s2t and 0x30000<=s2t[fo+0x10]-B<0x47000:
            subj,snd,a,n,body=struct.unpack_from('<5I',prg,fo)
            raw=prg[body-B:body-B+20000].split(b'\0')[:n]
            while raw and raw[-1]==b'': raw.pop()
            out.append(dict(fo=fo,subject=dec(cstr(prg,subj)),sender=dec(cstr(prg,snd)),lines=[dec(l) for l in raw]))
    return out
# ---- largeur en pixels (grande et petite police)
def widths(text,tabs,orig=False):
    data=text.encode('latin1') if orig else fp.encode(text)
    w=[0,0]; i=0
    while i<len(data):
        c=data[i]
        if c==0x23 and i+1<len(data): i+=2; continue          # #x : couleur / nom
        if c==0x25 and i+1<len(data):
            d=data[i+1]; g=(d-32) if d in (0x25,0x23) else (47+d if d<0x41 else 40+d); i+=2
        else: g=c-32; i+=1
        g=min(max(g,0),127)
        for k,(cell,tab) in enumerate(tabs): w[k]+=cell-tab[g]
    return w
def tabs():
    r=[]
    for cell,addr in ((12,0x2fb4f0),(8,0x2fb5f0)):
        o=v2o(addr); r.append((cell,struct.unpack('<128h',ELF[o:o+256])))
    return r
if __name__=='__main__':
    prg=open('DESKTOP.PRG','rb').read(); recs=records(prg)
    json.dump(recs,open('mails_en.json','w'),indent=0,ensure_ascii=False)
    T=tabs(); ws=sorted(widths(l,T,True)+[l] for r in recs for l in r['lines'] if '<' not in l)
    print(len(recs),'mails', sum(len(r['lines']) for r in recs),'lignes')
    print('largeurs max (L,S):',[w[:2] for w in sorted(ws,key=lambda x:x[0])[-6:]],[w[:2] for w in sorted(ws,key=lambda x:x[1])[-6:]])
    print('sujets max:',sorted((widths(r['subject'],T,True),r['subject']) for r in recs if '<' not in r['subject'])[-4:])
    print('lignes max par mail:',sorted(len(r['lines']) for r in recs)[-5:])
    print('non decodes:',set(re.findall(r'<....>',' '.join(l for r in recs for l in r['lines']+[r['subject'],r['sender']]))))
    for i,r in enumerate(recs[:12]):
        print('\n##',i,hex(r['fo']),r['subject'],'| de',r['sender']); print('\n'.join(r['lines']))

# ------------------------------------------------------------ reinsertion
MAXW=(408,272); MAXSUBJ=(224,159)
def wrap(text,T,MAXW=MAXW):
    out=[]
    for para in text.split('\n\n'):
        out.append('')
        for seg in para.split('\n'):
            cur=''; col=''
            for word in seg.split(' '):
                trial=(cur+' '+word) if cur else word
                w=widths(trial,T)
                if cur and (w[0]>MAXW[0] or w[1]>MAXW[1]):
                    out.append(cur)
                    cs=re.findall(r'#([WRGBY])',cur); col=('#'+cs[-1]) if cs and cs[-1]!='W' else (col if not cs else '')
                    cur=col+word
                else: cur=trial
            w=widths(cur,T); assert w[0]<=MAXW[0] and w[1]<=MAXW[1],('ligne trop large',cur)
            out.append(cur)
    return out
def insert(prg,trmods,bss=0x380,extras=()):
    """prg: bytearray du DESKTOP.PRG. Retourne le nouveau fichier (orig + bss a zero + nouveau texte)."""
    T=tabs(); recs=records(bytes(prg)); blob=bytearray(); base=B+len(prg)+bss; cache={}
    def add(bs):
        if bs in cache: return cache[bs]
        a=base+len(blob); blob.extend(bs+b'\0'); cache[bs]=a; return a
    def add_block(lines):
        a=base+len(blob); blob.extend(b'\0'.join(fp.encode(l) for l in lines)+b'\0\0')
        while len(blob)%4: blob.append(0)
        return a
    import replies, replies_fr
    RS={replies.norm(k):v for k,v in replies_fr.SUBJ.items()}
    senders={}; n=0; report=[]
    for mod in trmods:
        senders.update(getattr(mod,'SENDERS',{}))
    for i,r in enumerate(recs):
        fo=r['fo']
        if r['sender'] in senders: struct.pack_into('<I',prg,fo+4,add(fp.encode(senders[r['sender']])))
        for mod in trmods:
            if i in mod.M:
                t=dict(mod.M[i])
                if r['subject'].upper().startswith('RE:') and replies.norm(r['subject'][3:]) in RS:
                    t['subject']='RE: '+RS[replies.norm(r['subject'][3:])]
                w=widths(t['subject'],T)
                assert w[0]<=MAXSUBJ[0]+8 and w[1]<=MAXSUBJ[1]+8,('sujet trop large',t['subject'],w)
                lines=wrap(t['body'],T)
                struct.pack_into('<I',prg,fo,add(fp.encode(t['subject'])))
                a=base+len(blob); blob.extend(b'\0'.join(fp.encode(l) for l in lines)+b'\0\0')
                while len(blob)%4: blob.append(0)
                struct.pack_into('<I',prg,fo+0x10,a); struct.pack_into('<I',prg,fo+0xc,len(lines))
                n+=1; report.append((i,r['subject'],t['subject'],len(r['lines']),len(lines)))
    extra=[]; miss=replies.insert(prg,add,add_block,T,extra)
    if extras: 
        for fn in extras: fn(prg,add,add_block,T,extra)
    return bytes(prg)+bytes(bss)+bytes(blob),report,len(recs),extra,miss

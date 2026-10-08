"""Textes de l'executable : deplaces dans un segment supplementaire (0x790600), le tas est decale d'autant."""
import sys,struct,pickle,re; sys.path.insert(0,'tools'); sys.path.insert(0,'.'); sys.path.insert(0,'tr')
import relocs,mails,strs,fontpatch as fp
from elf import v2o
MB=0x100000-0x100
GCMN_EXTRA=0x730600; ELF_EXTRA=0x790600; NEW_END=0x7B0600
DW=(363,259)
def lines_for(text,T,maxlines,W=DW):
    if '\n' in text: ls=text.split('\n')
    else: ls=mails.wrap(text,T,W)[1:]
    return ls
def build(elf):
    import elf_01,elf_02,elf_03,elf_fix
    T=mails.tabs(); orig=open('SLUS_202.67','rb').read()
    X={t['a']:t for t in strs.targets('main',orig,MB,dstart=0x100,dend=0x100+0x278880)}
    blob=bytearray(); warn=[]; n=0
    XS=sorted(X); tight=[]
    def place(a,lines,fixedlens=None):
        nonlocal n
        t=X[a]; enc=[fp.encode(l) for l in lines]
        if fixedlens:
            for i,(e,L) in enumerate(zip(enc,fixedlens)):
                if len(e)>L: warn.append('champ trop long %x: %r (%d>%d)'%(a,lines[i],len(e),L))
                enc[i]=e[:L].ljust(L,b' ')
        if not fixedlens: enc=[e_+b' '*(e_.count(b'%F')+e_.count(b'%G')) for e_ in enc]
        addr=ELF_EXTRA+len(blob); blob.extend(b'\0'.join(enc)+b'\0\0\0\0')
        while len(blob)%4: blob.append(0)
        for s in t['sites']: relocs.repoint(elf,s,addr)
        n+=1
    D=dict(elf_01.D); D.update(elf_02.D); D.update(elf_fix.D); elf_03.S.update(elf_fix.S)
    for a,text in D.items():
        if a not in X: warn.append('adresse inconnue %x'%a); continue
        ls=lines_for(text,T,3)
        if len(ls)>max(3,len(X[a]['lines'])): warn.append('trop de lignes %x (%d): %s'%(a,len(ls),text))
        for l in ls:
            w=mails.widths(l,T)
            if w[0]>DW[0]+6 or w[1]>DW[1]+6: warn.append('ligne trop large %x: %s'%(a,l))
        place(a,ls)
    for a,v in elf_03.S.items():
        if a not in X: warn.append('adresse inconnue %x'%a); continue
        ol=X[a]['lines']; N=len(ol)
        if isinstance(v,str):
            # largeur visee = plus large ligne anglaise du voisinage (meme boite), sinon celle des dialogues
            i=XS.index(a); loc=max(max(mails.widths(l,T,True)[0] for l in X[k]['lines']) for k in XS[max(0,i-6):i+7])
            ls=None
            if N>1 and loc<DW[0]:
                try:
                    c=mails.wrap(v,T,(loc+3,int((loc+3)*DW[1]/DW[0])+2))[1:]
                    if len(c)<=N: ls=c
                    else: tight.append('%x %d>%d : %s'%(a,len(c),N,v))
                except Exception: pass
            elif N==1 and mails.widths(v,T)[0]>loc+3: tight.append('%x 1 ligne %d>%d : %s'%(a,mails.widths(v,T)[0],loc,v))
            if ls is None: ls=mails.wrap(v,T,DW)[1:]
            if len(ls)>N: warn.append('trop de lignes %x (%d>%d): %s'%(a,len(ls),N,v))
            ls=ls+['']*(N-len(ls))
        else:
            ls=list(v)
            if len(ls)!=N: warn.append('nb de lignes %x: %d au lieu de %d %r'%(a,len(ls),N,ol)); continue
        lens=[len(l.encode('latin1','replace')) for l in ol]
        fixed=lens if (len(set(lens))==1 and N>1 and any(l.endswith(' ') for l in ol)) else None
        place(a,ls,fixed)
    for a,fields in elf_03.F.items():
        t=X[a]; ol=t['lines'][0]; assert len(t['lines'])==1 and len(ol)==16*len(fields),(hex(a),ol,len(ol))
        out=b''
        for f in fields:
            e=fp.encode(f)
            if len(e)>15: warn.append('champ >15 %x: %s'%(a,f))
            out+=e[:16].ljust(16,b' ')
        addr=ELF_EXTRA+len(blob); blob.extend(out+b'\0\0\0\0')
        for s in t['sites']: relocs.repoint(elf,s,addr)
        n+=1
    assert len(blob)<=NEW_END-ELF_EXTRA,len(blob)
    # tas decale : _end 0x730600 -> NEW_END
    for va in (0x10006c,0x100398):
        o=v2o(va); w,=struct.unpack_from('<I',elf,o); assert w&0xffff==0x73,(hex(va),hex(w))
        struct.pack_into('<I',elf,o,(w&0xffff0000)|(NEW_END>>16))
    o=v2o(0x2f77d4); assert struct.unpack_from('<I',elf,o)[0]==0x730600; struct.pack_into('<I',elf,o,NEW_END)
    # segment supplementaire (en-tete de programme n.5)
    phoff,=struct.unpack_from('<I',elf,0x1c); p=phoff+5*32
    assert struct.unpack_from('<8I',elf,p)[2]==0x730600
    while len(elf)%16: elf.append(0)
    struct.pack_into('<8I',elf,p,1,len(elf),ELF_EXTRA,ELF_EXTRA,len(blob),len(blob),6,0x10)
    elf.extend(blob)
    print('ELF: %d textes deplaces, segment de %d octets'%(n,len(blob)))
    for w in warn: print('  !',w)
    print('  serres:',len(tight))
    for w in tight: print('  ~',w)
    return elf

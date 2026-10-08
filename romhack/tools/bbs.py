"""Forum (TOPPAGE.PRG) : messages {ptr titre, ptr auteur, nb lignes+1, ptr corps, x}."""
import sys,struct,json,re; sys.path.insert(0,'tools'); sys.path.insert(0,'.'); sys.path.insert(0,'tr')
import relocs,mails,fontpatch as fp
B=0x400800
def records(prg):
    tg=relocs.sites('toppage.prg',prg); s2t={s[1]:t for t,ss in tg.items() for s in ss if s[0]=='w'}
    out=[]
    for fo in sorted(s2t):
        if fo-12 in s2t and fo-8 in s2t:
            n,x=struct.unpack_from('<I',prg,fo-4)[0],struct.unpack_from('<I',prg,fo+4)[0]
            if not 0<n<200: continue
            body=s2t[fo]; raw=prg[body-B:body-B+8000].split(b'\0')[:n]
            while raw and raw[-1]==b'': raw.pop()
            out.append(dict(fo=fo,title=mails.dec(mails.cstr(prg,s2t[fo-12])),author=mails.dec(mails.cstr(prg,s2t[fo-8])),lines=[mails.dec(l) for l in raw],n=n,x=x))
    return out
if __name__=='__main__':
    prg=open('TOPPAGE.PRG','rb').read(); recs=records(prg)
    json.dump(recs,open('bbs_en.json','w'),ensure_ascii=False,indent=0)
    T=mails.tabs()
    ws=sorted(mails.widths(l,T,True)+[l] for r in recs for l in r['lines'])
    print(len(recs),'messages',sum(len(r['lines']) for r in recs),'lignes ; largeurs max',[w[:2] for w in ws[-4:]],max(w[1] for w in ws))
    print('titres max',sorted(mails.widths(r['title'],T,True) for r in recs)[-3:], 'max lignes',max(r['n'] for r in recs))
    if len(sys.argv)<3: sys.exit()
    a,b=int(sys.argv[1]),int(sys.argv[2])
    for i in range(a,min(b,len(recs))):
        r=recs[i]; out=[]; cur=''; prev=''
        for l in r['lines']:
            if l=='': out.append(cur); cur=''; continue
            if cur and (len(prev)<30 or l.startswith('>') or l.startswith('#B%')): cur+=' | '+l
            else: cur=(cur+' '+l) if cur else l
            prev=l
        out.append(cur)
        print('@%d [%s] %s'%(i,r['author'],r['title'])); print('\n'.join(out))

def build(prg):
    """prg: bytes de TOPPAGE.PRG original -> nouveau fichier"""
    import bbs_01,bbs_02,strs
    prg=bytearray(prg); T=mails.tabs(); recs=records(bytes(prg)); base=B+len(prg); blob=bytearray(); cache={}
    TT=dict(bbs_01.T); TT.update(bbs_02.T); BB=dict(bbs_01.B); BB.update(bbs_02.B)
    ws=sorted(mails.widths(l,T,True) for r in recs[1:342] for l in r['lines'] if not l.startswith('___'))
    MAXW=(max(w[0] for w in ws),max(w[1] for w in ws))
    def add(bs):
        if bs in cache: return cache[bs]
        a=base+len(blob); blob.extend(bs+b'\0'); cache[bs]=a; return a
    def add_block(lines):
        a=base+len(blob); blob.extend(b'\0'.join(fp.encode(l) for l in lines)+b'\0\0')
        while len(blob)%4: blob.append(0)
        return a
    n=0; miss=[]
    for i,r in enumerate(recs[:342]):
        if i==0: continue
        fo=r['fo']; t=r['title']; pre=''
        while t.startswith('RE:'): pre+='RE: '; t=t[3:].lstrip()
        ft=TT.get(t)
        if ft is None or i not in BB: miss.append((i,r['title'])); continue
        if r['author']=='Deleted': struct.pack_into('<I',prg,fo-8,add(fp.encode('Supprimé')))
        lines=mails.wrap(BB[i],T,MAXW)[1:]
        struct.pack_into('<I',prg,fo-12,add(fp.encode(pre+ft)))
        struct.pack_into('<I',prg,fo,add_block(lines)); struct.pack_into('<I',prg,fo-4,len(lines)+1); n+=1
    th=0
    for t in strs.targets('toppage.prg',bytes(prg)):
        if len(t['lines'])==1 and (t['lines'][0] in bbs_02.TH or t['lines'][0] in TT):
            a=add(fp.encode(bbs_02.TH.get(t['lines'][0]) or TT[t['lines'][0]]))
            for s in t['sites']: relocs.repoint(prg,s,a)
            th+=1
    print('forum: %d messages traduits, %d titres de fils/libelles, manquants %s, largeur max %s'%(n,th,miss,MAXW))
    return bytes(prg)+bytes(blob)

"""Audit de debordement : largeur FR vs largeur EN au meme endroit et dans le voisinage (meme table = meme boite probable)."""
import sys,struct,pickle; sys.path.insert(0,'tools'); sys.path.insert(0,'.')
import strs,mails,fontpatch as fp
from elf import v2o
T=mails.tabs(); B=0x400800; MB=0x100000-0x100
INV=None
def decfr(b):
    return b.decode('latin1')
def wfr(b):
    # largeur d'une ligne deja encodee (glyphes remplaces) : meme table que l'anglais apres patch
    return mails.widths(b.decode('latin1'),T,True)[0]
def rd(buf,site):
    if site[0]=='w': return struct.unpack_from('<I',buf,site[1])[0]
    hw,=struct.unpack_from('<I',buf,site[1]); lw,=struct.unpack_from('<I',buf,site[2]); lo=lw&0xffff
    return ((hw&0xffff)<<16)+(lo-0x10000 if lo&0x8000 else lo)
def elf_off(buf):
    phoff,=struct.unpack_from('<I',buf,0x1c); n,=struct.unpack_from('<H',buf,0x2c); segs=[]
    for i in range(n):
        t,off,va,pa,fs,ms=struct.unpack_from('<6I',buf,phoff+i*32)
        if t==1: segs.append((va,off,fs))
    def f(a):
        for va,off,fs in segs:
            if va<=a<va+fs: return off+a-va
    return f
def run(name,orig,new,targets,a2o_old,a2o_new):
    rows=[]
    for t in targets:
        na=rd(new,t['sites'][0]); N=len(t['lines'])
        o=a2o_new(na)
        if o is None: continue
        ls=[]; p=o
        for _ in range(N):
            e=new.index(b'\0',p); ls.append(bytes(new[p:e])); p=e+1
        en=[mails.widths(l,T,True)[0] for l in t['lines']]
        try: fr=[wfr(l) for l in ls]
        except Exception: continue
        rows.append(dict(a=t['a'],en=t['lines'],fr=[l.decode('latin1') for l in ls],wen=max(en),wfr=max(fr),same=(na==t['a'] and [l.encode('latin1','replace') for l in t['lines']]==ls)))
    rows.sort(key=lambda r:r['a']); out=[]
    for i,r in enumerate(rows):
        if r['same']: continue
        loc=max(x['wen'] for x in rows[max(0,i-10):i+11])
        r['loc']=loc
        if r['wfr']>r['wen']: out.append(r)
    return rows,out
res={}
o=open('SLUS_202.67','rb').read(); n=open('out/SLUS_202.67','rb').read(); f=elf_off(n)
res['ELF']=run('ELF',o,n,strs.targets('main',o,MB,dstart=0x100,dend=0x100+0x278880),None,f)
for nm in ('DESKTOP','TOPPAGE','GCMN','DEMO'):
    o=open(nm+'.PRG','rb').read(); n=open('out/'+nm+'.PRG','rb').read()
    res[nm]=run(nm,o,n,strs.targets(nm.lower()+'.prg',o),None,lambda a,n=n:(a-B) if 0<=a-B<len(n) else None)
pickle.dump(res,open('audit.pkl','wb'))
for k,(rows,out) in res.items():
    ch=[r for r in rows if not r['same']]
    print(k,len(rows),'textes,',len(ch),'modifies,',len(out),'plus larges que leur anglais,',sum(1 for r in out if r['wfr']>r['loc']),'plus larges que tout le voisinage')

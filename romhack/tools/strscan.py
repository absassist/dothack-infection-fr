"""Parcourt une archive gzip (STREAM/*.BIN) dans l'ISO : index des membres + chaines de texte lisibles."""
import os,sys,re,zlib,json,time,struct
iso=os.path.expanduser('~/mnt/roms/Dot Hack Part 1 - Infection (USA).iso')
name,lba,size=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
st='strscan_%s.json'%name
S=json.load(open(st)) if os.path.exists(st) else {'pos':0,'ents':[],'txt':[]}
f=open(iso,'rb'); t=time.time()
W=re.compile(rb"[A-Za-z#%][\x20-\x7e]{5,}")
EN=re.compile(rb"[A-Za-z][a-z]{2,} [a-z]{2,} [a-zA-Z]{2,}")
while S['pos']<size and time.time()-t<140:
    pos=S['pos']; f.seek(lba*2048+pos); buf=f.read(min(48<<20,size-pos))
    if buf[:3]!=b'\x1f\x8b\x08': S['pos']=pos+2048; continue
    fl=buf[3]; p=10; nm=''
    if fl&8: e=buf.index(b'\0',p); nm=buf[p:e].decode('latin1')
    z=zlib.decompressobj(31)
    try: out=z.decompress(buf)
    except Exception as ex: print('ERR',pos,nm,ex); S['pos']=pos+2048; continue
    clen=len(buf)-len(z.unused_data)
    hits=[(m.start(),m.group().decode('latin1')) for m in W.finditer(out) if b' ' in m.group() and EN.search(m.group())]
    S['ents'].append((pos,clen,len(out),nm,out[:8].hex(),len(hits)))
    if hits: S['txt'].append((nm,hits[:400]))
    S['pos']=(pos+clen+2047)//2048*2048
json.dump(S,open(st,'w'))
print(name,S['pos'],size,len(S['ents']),'membres',sum(1 for e in S['ents'] if e[5]),'avec texte','FINI' if S['pos']>=size else 'partiel')

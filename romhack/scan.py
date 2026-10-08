import zlib,re,collections,os,json
d=open('DATA.BIN','rb').read()
ents=[];pos=0
os.makedirs('data',exist_ok=True)
while pos<len(d):
    if d[pos:pos+3]!=b'\x1f\x8b\x08':
        # skip to next sector
        pos=(pos//2048+1)*2048 if pos%2048 else pos+2048
        continue
    fl=d[pos+3]; p=pos+10; name=''
    if fl&8:
        e=d.index(b'\0',p); name=d[p:e].decode('latin1')
    z=zlib.decompressobj(31)
    try:
        out=z.decompress(d[pos:pos+64*1024*1024])
    except Exception as ex:
        print('ERR',pos,name,ex); pos+=2048; continue
    clen=len(d[pos:pos+64*1024*1024])-len(z.unused_data)
    ents.append((pos,clen,len(out),name))
    open('data/%05d_%s'%(len(ents)-1,name.replace('/','_')),'wb').write(out)
    pos=(pos+clen+2047)//2048*2048
print(len(ents),'members; total unc',sum(e[2] for e in ents))
json.dump(ents,open('data_index.json','w'))
c=collections.Counter(os.path.splitext(e[3])[1].lower() for e in ents)
print(c)
for e in ents[:40]: print(e)

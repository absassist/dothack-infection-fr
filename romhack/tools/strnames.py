import os,sys,re,zlib,json
iso=os.path.expanduser('~/mnt/roms/Dot Hack Part 1 - Infection (USA).iso')
f=open(iso,'rb')
def member(lba,pos,clen):
    f.seek(lba*2048+pos); return zlib.decompress(f.read(clen),31)
def names(d): return set(m.decode('latin1') for m in re.findall(rb'[A-Za-z_][\x21-\x7e]{4,31}(?=\0)',d[:0x40000]))
S=json.load(open('strscan_STRCMNE.json')); E={e[3]:e for e in S['ents']}
for nm in ['str7100','str7400','str8801','str7482']:
    a=member(795358,*E[nm+'e.tmp'][:2]); b=member(795358,*E[nm+'.tmp'][:2])
    na,nb=names(a),names(b)
    print(nm,len(a),len(b),'seulement E:',sorted(na-nb)[:30],'seulement JP:',sorted(nb-na)[:30])
S=json.load(open('strscan_STR1E.json'))
print([(e[3],e[2]) for e in S['ents']])
allt=set()
for e in S['ents']:
    d=member(837295,e[0],e[1])
    for n in names(d):
        if re.search(r'txt|sub|msg|tel|moj|font|serif|jimak',n,re.I): allt.add((e[3],n))
print(sorted(allt)[:120])

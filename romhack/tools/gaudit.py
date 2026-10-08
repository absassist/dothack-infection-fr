"""Chaines de GCMN.PRG non couvertes par la traduction (ni deplacees ni remplacees sur place)."""
import sys,re,struct,bisect; sys.path[:0]=['tools','.','tr']
import gcmn
d=open('GCMN.PRG','rb').read(); B=gcmn.B
gcmn.build(d)
cov=sorted(gcmn.COV); st=[c[0] for c in cov]
hdr=struct.unpack('<8I',d[:32]); ds=hdr[3]+0x40
out=[]
for m in re.finditer(rb'[\x20-\x7e]{3,}\0',d[ds:]):
    a=B+ds+m.start(); s=m.group()[:-1].decode()
    i=bisect.bisect_right(st,a)-1
    if i>=0 and cov[i][0]<=a<cov[i][1]: continue
    if '_' in s or not re.search(r'[a-z]{3}',s) or re.search(r'\.(CCS|ccs|BIN|bin|tmp|PRG|cmp|c|h)$',s): continue
    if not re.search(r'[A-Za-z]{2,} [A-Za-z]{2,}|^[A-Z][a-z]+[.:!?]?$|^ ?[a-z]+[.:!?]? ?$',s): continue
    k=m.end()+ds
    while k<len(d) and d[k]==0: k+=1
    out.append('%x|%d|%s'%(a,k-(m.start()+ds)-1,s))
open('gaudit.txt','w').write('\n'.join(out)); print(len(out))

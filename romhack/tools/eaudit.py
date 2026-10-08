"""Chaines de l'ELF non couvertes par la traduction."""
import sys,re,bisect; sys.path[:0]=['tools','.','tr']
import strs,elfmod,elf_01,elf_02,elf_03,elf_fix
MB=elfmod.MB
orig=open('SLUS_202.67','rb').read()
X={t['a']:t for t in strs.targets('main',orig,MB,dstart=0x100,dend=0x100+0x278880)}
K=set(elf_01.D)|set(elf_02.D)|set(elf_fix.D)|set(elf_03.S)|set(elf_fix.S)|set(elf_03.F)|set(getattr(elf_03,'INPLACE_A',{}))
cov=sorted((a,a+X[a]['slot']) for a in K if a in X); st=[c[0] for c in cov]
out=[]
for m in re.finditer(rb'(?:[\x20-\x7e]|\x81[\x40-\xfc]){3,}\0',orig[0x200000-MB:0x100+0x278880]):
    a=MB+0x200000-MB+m.start(); s=m.group()[:-1].decode('latin1')
    i=bisect.bisect_right(st,a)-1
    if i>=0 and cov[i][0]<=a<cov[i][1]: continue
    if not re.search(r'[a-z]{3}',s) or re.search(r'\.(CCS|ccs|BIN|bin|tmp|PRG|prg|cmp|c|h|cpp|elf|ELF|txt|irx|IRX|str|STR|pss|PSS|vag|vb|hd|bd)\b|^[a-z0-9_]+$|%[0-9]*[dsxfc]|_[a-z]|[a-z][A-Z]{2}|/|\\|=',s): continue
    k=m.end()+0x200000-MB
    while k<len(orig) and orig[k]==0: k+=1
    out.append('%x|%d|%d|%s'%(a,k-(m.start()+0x200000-MB)-1,1 if a in X else 0,s))
open('eaudit.txt','w').write('\n'.join(out)); print(len(out))

"""Sites de reference (pointeurs) d'un PRG, d'apres les sections .rel de l'ELF."""
import struct,sys,collections
sys.path.insert(0,'.')
from elf import SECS,b as ELF
BASE=0x400800
def sites(prgname,prg,BASE=BASE):
    """retourne dict cible -> liste de sites ; site = ('w',off) ou ('hl',off_hi,off_lo)"""
    s=[x for x in SECS if x[0]=='.rel'+prgname][0]
    n=s[6]//8; ents=[struct.unpack('<II',ELF[s[5]+i*8:s[5]+i*8+8]) for i in range(n)]
    tg=collections.defaultdict(list); lasthi={}
    for off,info in ents:
        t=info&0xff; sym=info>>8; fo=off-BASE
        if fo<0 or fo+4>len(prg): continue
        w,=struct.unpack_from('<I',prg,fo)
        if t==2: tg[w].append(('w',fo))
        elif t==5: lasthi[sym]=fo; lasthi[None]=fo
        elif t==6:
            hi=lasthi.get(sym)
            if hi is None: continue
            hw,=struct.unpack_from('<I',prg,hi)
            lo=w&0xffff; lo=lo-0x10000 if lo&0x8000 else lo
            tg[((hw&0xffff)<<16)+lo].append(('hl',hi,fo))
    return tg
def repoint(prg,site,new):
    if site[0]=='w': struct.pack_into('<I',prg,site[1],new)
    else:
        _,hi,lo=site
        hw,=struct.unpack_from('<I',prg,hi); lw,=struct.unpack_from('<I',prg,lo)
        struct.pack_into('<I',prg,hi,(hw&0xffff0000)|(((new+0x8000)>>16)&0xffff))
        struct.pack_into('<I',prg,lo,(lw&0xffff0000)|(new&0xffff))

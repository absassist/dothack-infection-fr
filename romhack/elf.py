import struct
b=open('SLUS_202.67','rb').read()
shoff,=struct.unpack('<I',b[0x20:0x24]); shentsize,shnum,shstrndx=struct.unpack('<HHH',b[0x2e:0x34])
phoff,=struct.unpack('<I',b[0x1c:0x20]); phnum,=struct.unpack('<H',b[0x2c:0x2e])
secs=[]
for i in range(shnum):
    s=struct.unpack('<10I',b[shoff+i*shentsize:shoff+i*shentsize+40]); secs.append(s)
strtab=secs[shstrndx]
def nm(off,tab): 
    o=tab[4]+off; return b[o:b.index(b'\0',o)].decode('latin1')
SECS=[(nm(s[0],strtab),)+s for s in secs]
syms=[]
for s in SECS:
    if s[2]==2:
        st=secs[s[7]]
        for j in range(s[6]//16):
            n,v,sz,info,oth,shn=struct.unpack('<IIIBBH',b[s[4+1]+j*16:s[4+1]+j*16+16])
            syms.append((v,sz,info,shn,nm(n,st)))
def v2o(v):
    for s in SECS:
        if s[2]==1 and s[4] and s[4]<=v<s[4]+s[6]: return v-s[4]+s[5]
if __name__=='__main__':
    for s in SECS: print(s[0],hex(s[2]),'addr',hex(s[4]),'off',hex(s[5]),'size',hex(s[6]))
    print(len(syms),'symbols')
    import re
    for v,sz,info,shn,n in sorted(syms):
        if re.search(r'(?i)kanji|font|sjis|moji',n): print(hex(v),sz,info&15,n)
    print('biggest data objects:')
    for v,sz,info,shn,n in sorted(syms,key=lambda x:-x[1])[:25]: print(hex(v),sz,info&15,n)

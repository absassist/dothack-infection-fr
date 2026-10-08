"""Applique out/* sur une copie de l'ISO. Les fichiers agrandis sont replaces en fin d'ISO (entree de repertoire mise a jour)."""
import os,sys,struct,time
R=os.path.expanduser('~/mnt/roms/')
# ISO USA d'origine : variable d'environnement DOTHACK_ISO, sinon l'emplacement de l'auteur
SRC=os.environ.get('DOTHACK_ISO') or R+'Dot Hack Part 1 - Infection (USA).iso'
ORIG=os.path.getsize(SRC)
FILES={'SLUS_202.67':('/',b'SLUS_202.67;1'),'DEMO.PRG':('/DATA',b'DEMO.PRG;1'),'DESKTOP.PRG':('/DATA',b'DESKTOP.PRG;1'),'TOPPAGE.PRG':('/DATA',b'TOPPAGE.PRG;1'),'GCMN.PRG':('/DATA',b'GCMN.PRG;1')}
def find_rec(g,dirname,name):
    g.seek(16*2048); pvd=g.read(2048); root=pvd[156:190]
    lba,size=struct.unpack('<I',root[2:6])[0],struct.unpack('<I',root[10:14])[0]
    def scan(lba,size,want):
        g.seek(lba*2048); d=g.read(size); i=0
        while i<size:
            l=d[i]
            if l==0: i=(i//2048+1)*2048; continue
            nl=d[i+32]; nm=d[i+33:i+33+nl]
            if nm==want: return lba*2048+i,struct.unpack('<I',d[i+2:i+6])[0],struct.unpack('<I',d[i+10:i+14])[0]
            i+=l
    if dirname!='/':
        _,lba,size=scan(lba,size,dirname[1:].encode())
    return scan(lba,size,name)
def patch(dst):
    with open(dst,'r+b') as g:
        g.truncate(ORIG); end=ORIG
        for f,(dn,nm) in FILES.items():
            data=open('out/'+f,'rb').read(); pos,lba,size=find_rec(g,dn,nm)
            with open(SRC,'rb') as s:
                _,olba,osize=find_rec(s,dn,nm)
            if len(data)<=(osize+2047)//2048*2048: nlba=olba
            else: nlba=end//2048; end+=(len(data)+2047)//2048*2048
            g.seek(nlba*2048); g.write(data.ljust((len(data)+2047)//2048*2048,b'\0'))
            g.seek(pos+2); g.write(struct.pack('<I',nlba)+struct.pack('>I',nlba)+struct.pack('<I',len(data))+struct.pack('>I',len(data)))
            print(f,'LBA',olba,'->',nlba,'taille',osize,'->',len(data))
        g.seek(16*2048+80); g.write(struct.pack('<I',end//2048)+struct.pack('>I',end//2048))
        # articles de news : membres gzip de DATA/DATA.BIN (LBA 12463), reecrits a leur place
        if os.path.exists('out/news/plan.json'):
            import json
            for nm,pos,clen,nlen in json.load(open('out/news/plan.json')):
                gz=open('out/news/%s.gz'%nm,'rb').read(); assert len(gz)==nlen<=clen
                g.seek(12463*2048+pos); assert g.read(3)==b'\x1f\x8b\x08'
                g.seek(12463*2048+pos); g.write(gz.ljust(clen,b'\0'))
            print('news : articles FR ecrits dans DATA.BIN')
        # scene de l'Epitaphe : meme membre gzip dans STR1E.BIN (LBA 837295) et STR1.BIN (LBA 1052212), position 188416
        if os.path.exists('out/str0001e.gz'):
            gz=open('out/str0001e.gz','rb').read(); assert len(gz)<=844995
            for lba in (837295,1052212):
                g.seek(lba*2048+188416); assert g.read(4)==b'\x1f\x8b\x08\x08'
                g.seek(lba*2048+188416); g.write(gz.ljust(844995,b'\xff'))
            print('str0001e : texture FR ecrite dans STR1E.BIN et STR1.BIN')
        for k,pos in ((1,0),(2,94208)):
            p='out/title1_st%d.gz'%k
            if not os.path.exists(p): continue
            gz=open(p,'rb').read(); assert len(gz)<=94208
            for lba in (837295,1052212):
                g.seek(lba*2048+pos); assert g.read(4)==b'\x1f\x8b\x08\x08'
                g.seek(lba*2048+pos); g.write(gz.ljust(94208,b'\xff'))
            print('title1_st%d : menu FR ecrit dans STR1E.BIN et STR1.BIN'%k)
    # verification
    with open(dst,'rb') as g:
        for f,(dn,nm) in FILES.items():
            data=open('out/'+f,'rb').read(); pos,lba,size=find_rec(g,dn,nm); g.seek(lba*2048)
            assert size==len(data) and g.read(size)==data,f
    print('OK',dst,os.path.getsize(dst))
if __name__=='__main__':
    import shutil
    for name in sys.argv[1:]:
        p=name if os.path.dirname(name) else R+name
        if not os.path.exists(p): print('copie de l\'ISO USA ->',p); shutil.copyfile(SRC,p)
        try:
            open(p,'r+b').close(); patch(p); break
        except PermissionError: print('verrouille:',name)

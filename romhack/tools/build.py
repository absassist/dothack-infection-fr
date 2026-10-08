import sys,os,importlib,glob; sys.path.insert(0,'tools'); sys.path.insert(0,'.'); sys.path.insert(0,'tr')
import runpy
os.makedirs('out',exist_ok=True)
if not os.path.exists('mails_en.json'):   # liste des mails anglais (sert a retrouver les citations des reponses)
    import json,mails as _m; json.dump(_m.records(open('DESKTOP.PRG','rb').read()),open('mails_en.json','w'),indent=0,ensure_ascii=False)
runpy.run_path('tools/build_poc.py')          # police + ecran d'inscription -> out/
import mails
mods=[importlib.import_module(os.path.basename(f)[:-3]) for f in sorted(glob.glob('tr/mails_*.py'))]
prg=bytearray(open('out/DESKTOP.PRG','rb').read())
import desk_rest
new,rep,total,extra,miss=mails.insert(prg,mods,extras=desk_rest.EXTRAS)
open('out/DESKTOP.PRG','wb').write(new)
print('mails traduits: %d / %d ; DESKTOP.PRG %d -> %d octets'%(len(rep),total,len(prg),len(new)))
print('\n'.join(extra)); print('reponses manquantes:',miss)

import bbs
new=bbs.build(open('TOPPAGE.PRG','rb').read()); open('out/TOPPAGE.PRG','wb').write(new); print('TOPPAGE.PRG ->',len(new))

import elfmod
e=elfmod.build(bytearray(open('out/SLUS_202.67','rb').read())); open('out/SLUS_202.67','wb').write(e)

import gcmn
g=gcmn.build(open('GCMN.PRG','rb').read()); open('out/GCMN.PRG','wb').write(g); print('GCMN.PRG ->',len(g))

# 1re cinematique : texture de l'Epitaphe redessinee (scene str0001e, presente dans STR1.BIN et STR1E.BIN)
import epitaph,zlib,struct
OLD=844995; raw=open('str0001e.gz.orig','rb').read(); assert len(raw)==OLD
hdr=raw[:raw.index(b'\0',10)+1]; ccs,wmax=epitaph.build(zlib.decompress(raw,31))
c=zlib.compressobj(9,zlib.DEFLATED,-15,9); body=c.compress(ccs)+c.flush()
gz=hdr+body+struct.pack('<II',zlib.crc32(ccs)&0xffffffff,len(ccs)); assert len(gz)<=OLD and zlib.decompress(gz,31)==ccs
open('out/str0001e.gz','wb').write(gz)
e=bytearray(open('out/SLUS_202.67','rb').read())
for o in (0x20c28c,0x20fe0c):
    assert struct.unpack_from('<I',e,o)[0]==OLD,hex(o); struct.pack_into('<I',e,o,len(gz))
open('out/SLUS_202.67','wb').write(e)
print('Epitaphe: texture FR, %d -> %d octets compresses (largeur max %d px)'%(OLD,len(gz),wmax))

# articles de news : 17 textures redessinees (DATA.BIN), taille compressee mise a jour dans la table de l'ELF
import news,json,glob
IDX=json.load(open('data_index.json')); e=bytearray(open('out/SLUS_202.67','rb').read()); os.makedirs('out/news',exist_ok=True); plan=[]
databin=open('DATA.BIN','rb')
for n in sorted(news.A):
    nm='xddn_%s.cmp'%n; i=[k for k,x in enumerate(IDX) if x[3]==nm][0]; pos,clen,ulen,_=IDX[i]; slot=IDX[i+1][0]-pos
    databin.seek(pos); raw=databin.read(clen); hdr=raw[:raw.index(b'\0',10)+1]; old=zlib.decompress(raw,31)
    ccs=news.render(old,n)[0]; c=zlib.compressobj(9,zlib.DEFLATED,-15,9); body=c.compress(ccs)+c.flush()
    gz=hdr+body+struct.pack('<II',zlib.crc32(ccs)&0xffffffff,len(ccs)); assert len(gz)<=clen and zlib.decompress(gz,31)==ccs,nm
    key=('XDDN_%s.CCS'%n).encode(); hits=[]; q=e.find(key)
    while q>=0:
        if struct.unpack_from('<II',e,q+0x24)==(clen,ulen): hits.append(q)
        q=e.find(key,q+1)
    assert len(hits)==1,(nm,hits); struct.pack_into('<I',e,hits[0]+0x24,len(gz))
    open('out/news/%s.gz'%nm,'wb').write(gz); plan.append((nm,pos,clen,len(gz)))
json.dump(plan,open('out/news/plan.json','w')); open('out/SLUS_202.67','wb').write(e)
print('News: %d articles redessines, %d -> %d octets compresses'%(len(plan),sum(x[2] for x in plan),sum(x[3] for x in plan)))

# menu de l'ecran-titre : textures de title1..4.cmp (DATA.BIN)
import titlemenu
for k in (1,):  # title2..4 = autres volumes, inutilises ici (et ne rentrent pas dans leur emplacement)
    nm='title%d.cmp'%k; i=[j for j,x in enumerate(IDX) if x[3]==nm][0]; pos,clen,ulen,_=IDX[i]; slot=IDX[i+1][0]-pos
    databin.seek(pos); raw=databin.read(clen); hdr=raw[:raw.index(b'\0',10)+1]; old=zlib.decompress(raw,31)
    ccs,nt=titlemenu.patch(old); c=zlib.compressobj(9,zlib.DEFLATED,-15,9); body=c.compress(ccs)+c.flush()
    gz=hdr+body+struct.pack('<II',zlib.crc32(ccs)&0xffffffff,len(ccs)); assert len(gz)<=slot and zlib.decompress(gz,31)==ccs,(nm,len(gz),slot)
    key=('TITLE%d.CCS'%k).encode(); hits=[]; q=e.find(key)
    while q>=0:
        if struct.unpack_from('<II',e,q+0x24)==(clen,ulen): hits.append(q)
        q=e.find(key,q+1)
    assert len(hits)==1,(nm,hits); struct.pack_into('<I',e,hits[0]+0x24,len(gz))
    open('out/news/%s.gz'%nm,'wb').write(gz); plan.append((nm,pos,max(clen,len(gz)),len(gz))); print(' ',nm,nt,'textures',clen,'->',len(gz),'emplacement',slot)
json.dump(plan,open('out/news/plan.json','w')); open('out/SLUS_202.67','wb').write(e)

# ecran d'accueil de The World : textures de xdttopen0.cmp (DATA.BIN)
import toppage
nm='xdttopen0.cmp'; i=[j for j,x in enumerate(IDX) if x[3]==nm][0]; pos,clen,ulen,_=IDX[i]; slot=IDX[i+1][0]-pos
databin.seek(pos); raw=databin.read(clen); hdr=raw[:raw.index(b'\0',10)+1]; old=zlib.decompress(raw,31)
ccs=toppage.patch(old); c=zlib.compressobj(9,zlib.DEFLATED,-15,9); body=c.compress(ccs)+c.flush()
gz=hdr+body+struct.pack('<II',zlib.crc32(ccs)&0xffffffff,len(ccs)); assert len(gz)<=slot and zlib.decompress(gz,31)==ccs,(nm,len(gz),slot)
key=b'XDTTOPEN0.CCS'; hits=[]; q=e.find(key)
while q>=0:
    if struct.unpack_from('<II',e,q+0x24)==(clen,ulen): hits.append(q)
    q=e.find(key,q+1)
assert len(hits)==1,(nm,hits); struct.pack_into('<I',e,hits[0]+0x24,len(gz))
open('out/news/%s.gz'%nm,'wb').write(gz); plan.append((nm,pos,max(clen,len(gz)),len(gz))); print(' ',nm,clen,'->',len(gz),'emplacement',slot)
json.dump(plan,open('out/news/plan.json','w')); open('out/SLUS_202.67','wb').write(e)

# animation de l'ecran-titre (title1_st1/st2 dans STR1E.BIN et STR1.BIN) : memes textures de menu que title1.cmp
import titlemenu
iso_us=os.environ.get('DOTHACK_ISO') or os.path.expanduser('~/mnt/roms/Dot Hack Part 1 - Infection (USA).iso')
e=bytearray(open('out/SLUS_202.67','rb').read())
with open(iso_us,'rb') as f:
    for k,(pos,offs) in enumerate(((0,(0x20c08c,0x20fd8c)),(94208,(0x20c0cc,0x20fdcc)))):
        f.seek(837295*2048+pos); raw=f.read(92849)
        hdr=raw[:raw.index(b'\0',10)+1]; ccs,nt=titlemenu.patch(zlib.decompress(raw,31))
        c=zlib.compressobj(9,zlib.DEFLATED,-15,9); body=c.compress(ccs)+c.flush()
        gz=hdr+body+struct.pack('<II',zlib.crc32(ccs)&0xffffffff,len(ccs)); assert len(gz)<=94208 and zlib.decompress(gz,31)==ccs
        open('out/title1_st%d.gz'%(k+1),'wb').write(gz)
        for o in offs:
            assert struct.unpack_from('<I',e,o)[0]==92849,hex(o); struct.pack_into('<I',e,o,len(gz))
        print('  title1_st%d : %d textures, 92849 -> %d octets'%(k+1,nt,len(gz)))
open('out/SLUS_202.67','wb').write(e)

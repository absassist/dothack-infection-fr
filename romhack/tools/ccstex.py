"""Textures d'un fichier CCS : lecture/ecriture (8bpp et 4bpp, palette RGBA alpha 0..0x80)."""
import struct,re
from PIL import Image
def index(d):
    p=8+struct.unpack_from('<I',d,4)[0]*4; nf,no=struct.unpack_from('<II',d,p+8); q=p+16+nf*32
    return [d[q+i*32:q+i*32+30].split(b'\0')[0].decode('latin1') for i in range(no)]
def chunks(d,kind):
    out={}
    for m in re.finditer(rb'\x00'+bytes([kind>>8])+rb'\xcc\xcc',d):
        p=m.start()
        if p%4: continue
        out[struct.unpack_from('<I',d,p+8)[0]]=p
    return out
def tex(d,name):
    ob=index(d); T=chunks(d,0x300); C=chunks(d,0x400); i=ob.index(name); p=T[i]
    clt=struct.unpack_from('<I',d,p+12)[0]; typ=d[p+21]; lw,lh=d[p+24],d[p+25]; w,h=1<<lw,1<<lh
    n=struct.unpack_from('<I',d,p+32)[0]*4; data=d[p+36:p+36+n]
    c=C[clt]; nc=struct.unpack_from('<I',d,c+24)[0]; pal=[tuple(d[c+28+4*k:c+32+4*k]) for k in range(nc)]
    return dict(p=p,off=p+36,n=n,w=w,h=h,typ=typ,data=data,pal=pal,clt=c)
def image(t):
    w,h=t['w'],t['h']; im=Image.new('RGBA',(w,h)); px=im.load(); d=t['data']
    for y in range(h):
        for x in range(w):
            if t['typ']==0x14:
                b=d[(y*w+x)//2]; i=(b>>4) if x&1 else (b&15)
            else: i=d[y*w+x]
            r,g,b_,a=t['pal'][i]; px[x,y]=(r,g,b_,min(255,a*2))
    return im
if __name__=='__main__':
    import sys,os
    d=open(sys.argv[1],'rb').read()
    for nm in sys.argv[2:]:
        t=tex(d,nm); print(nm,t['w'],t['h'],hex(t['typ']),hex(t['off']),t['n'],len(t['pal']),t['pal'][:6])
        im=image(t); bg=Image.new('RGBA',im.size,(40,40,60,255)); bg.alpha_composite(im)
        bg.convert('RGB').save(os.path.expanduser('~/mnt/roms/dothack-fr/img/%s.png'%nm))

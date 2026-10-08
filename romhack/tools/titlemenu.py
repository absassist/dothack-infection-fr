# -*- coding: utf-8 -*-
"""Menu de l'ecran-titre : 5 textures 128x32 (4bpp, blanc + niveaux d'alpha) redessinees en francais."""
import sys,os; sys.path.insert(0,'tools')
import ccstex
from PIL import Image,ImageDraw,ImageFont
BOLD='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
CREDIT='Traduction FR : no4bs'
LABELS={'TEX_xgtmen00':'NOUVEAU','TEX_xgtmen01':'CHARGER','TEX_xgtmen02':'OPTIONS','TEX_xgtmen03':'PARODIE','TEX_xgtmen04':'CONVERTIR'}
def glyphs(txt):
    """texte gras, resserre horizontalement (aspect proche de l'original), hauteur 21 px ; masque 128x32"""
    f=ImageFont.truetype(BOLD,112); big=Image.new('L',(2400,200),0); dr=ImageDraw.Draw(big)
    dr.text((10,10),txt,font=f,fill=255,stroke_width=5,stroke_fill=255); bb=big.getbbox(); big=big.crop(bb)
    h=21; w=int(round(big.width*h/big.height*0.60)); w=min(w,92)
    small=big.resize((w,h),Image.LANCZOS); m=Image.new('L',(128,32),0); m.paste(small,(2,6)); return m
SANS='/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
SERIF='/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'
CMP_DX=38   # la ligne ".hack TM and" (title1.cmp) est affichee ~38 texels plus a gauche que l'autre texture
def copmask(cmp_):
    """masque 256x128 : 3 lignes de 13 px dans la bande 88-127, alignees a droite sur x=243"""
    m=Image.new('L',(256,128),0); dr=ImageDraw.Draw(m)
    fs=ImageFont.truetype(SANS,12); fr=ImageFont.truetype(SERIF,12)
    def right(txt,f,y,xr=243):
        w=dr.textlength(txt,font=f); dr.text((xr-w,y),txt,font=f,fill=255); return xr-w
    c='\u00a9 2001-2002 BANDAI'
    x1=243-dr.textlength(c,font=fr)
    if cmp_:
        right('.hack TM and',fs,88,x1-4+CMP_DX); return m   # cette texture n'affiche que la 1re ligne
    right(c,fr,88)
    xp=right(c,fr,101); right('Program ',fs,101,xp)
    right(CREDIT,fs,114)
    return m
def patch(ccs):
    d=bytearray(ccs); ob=ccstex.index(ccs); n=0
    for name,txt in LABELS.items():
        if name not in ob: continue
        t=ccstex.tex(bytes(d),name); assert t['typ']==0x14 and (t['w'],t['h'])==(128,32),name
        al=[(i,c[3]) for i,c in enumerate(t['pal']) if c[:3]==(255,255,255)]
        m=glyphs(txt).transpose(Image.FLIP_TOP_BOTTOM); px=m.load(); data=bytearray(128*32//2)
        for y in range(32):
            for x in range(0,128,2):
                a0=px[x,y]*128//255; a1=px[x+1,y]*128//255
                i0=min(al,key=lambda t_:abs(t_[1]-a0))[0]; i1=min(al,key=lambda t_:abs(t_[1]-a1))[0]
                data[(y*128+x)//2]=i0|(i1<<4)
        d[t['off']:t['off']+t['n']]=data; n+=1
    if False and 'TEX_xgtcop00' in ob:   # DESACTIVE (l'ecran affiche des morceaux de l'image, pas l'image entiere) - mentions Bandai resserrees sur 3 lignes + credit de traduction (bande visible : lignes 86-127)
        t=ccstex.tex(bytes(d),'TEX_xgtcop00'); assert t['typ']==0x14 and (t['w'],t['h'])==(256,128)
        cmp_=not any(ccstex.image(t).transpose(Image.FLIP_TOP_BOTTOM).split()[3].crop((150,86,256,106)).getdata())
        m=copmask(cmp_).transpose(Image.FLIP_TOP_BOTTOM); px=m.load(); data=bytearray(d[t['off']:t['off']+t['n']])
        for y in range(128):
            if not (0<=y<=127-84): continue          # lignes 84-127 de l'image (retournee)
            for x in range(256):
                v=0 if px[x,y]>=110 else 1
                i=(y*256+x)//2; data[i]=((data[i]&0xf0)|v) if x%2==0 else ((data[i]&0x0f)|(v<<4))
        d[t['off']:t['off']+t['n']]=data; n+=1
    return bytes(d),n
if __name__=='__main__':
    import glob
    d=open(glob.glob('data/*title1.cmp')[0],'rb').read(); new,n=patch(d); print(n,'textures')
    sheet=Image.new('RGB',(128*4+20,(32*4+8)*5+8),(60,20,80))
    for k,nm in enumerate(LABELS):
        im=ccstex.image(ccstex.tex(new,nm)).transpose(Image.FLIP_TOP_BOTTOM); bg=Image.new('RGBA',im.size,(60,20,80,255)); bg.alpha_composite(im)
        sheet.paste(bg.convert('RGB').resize((512,128),Image.NEAREST),(10,8+k*136))
    sheet.save(os.path.expanduser('~/mnt/roms/dothack-fr/img/title/_menu_fr.png'))

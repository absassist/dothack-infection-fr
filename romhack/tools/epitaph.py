# -*- coding: utf-8 -*-
"""Redessine la texture TEX_xddhibn0 (texte de l'Epitaphe, 1re cinematique) en francais."""
import sys,os; sys.path.insert(0,'tools')
import ccstex
from PIL import Image,ImageDraw,ImageFont,ImageFilter
LINES=["Il n'est pas encore revenu, l'être à l'ombre",
"parti en quête du Dragon du Crépuscule.",
"Le Foyer des Ténèbres gronde,",
"et Helba, Reine des Ténèbres, a enfin levé son armée.",
"Apeiron, Roi de la Lumière, appelle...",
"Au pied de l'arc-en-ciel, ils se rejoignent.",
"Contre l'abominable « Vague », ensemble ils luttent.",
"Le lac d'Alba bouillonne,",
"le grand arbre de la Lumière s'abat.",
"Toute puissance se change en gouttes au temple d'Arche Koeln.",
"Il retourne au néant, ce monde des êtres sans ombre.",
"Jamais il ne reviendra, l'être à l'ombre",
"parti en quête du Dragon du Crépuscule."]
TITLE="« Epitaphe du Crépuscule » —— Emma Wielant"
FONT='/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf'
def render(size=19):
    W=H=512; f=ImageFont.truetype(FONT,size)
    mask=Image.new('L',(W,H),0); dr=ImageDraw.Draw(mask); wmax=0
    def put(txt,k,right=None):
        nonlocal wmax
        l,t,r,b=dr.textbbox((0,0),txt,font=f); w=r-l; wmax=max(wmax,w)
        x=(right-w) if right else (W-w)//2
        dr.text((x-l,6+32*k+3),txt,font=f,fill=255)
    for k,t in enumerate(LINES): put(t,k)
    put(TITLE,14,right=508)
    return mask,wmax
def quantize(mask,pal):
    # contour noir opaque + ombre douce, texte blanc antialiase par-dessus
    out=mask.filter(ImageFilter.MaxFilter(3)); soft=out.filter(ImageFilter.GaussianBlur(1.6))
    greys=[(i,c[0]) for i,c in enumerate(pal) if c[3]==128 and c[0]==c[1]==c[2]]
    alphas=[(i,c[3]) for i,c in enumerate(pal) if c[:3]==(0,0,0) and c[3]<128]
    W,H=mask.size; idx=bytearray(W*H); m=mask.load(); o=out.load(); s=soft.load()
    for y in range(H):
        for x in range(W):
            if m[x,y]>0 or o[x,y]>=128:
                g=m[x,y]; idx[y*W+x]=min(greys,key=lambda t:abs(t[1]-g))[0]
            else:
                a=min(128,int(s[x,y]*1.3))//2*1; a=min(127,int(s[x,y]/255*128*1.4))
                idx[y*W+x]=min(alphas,key=lambda t:abs(t[1]-a))[0]
    return idx
def build(ccs):
    d=bytearray(ccs); t=ccstex.tex(bytes(d),'TEX_xddhibn0'); assert t['typ']==0x14 and t['w']==512
    mask,wmax=render(); assert wmax<=506,wmax
    idx=quantize(mask,t['pal']); W=H=512
    data=bytearray(W*H//2)
    for y in range(H):
        sy=H-1-y                      # la texture est stockee a l'envers
        for x in range(0,W,2):
            data[(y*W+x)//2]=idx[sy*W+x]|(idx[sy*W+x+1]<<4)
    d[t['off']:t['off']+t['n']]=data
    return bytes(d),wmax
if __name__=='__main__':
    new,wmax=build(open('str0001e.ccs','rb').read()); open('str0001e_fr.ccs','wb').write(new); print('largeur max',wmax)
    t=ccstex.tex(new,'TEX_xddhibn0'); im=ccstex.image(t).transpose(Image.FLIP_TOP_BOTTOM)
    bg=Image.new('RGBA',im.size,(40,40,60,255)); bg.alpha_composite(im); bg.convert('RGB').save(os.path.expanduser('~/mnt/roms/dothack-fr/img/epitaphe_fr.png'))
    t0=ccstex.tex(open('str0001e.ccs','rb').read(),'TEX_xddhibn0'); im=ccstex.image(t0).transpose(Image.FLIP_TOP_BOTTOM)
    bg=Image.new('RGBA',im.size,(40,40,60,255)); bg.alpha_composite(im); bg.convert('RGB').save(os.path.expanduser('~/mnt/roms/dothack-fr/img/epitaphe_en.png'))

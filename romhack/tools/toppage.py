# -*- coding: utf-8 -*-
"""Ecran d'accueil de The World (xdttopen0) : phrases d'aide + boutons ENTRER / FORUM / QUITTER (3 variantes)."""
import sys,os; sys.path.insert(0,'tools')
import ccstex
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
REG='/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
BOLD='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
HELP=[(72,"Accéder à The World."),(105,"Forum avec les autres joueurs."),(169,"Retour au bureau."),(232,"Nouveau message posté.")]
WORDS=["ENTRER","FORUM","QUITTER"]
def word(txt,maxw,h=20):
    f=ImageFont.truetype(BOLD,96); big=Image.new('L',(1600,170),0); dr=ImageDraw.Draw(big)
    dr.text((10,10),txt,font=f,fill=255,stroke_width=3,stroke_fill=255); big=big.crop(big.getbbox())
    w=min(maxw,int(round(big.width*h/big.height*1.15))); return big.resize((w,h),Image.LANCZOS)
def chrome(mask,top=(150,200,235),mid=(70,120,165),bot=(35,60,110),edge=(22,32,72),alpha=255):
    """lettres bleu metal : contour sombre, degrade vertical, reflet en haut ; image RGBA"""
    w,h=mask.size; pad=3; M=Image.new('L',(w+2*pad,h+2*pad),0); M.paste(mask,(pad,pad))
    out=M.filter(ImageFilter.MaxFilter(5)); im=Image.new('RGBA',M.size,(0,0,0,0)); px=im.load(); m=M.load(); o=out.load()
    for y in range(M.size[1]):
        t=min(1,max(0,(y-pad)/max(1,h-1)))
        c=tuple(int(top[k]+(mid[k]-top[k])*t*2) if t<0.5 else int(mid[k]+(bot[k]-mid[k])*(t-0.5)*2) for k in range(3))
        for x in range(M.size[0]):
            if m[x,y]>110: px[x,y]=c+(alpha,)
            elif o[x,y]>90: px[x,y]=edge+(alpha,)
    return im
def glow(mask):
    w,h=mask.size; pad=6; M=Image.new('L',(w+2*pad,h+2*pad),0); M.paste(mask,(pad,pad))
    g=M.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(2.6)); im=Image.new('RGBA',M.size,(0,0,0,255)); px=im.load(); gp=g.load()
    for y in range(M.size[1]):
        for x in range(M.size[0]):
            v=min(255,int(gp[x,y]*1.5)); px[x,y]=(int(v*0.62),v,int(v*0.93),255)
    return im
def put(d,name,canvas,region=None):
    """ecrit canvas (RGBA, a l'endroit) dans la texture ; region=(x0,y0,x1,y1) limite la zone remplacee"""
    t=ccstex.tex(bytes(d),name); assert t['typ']==0x13; W,H=t['w'],t['h']; assert canvas.size==(W,H)
    pal=t['pal']; cache={}; cp=canvas.load(); data=bytearray(t['data'])
    def near(c):
        if c not in cache:
            a=c[3]*128//255
            cache[c]=min(range(len(pal)),key=lambda i:((pal[i][0]-c[0])**2+(pal[i][1]-c[1])**2+(pal[i][2]-c[2])**2)*(1 if a>8 else 0)+ (pal[i][3]-a)**2*6)
        return cache[c]
    x0,y0,x1,y1=region or (0,0,W,H)
    for y in range(y0,y1):
        for x in range(x0,x1): data[(H-1-y)*W+x]=near(cp[x,y])
    d[t['off']:t['off']+t['n']]=data
def cur(d,name):
    return ccstex.image(ccstex.tex(bytes(d),name)).transpose(Image.FLIP_TOP_BOTTOM)
def patch(ccs):
    d=bytearray(ccs)
    # 1) phrases d'aide (xdtcomo0) : blanc + ombre
    im=cur(d,'TEX_xdtcomo0'); f=ImageFont.truetype(REG,17)
    clear=Image.new('RGBA',(256,256-66),(0,0,0,0)); im.paste(clear,(0,66))
    for y,txt in HELP:
        assert f.getlength(txt)<=246,txt
        sh=Image.new('L',(256,256),0); ImageDraw.Draw(sh).text((6,y+2),txt,font=f,fill=255); sh=sh.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
        lay=Image.new('RGBA',(256,256),(0,0,0,0)); lay.putalpha(sh.point(lambda v:min(255,int(v*0.75)))); im=Image.alpha_composite(im,lay)
        tx=Image.new('L',(256,256),0); ImageDraw.Draw(tx).text((5,y+1),txt,font=f,fill=255)
        white=Image.new('RGBA',(256,256),(255,255,255,255)); white.putalpha(tx); im=Image.alpha_composite(im,white)
    put(d,'TEX_xdtcomo0',im,(0,66,256,256))
    # 2) boutons : version normale (moitie droite de xdtcomo1), selectionnee (xdtcomo3), lumineuse (xdtcomo2)
    c1=cur(d,'TEX_xdtcomo1'); c1.paste(Image.new('RGBA',(126,128),(0,0,0,0)),(130,0))
    c3=Image.new('RGBA',(128,128),(222,255,255,0)); c2=Image.new('RGBA',(128,128),(0,0,0,255))
    for k,(txt,y1,y3) in enumerate(zip(WORDS,(10,55,96),(10,54,96))):
        m=word(txt,112); ch=chrome(m); gl=glow(m)
        x3=(121-m.width) if k==2 else 8; c3.alpha_composite(ch,(x3-3,y3-3))
        ch1=chrome(m,(240,254,254),(135,200,205),(45,68,110),(43,67,107),202)
        x1=(249-m.width) if k==2 else 136; c1.paste(ch1,(x1-3,y1-3))
        c2.paste(ImageChops.lighter(c2.crop((x3-6,y3-6,x3-6+gl.width,y3-6+gl.height)).convert('RGB'),gl.convert('RGB')),(x3-6,y3-6))
    put(d,'TEX_xdtcomo1',c1,(130,0,256,128)); put(d,'TEX_xdtcomo3',c3); put(d,'TEX_xdtcomo2',c2.convert('RGBA'))
    return bytes(d)
if __name__=='__main__':
    import glob
    d=open(glob.glob('data/*xdttopen0.cmp')[0],'rb').read(); new=patch(d); out=os.path.expanduser('~/mnt/roms/dothack-fr/img/top/')
    sheet=Image.new('RGB',(256+256+128+128+30,270),(70,30,90)); x=5
    for nm in ('TEX_xdtcomo0','TEX_xdtcomo1','TEX_xdtcomo3','TEX_xdtcomo2'):
        im=cur(new,nm); bg=Image.new('RGBA',im.size,(70,30,90,255)); bg.alpha_composite(im); sheet.paste(bg.convert('RGB'),(x,5)); x+=im.width+6
    sheet=sheet.resize((sheet.width*2,sheet.height*2),Image.NEAREST); sheet.save(out+'_top_fr.png'); print('ok',sheet.size)

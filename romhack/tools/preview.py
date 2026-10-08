import sys,io,base64; sys.path.insert(0,'.'); sys.path.insert(0,'tools')
from elf import v2o
import fontpatch as fp
from PIL import Image
elf=bytearray(open('SLUS_202.67','rb').read()); fp.patch(elf,v2o)
def render(text,F,scale=3):
    sh=fp.Sheet(elf,v2o(F['addr']),F['gw'],F['gh']); to=v2o(F['ofs'])
    data=fp.encode(text); idxs=[]; i=0
    while i<len(data):
        if data[i]==0x25: idxs.append(40+data[i+1] if data[i+1]>=65 else 47+data[i+1]); i+=2
        else: idxs.append(data[i]-32); i+=1
    W=sum(F['gw'] for _ in idxs)+4; im=Image.new('L',(W,F['gh']),90); x=0
    pal={0:None,4:0,9:170,10:185,11:200,12:215,15:255}
    for g in idxs:
        gl=sh.get(g); o=int.from_bytes(elf[to+2*g:to+2*g+2],'little')
        for yy,row in enumerate(gl):
            for xx,v in enumerate(row):
                if v and x+xx<W: im.putpixel((x+xx,yy),pal.get(v,255))
        x+=F['gw']-o
    return im.crop((0,0,x+2,F['gh']))
lines=["Voil[ : {t{, d}s que le ch~teau fut pr]t,", "le gar|on re|ut l'{p{e o` dort l'\\le. %F %G"]
txt=["Voilà : été, dès que le château fut prêt,","le garçon reçut l'épée où dort l'île. bientôt sûr","éèàêçùâîôû  eacuio  Contrôle du prénom déjà reçu"]
ims=[render(t,F) for F in (fp.SMALL,fp.LARGE) for t in txt]
W=max(i.width for i in ims); H=sum(i.height+2 for i in ims)
out=Image.new('L',(W,H),90); y=0
for i in ims: out.paste(i,(0,y)); y+=i.height+2
out=out.quantize(8); bio=io.BytesIO(); out.save(bio,'PNG',optimize=True)
print(out.size,len(bio.getvalue())); print(base64.b64encode(bio.getvalue()).decode())

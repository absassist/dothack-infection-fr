import sys,re,os; sys.path.insert(0,'.'); sys.path.insert(0,'tools')
from elf import v2o
import fontpatch as fp
SLOTS=[(0x000,0x20),(0x020,0x20),(0x040,0x30),(0x070,0x20),(0x090,0x20),(0x0b0,0x70),(0x120,0x40),(0x160,0x30),(0x190,0x30),(0x1c0,0x40),(0x200,0x20),(0x220,0x20),(0x240,0x38)]
FR=[["Entrez votre nom de famille."],
    ["Entrez un nom d'utilisateur."],
    ["Entrez le nom de votre","personnage."],
    ["Nom de famille réinitialisé."],
    ["Paramètres par défaut rétablis"],
    ["Entrez un nom.","Retour impossible.","Ce nom de personnage est déjà","pris. Choisissez-en un autre."],
    ["Vous êtes maintenant inscrit","à \"The World\"."],
    ["Choix du nom de joueur","et du personnage."],
    ["Inscription reçue et validée."],
    ["Pour lancer le jeu, choisissez","\"The World\" sur votre bureau."],
    ["Bon séjour dans \"The World\"."],
    ["Enregistrement du prénom."],
    ["Enregistrement du nom de","personnage utilisé en jeu."]]
log=[]
def put(buf,off,size,fr,prefix=0,name=''):
    """remplace un objet texte (lignes separees par \\0) sans changer ni son debut, ni sa taille, ni son nombre de lignes"""
    old=bytes(buf[off+prefix:off+size]); lines=old.rstrip(b'\0').split(b'\0')
    assert len(lines)==len(fr),(name,hex(off),lines,fr)
    new=b'\0'.join(fp.encode(l) for l in fr)
    assert prefix+len(new)<=size-1,(name,hex(off),len(new),size)
    buf[off+prefix:off+size]=new.ljust(size-prefix,b'\0')
    log.append('%s %06x  %s  ->  %s'%(name,off,' / '.join(l.decode() for l in lines),' / '.join(fr)))
orig_blk=open('DEMO.PRG','rb').read()[0xdc00:0xdc00+0x278]
out={}
for f in ('SLUS_202.67','DEMO.PRG','DESKTOP.PRG'):
    buf=bytearray(open(f,'rb').read())
    for m in list(re.finditer(re.escape(orig_blk),bytes(buf))):
        for (o,s),fr in zip(SLOTS,FR): put(buf,m.start()+o,s,fr,name=f[:4])
    out[f]=buf
fp.patch(out['SLUS_202.67'],v2o)
# ecran de saisie du nom (DESKTOP.PRG) : variante du bloc + libelles
d=out['DESKTOP.PRG']; B=0x604d0
for o,s,fr in [(0x00,0x20,FR[0]),(0x20,0x20,FR[1]),(0x40,0x30,FR[2]),(0x70,0x20,FR[3]),(0x90,0x30,FR[4]),
               (0xc0,0x20,["Retour au champ précédent."]),(0xe0,0x70,FR[5]),
               (0x150,0x20,["Enregistrer ce nom.","Valider ?"]),(0x170,0x10,["Votre nom"]),(0x180,0x10,["Personnage"]),
               (0x190,0x40,FR[6]),(0x1d0,0x30,FR[7]),(0x200,0x30,FR[8]),(0x230,0x40,FR[9]),(0x270,0x20,FR[10]),(0x290,0x20,FR[11]),(0x2b0,0x40,FR[12])]:
    put(d,B+o,s,fr,name='DESK')
put(d,0x607c0,0x20,["Utilisateur","Personnage"],prefix=3,name='DESK')
put(d,0x607e0,0x20,["#GUtilisateur","Personnage"],prefix=1,name='DESK')
put(d,0x60800,0x20,["Utilisateur","#GPersonnage"],prefix=1,name='DESK')
btn="%sPar défaut%s      %sEffacer%s        %sValider%s"
for i,off in enumerate((0x60900,0x60930,0x60960,0x60990)):
    c=['']*6
    if i: c[2*(i-1)]='#G'; c[2*(i-1)+1]='#W'
    put(d,off,0x30,[btn%tuple(c)],name='DESK')
# ecran-titre (DEMO.PRG) : libelles du chargement, remplaces sur place
dm=out['DEMO.PRG']
for off,old,fr in [(0xe0a8,b'YES','OUI'),(0xe0b0,b'NO','NON'),(0xe0b8,b'Lv. ','Nv. '),(0xe0c0,b'Time','Temps'),(0xe0c8,b'Unused','Vide'),
                   (0xe0e0,b'slot 1','fente 1'),(0xe0e8,b'slot 2','fente 2'),(0xe0f0,b'Data','Données'),(0xe108,b' Parody Mode',' Mode Parodie'),(0xe118,b'No Data Flag','Sans Data Flag')]:
    assert bytes(dm[off:off+len(old)])==old,(hex(off),bytes(dm[off:off+16])); e=bytes(dm).index(b'\0',off); n=e
    while dm[n]==0: n+=1
    cap=n-off-1; enc=fp.encode(fr); assert len(enc)<=cap,(hex(off),fr,cap); dm[off:off+cap]=enc.ljust(cap,b'\0')
for f,buf in out.items():
    assert len(buf)==os.path.getsize(f); open('out/'+f,'wb').write(buf)
open('out/log.txt','w').write('\n'.join(log))
print(len(log),'objets inscription')

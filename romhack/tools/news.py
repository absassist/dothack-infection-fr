# -*- coding: utf-8 -*-
"""Articles de news (textures xddn_NNN de DATA.BIN) : redessine en francais les 17 articles presents en anglais sur le disque.
Les 52 autres fichiers sont restes en japonais (articles des volumes suivants, non affichables dans Infection)."""
import sys,os,glob; sys.path.insert(0,'tools')
import ccstex
from PIL import Image,ImageDraw,ImageFont
REG='/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
BOLD='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
N=u' '
# zones a conserver (photos, encarts, legendes) : x0,y0,x1,y1 dans l'image a l'endroit
KEEP={'010':[(10,50,148,158)],'030':[(0,165,352,470)],'040':[(10,48,148,160)],'050':[(154,306,342,442)],
'060':[(176,54,340,192)],'070':[(174,130,342,272)],'080':[(10,52,150,156)],'090':[(164,202,336,320)],
'100':[(10,50,124,138)],'110':[(10,50,158,160)]}
A={}
A['010']=("Nouveau système de transport en service",
"Le système de régulation du trafic en temps réel (RTCS) a terminé aujourd'hui sa période d'essai et sera pleinement opérationnel dès demain. Il devrait venir à bout des embouteillages chroniques.\n\n"
"Sa grande particularité : piloter et ajuster les feux de circulation selon la situation. Il sait aussi prévoir le meilleur moment pour les passages à niveau. En cas de crime, il passe au rouge tous les feux du secteur pour empêcher le coupable de fuir. Reste à savoir, bien sûr, si les criminels respecteront le code de la route.")
A['020']=("« The World » dépasse les 20 millions",
"Les ventes du jeu de rôle en ligne « The World » (CC Corporation, décembre 2007) ont dépassé les vingt millions d'exemplaires dans le monde. C'est le premier jeu en ligne sorti depuis l'incident du « Crépuscule des nouveaux dieux ». Il s'est vendu à dix millions d'exemplaires en six mois et ses ventes n'ont cessé de croître au fil des mises à jour.\n\n"
"On compterait environ dix millions d'utilisateurs rien qu'au Japon. Dans son communiqué, CC Corporation déclare : « Nous sommes reconnaissants de ce soutien, mais nous sentons aussi une responsabilité sociale à assumer. »\n\n"
"Selon une source interne, CC Corporation envisage de soumettre le titre au Livre Guinness des records comme « jeu le plus vendu de l'histoire ».")
A['030']=("Visiocasque Neuro Goggle",
"SONES annonce la sortie prochaine d'un nouveau visiocasque, le « Neuro Goggle FMD ». Il est conçu sur mesure pour « The World », le jeu à succès de CC Corporation. Son prix n'est pas encore fixé.")
A['040']=("0,49 % d'erreur",
"La reconnaissance vocale frôle désormais la perfection, avec un taux d'erreur inférieur à 0,5 %. En mode Chat, elle repère les pauses de l'utilisateur et les transcrit par « .... ». Le jour viendra peut-être où les claviers seront obsolètes.")
A['050']=("Nouvelle arme du commerce en ligne",
"Au salon de la vente par correspondance de Makuhari New City, le « Fitting Simulator » a capté toute l'attention de la profession. Mis au point par Benesson, géant de la vente en ligne, il gomme le point faible du secteur : le client saisit ses mensurations et crée sur Internet son double virtuel, qu'il peut habiller à sa guise. Des clientes s'inquiètent toutefois de voir leurs mensurations circuler sur Internet, et Benesson envisage de proposer une version téléchargeable du « Fitting Simulator ».")
A['060']=("« The World » pour les nuls",
"Ce volume va bien au-delà de « The World » : stratégies, astuces et conseils pour profiter du jeu au maximum.\n\nBonne chance !")
A['070']=("Litière pour chat",
"« J'ai toujours rêvé d'une litière pareille ! » Elle se rince à l'eau, donc plus besoin de la nettoyer. Un capteur détecte les mouvements du chat et la garde propre en permanence. Elle se fixe facilement entre les toilettes et l'évacuation, sans aucun tracas.")
A['080']=("Ventes du Neuro Goggle",
"Les ventes du « Neuro Goggle FMD » de SONES, périphérique pour « The World » sorti le 10 du mois dernier, restent très fortes. Le produit est en rupture dans la plupart des magasins et beaucoup repartent les mains vides. Devant ce constat, SONES a décidé d'augmenter la production, mais ses responsables préviennent que la pénurie va durer encore un moment.")
A['090']=("Coma : cause inconnue",
"Deux lycéens de Kanazawa, dans la préfecture d'Ishikawa, ont été retrouvés inconscients dans la salle de leur club. L'un a repris connaissance à l'hôpital, mais l'autre, Tomonari Kasumi, est toujours dans le coma.\n\n"
"Les analyses n'ont révélé ni drogue ni substance addictive dans leur organisme. La cause de leur perte de connaissance fait toujours l'objet d'une enquête.")
A['100']=("Culture de pommes réussie",
"L'institut de recherche Sanyo Ring annonce avoir réussi à cultiver une nouvelle variété de pomme, plus riche en nutriments. Le goût et la texture du prototype sont bons, mais n'ont rien d'une pomme. Certains dégustateurs la trouvent très fade et sèche.")
A['110']=("Enquête sur Bigfoot",
"Une vaste enquête sur Bigfoot a débuté aujourd'hui dans la banlieue de Redding, dans l'Oregon. Les signalements se sont multipliés ces derniers temps, et la municipalité espère relancer ainsi le tourisme local. La créature n'a pas été capturée, mais le barbecue aux recettes de montagne a connu un franc succès. Les élus se disent ravis du résultat.")
A['410']=("Déclaration officielle du WNC",
"Le World Network Council (WNC) a annoncé aujourd'hui que le système d'exploitation réseau « ALTIMIT » équipe désormais près de 100 % du marché mondial. Autrement dit, tous les terminaux en réseau, chez les particuliers comme en entreprise, sont compatibles ALTIMIT.\n\n"
"Pour le service de presse du WNC, l'incident « Pluto's Kiss » de décembre 2005 et les deux années qui ont suivi, connues sous le nom de « Crépuscule des nouveaux dieux », ne sont plus qu'une page d'histoire.\n\n"
"Selon certains responsables, après six années mouvementées, le « New Generation Hyper Net Plan » proposé en avril 2004 est enfin accompli.")
A['420']=("Réseau téléphonique public achevé",
"La modernisation complète des téléphones publics, rendus compatibles avec les terminaux réseau (Net Phone Box), lancée l'an dernier, touche à sa fin.\n\n"
"Tous les téléphones publics du pays sont désormais reliés à un réseau en fibre optique, qui offre une connexion Internet à 100 Mbps depuis n'importe quelle cabine.\n\n"
"Des sceptiques jugeaient improbable de boucler le projet en un an, vu le retard des logiciels compatibles avec l'OS de référence « ALTIMIT », mais les efforts de tous ont payé.\n\n"
"La plupart des mobiles, PDA et ordinateurs portables peuvent se connecter, mais les appareils non compatibles Net Phone Box auront besoin d'un adaptateur. Misant sur cette demande, les fabricants préparent de nouveaux produits et accessoires.")
A['430']=("Annonce du « WonderHawk »",
"BANDAI, grand nom du jouet, a annoncé aujourd'hui le développement d'une nouvelle console portable baptisée « WonderHawk ».\n\n"
"Elle succédera à l'actuelle « WonderSwan Revolution », avec un processeur plus performant.\n\n"
"BANDAI précise qu'elle sera compatible avec l'OS réseau de référence, « ALTIMIT », et qu'elle servira aussi de terminal Internet.\n\n"
"D'après la société, « The World », le célèbre jeu en ligne de CC Corporation, devrait figurer parmi les titres de lancement.")
A['440']=("Informations ALTIMIT",
"Avec l'essor de la fibre optique nouvelle génération, le débit a fortement augmenté dans la plupart des foyers. Une connexion à 100 Mbps est désormais courante dans la plupart des zones urbaines.\n\n"
"CC Corporation annonce donc une mise à niveau majeure, très prochaine, de l'OS réseau de référence « ALTIMIT ».\n\n"
"L'ALTIMIT nouvelle génération gagnera en stabilité et en qualité de communication.\n\n"
"L'OS était déjà réputé pour sa stabilité et sa sécurité, mais CC Corporation affirme dans son communiqué que cette mise à niveau créera un environnement réseau « presque parfait », diffusé dans les foyers du monde entier.")
A['450']=("Un coma causé par un jeu en ligne ?",
"Une rumeur se répand depuis peu chez les internautes : les jeux en ligne pourraient faire perdre connaissance à un joueur et le plonger dans le coma.\n\n"
"Le jeu visé est « The World » de CC Corporation, actuellement en lice pour le Livre Guinness des records comme « jeu le plus vendu de l'histoire ».\n\n"
"Un porte-parole de CC Corporation assure que ces rumeurs sont « sans aucun fondement » et qu'aucune mesure n'est prévue à leur sujet.")
A['460']=("Réforme de la loi de sécurité du réseau",
"Réuni aujourd'hui en session extraordinaire, le Congrès a ouvert le débat sur la révision de la loi réseau, qui « interdit tout acte ou rassemblement susceptible de perturber le bon fonctionnement du réseau et d'entraîner dégâts ou obstruction ».\n\n"
"Cette loi a été votée en 2003 pour s'aligner sur les règles internationales fixées sous l'égide du World Network Council (WNC).\n\n"
"La peine de mort, peine maximale prévue par ce texte, a été prononcée contre le responsable de l'épidémie « Deadly Flash » de décembre 2003, la pire attaque virale de l'ancienne ère du réseau. La sentence n'a pas encore été exécutée.\n\n"
"Le débat porte surtout sur le maintien ou non de la peine de mort dans la loi.\n\n"
"La portée et l'existence même du texte sont vivement discutées : aucun cybercrime majeur n'a eu lieu depuis la diffusion d'ALTIMIT, et beaucoup estiment qu'il n'y a aucun danger dans un avenir proche.")

def nb(s):
    """espaces insecables a la francaise"""
    for a in ('« ',): s=s.replace(a,'«'+N)
    for a in (' »',' :',' ;',' ?',' !',' %'): s=s.replace(a,N+a[1:])
    return s
def upright(t):
    w,h=t['w'],t['h']; d=t['data']
    return [bytearray(d[(h-1-y)*w:(h-y)*w]) for y in range(h)]
def flow(text,size,keep,bottom):
    """liste de (x,y,ligne) ou None si ca ne tient pas"""
    f=ImageFont.truetype(REG,size); pitch=int(round(size*1.3)); y=54; out=[]
    def slot(y):
        iv=[(14,343)]
        for x0,y0,x1,y1 in keep:
            if y0-4<y+pitch and y-2<y1+4:
                ni=[]
                for a,b in iv:
                    if x1+8<=a or x0-8>=b: ni.append((a,b))
                    else:
                        if x0-8-a>0: ni.append((a,x0-8))
                        if b-(x1+8)>0: ni.append((x1+8,b))
                iv=ni
        iv=[i for i in iv if i[1]-i[0]>=95]
        return max(iv,key=lambda i:i[1]-i[0]) if iv else None
    for para in text.split('\n\n'):
        words=nb(para).split(' '); cur=''
        while words or cur:
            s=slot(y)
            if y+pitch>bottom-4: return None
            if s is None: y+=pitch; continue
            wmax=s[1]-s[0]; cur=''
            while words:
                t=(cur+' '+words[0]) if cur else words[0]
                if f.getlength(t)<=wmax: cur=t; words.pop(0)
                else: break
            if not cur: cur=words.pop(0)
            out.append((s[0],y,cur)); cur=''; y+=pitch
        y+=int(pitch*0.75)
    return out,f
def render(d,n):
    title,body=A[n]; t=ccstex.tex(d,'TEX_xddn_'+n); assert t['typ']==0x13 and t['w']==512
    rows=upright(t); pal=[c[:3] for c in t['pal']]; W=H=512
    im=Image.new('RGB',(W,H)); px=im.load()
    for y in range(H):
        r=rows[y]
        for x in range(W): px[x,y]=pal[r[x]]
    orig=im.copy(); keep=KEEP.get(n,[])
    # bas de page : la ou la colonne x=100 devient noire jusqu'en bas
    bottom=H
    while bottom>60 and px[100,bottom-1]==(0,0,0) and px[200,bottom-1]==(0,0,0) and px[300,bottom-1]==(0,0,0): bottom-=1
    dr=ImageDraw.Draw(im)
    # bandeau : chaque rangee reprend sa couleur dominante
    for y in range(3,39):
        # couleur du bandeau sur cette rangee = mediane des pixels qui ne sont pas du texte (noir)
        row=[px[x,y] for x in range(24,327) if max(px[x,y])>=70] or [px[x,y] for x in range(24,327)]
        c=tuple(sorted(v[k] for v in row)[len(row)//2] for k in range(3)); dr.line([(24,y),(326,y)],fill=c)
    size=15
    while True:
        fb=ImageFont.truetype(BOLD,size)
        if fb.getlength(nb(title))<=292 or size<=10: break
        size-=1
    dr.text((32,20),nb(title),font=fb,fill=(0,0,0),anchor='lm')
    # corps : blanc partout sauf les zones conservees
    def kept(x,y): return any(x0<=x<=x1 and y0<=y<=y1 for x0,y0,x1,y1 in keep)
    for y in range(46,bottom):
        for x in range(0,353):
            if not kept(x,y): px[x,y]=(255,255,255)
    for size in (16,15,14,13,12,11):
        r=flow(body,size,keep,bottom)
        if r: break
    assert r,(n,'texte trop long')
    lines,f=r
    for x,y,s in lines: dr.text((x,y),s,font=f,fill=(0,0,0))
    # retour en indices : seuls les pixels modifies sont recalcules (couleur de palette la plus proche)
    cache={}; op=orig.load()
    def near(c):
        if c not in cache: cache[c]=min(range(len(pal)),key=lambda i:(pal[i][0]-c[0])**2+(pal[i][1]-c[1])**2+(pal[i][2]-c[2])**2)
        return cache[c]
    for y in range(H):
        r=rows[y]
        for x in range(W):
            c=px[x,y]
            if c!=op[x,y]: r[x]=near(c)
    data=b''.join(bytes(rows[H-1-y]) for y in range(H))
    out=bytearray(d); out[t['off']:t['off']+t['n']]=data
    return bytes(out),size,len(lines),bottom
def preview(d,n):
    t=ccstex.tex(d,'TEX_xddn_'+n); im=ccstex.image(t).transpose(Image.FLIP_TOP_BOTTOM).convert('RGB').crop((0,0,360,512)); return im
if __name__=='__main__':
    dst=os.path.expanduser('~/mnt/roms/dothack-fr/img/news_fr/'); os.makedirs(dst,exist_ok=True); os.makedirs('news_fr',exist_ok=True)
    for n in sorted(A):
        p=glob.glob('data/*_xddn_%s.cmp'%n)[0]; d=open(p,'rb').read()
        new,size,nl,bottom=render(d,n); open('news_fr/xddn_%s.cmp'%n,'wb').write(new)
        preview(new,n).save(dst+'xddn_%s.png'%n); print(n,'police',size,'lignes',nl,'bas de page',bottom)

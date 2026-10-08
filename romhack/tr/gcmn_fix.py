# -*- coding: utf-8 -*-
"""Corrections de largeur (audit) : charge en dernier."""
import gcmn_00
_R={"Enchaîne les coups à grande vitesse.":"Enchaîne les coups ultra-rapides.",
"Frappe à grande vitesse en dansant.":"Frappe vite, comme une danse.",
"Lâche une boule de feu sur la cible.":"Lâche une boule de feu.",
"Lâche des boules de feu sur la cible.":"Lâche des boules de feu.",
"Des crânes convergent sur la cible.":"Des crânes fondent sur la cible."}
SK={k:[_R.get(l,l) for l in v] for k,v in gcmn_00.SK.items() if any(l in _R for l in v)}
G={
102:"Le Livre Ryu I crée un objet.",105:"Le Livre Ryu II crée un objet.",107:"Le Livre Ryu III crée un objet.",111:"Le Livre Ryu IV crée un objet.",114:"Le Livre Ryu V crée un objet.",116:"Le Livre Ryu VI crée un objet.",121:"Le Livre Ryu VII crée un objet.",125:"Le Livre Ryu VIII crée un objet.",109:"Liste des noms complète.",110:"Echanges faits avec tous.",113:"Liste des monstres complète.",120:" coffres Gott ouverts.",144:"C'est bien trop cher !",
190:"Je maîtrise enfin le jeu.",138:"Si j'avais plus de sous...",164:"Qui veut échanger ?",
216:"Je veux des Légume racines groin",
440:["Il paraît que c'est des hackers...","Ca craint vraiment rien... ?"],
473:["T'as entendu ? Les derniers soucis","viendraient de hackers."],
659:["Content qu'ils aient trouvé...","Bon, je me déconnecte...",""],
724:["Et l'été, du ragoût brûlant","sous la clim...","C'est mal... ?"],
744:["J'essaie de battre le record.","48 heures non-stop ! Je sais pas","si je vais tenir, par contre."],
807:"Attends, on s'est vus en vrai ?",
1089:"J'espère qu'on sera plus forts !",
1149:["Hmm, pas gagné grand-chose...","La prochaine, on devient riches !"],
1203:["Je peux vraiment l'avoir","gratuitement ?","... Merci beaucoup."],
1252:"C'était le plus rapide de la tribu.",
1263:"Donc genre, laisse-moi, OK ?",
1268:"Moi c'est Suzie, le Grunty errant.",
1282:"Je veux un truc juteux, groin !",
1293:"Ca pousse près d'un cocon, groin !",
1320:"Ca pousse près de bernacles groin !",
1372:["Mon maître... Mon dos n'est","pas un scarabée, clang !"],
1381:["Maître ?","Vous êtes bien rouge, coâ !","On échange, coâ ?"],
1410:["Echangeons mes jolies choses","contre celles du chef, ssss !"],
1414:["Trop bruyant, ssss ?","Je ne sais parler que","comme ça, ssss !"],
1421:["Roi Rouge ? Besoin de","quelque chose, gloup gloup ?"],
1433:"Je pars à mon heure, gloup gloup !",
1444:"Salut, baby ! Mon petit coeur !",
1457:["T'inquiète pas... Laisse un","vieil homme payer sa dette..."],
1464:"Tu es le portrait de mon fils !",
1469:["Hé hé ! Saperlipopette !","C'est comme une renaissance !"],
}
# noms d'objets traduits : repliques des Grunty
G.update({210:'Je veux de la Menthe Grunt groin !',211:'Je veux des Oignons vespéraux groin',212:'Je veux du Cactus serpent groin !',213:'Je veux du Melon Oh Non groin !',
214:'Je veux des Cordyceps groin !',215:'Je veux des Cerises blanches groin',216:'Je veux des Légumes racines groin',217:'Je veux des Citrouilles groin !',
218:'Je veux des Champignons groin !',219:'Je veux des Mandragores groin !',220:'Je veux des Pommes de pin groin !',221:'Je veux des Oeufs immatures groin',
222:'Je veux des Oeufs ours-chat groin',223:'Je veux des Oeufs invisibles groin',224:'Je veux des Oeufs sanglants groin',225:"Je veux des Oeufs d'or groin !",
1313:'Je veux de la Menthe Grunt, groin !',1315:'Je veux des Oignons vespéraux, groin !',1317:'Je veux du Cactus serpent, groin !',1319:'Je veux du Melon Oh Non, groin !',
1323:'Je veux des Cerises blanches, groin !',1325:'Je veux des Légumes racines, groin !',1327:'Je veux des Citrouilles, groin !',1329:'Je veux des Champignons, groin !',
1331:'Je veux des Mandragores, groin !',1333:'Je veux des Pommes de pin, groin !',1335:'Je veux des Oeufs immatures, groin !',1337:'Je veux des Oeufs ours-chat, groin !',
1339:'Je veux des Oeufs invisibles, groin !',1341:'Je veux des Oeufs sanglants, groin !',1343:"Je veux des Oeufs d'or, groin !"})
G.update({211:"Je veux de l'Oignon vespéral groin",1315:"Je veux de l'Oignon vespéral, groin !",1323:'Je veux une Cerise blanche, groin !',
1335:'Je veux un Oeuf immature, groin !',1341:'Je veux un Oeuf sanglant, groin !'})
# tutoiement : les bulles de groupe sont partagees entre personnages (BlackRose comprise)
G.update({911:"Quoi ? Oui, je peux t'aider ?",927:"Après t'avoir parlé, je brûle de faire des recherches...",1094:"Oui, que puis-je pour toi ?",1095:"Grâce à toi, je ne me perds plus.",
1151:"Merci pour aujourd'hui.\nPrends soin de toi.",1225:"Quel merveilleux cadeau !\nMerci infiniment.\nTu me combles de joie !",
1496:"T'es sûr de pas avoir besoin de moi ?",1582:"Admire mon savoir-faire !",1583:"Regarde bien.",1591:"Gare à toi !",1674:"Tu veux un affaiblissement ?",
1691:"Laisse-moi panser tes blessures...",1798:"J'aimerais que tu me ranimes.",1815:"Tu peux guérir mes altérations de statut ?",1833:"Je te remercie beaucoup.",
1850:"Jamais je n'oublierai ta bonté.",1867:"Je te remercie.",1962:"Je te suivrai n'importe où !",2095:"Tu peux restaurer mes HP perdus ?",
2113:"Tu peux guérir mon altération de statut ?",2221:"Laisse-moi faire, s'il te plaît.",2222:"#0, laisse-moi faire !",2862:"Un instant, s'il te plaît.",
2950:"Besoin de soins ou de guérison ?",3001:"Tu peux me guérir, s'il te plaît ?",3071:"Je ne peux que te soutenir par la parole...",3120:"Tu es gentil.",
3249:"N'en fais pas trop, s'il te plaît.",3250:"Je compte sur toi, #0 !"})

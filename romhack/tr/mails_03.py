VC3="""#Yserveurs %0#W et #Y%4#W :

Petits monstres : #YVirus Core A#W
Monstres moyens : #YVirus Core B#W
Grands monstres : #YVirus Core C#W
(il y a des exceptions)

Serveur #Y%1#W :

Petits monstres : #YVirus Core D#W
Monstres moyens : #YVirus Core E#W
Grands monstres : #YVirus Core F#W
(il y a des exceptions)

Serveur #Y%2#W :

Petits monstres : #YVirus Core G#W
Monstres moyens : #YVirus Core H#W
Grands monstres : #YVirus Core I#W
(il y a des exceptions)"""
def cleared(v): return dict(subject="Partie terminée",body="""Félicitations, vous avez terminé .hack//%s. Vous possédez désormais le #YData Flag#W de .hack//%s.

Une sauvegarde faite dans cet état (en jaune) peut être importée dans le volume suivant. Les données sans Data Flag ne seront pas importées, alors faites attention.

Vous pouvez poursuivre l'aventure avec ces données (l'histoire principale n'avancera plus).

Les objets et l'expérience gagnés après la fin sont importables dans le volume suivant : vous pouvez donc renforcer votre personnage avant de reprendre l'histoire."""%(v,v))
M={
62:dict(subject="De retour",body="""On sait pas quand ça va replanter, alors autant y aller tant qu'on peut encore se connecter à ce truc."""),
63:dict(subject="Ha ha ha",body="""C'est à moi ?
J'attends en coulisses, côté jardin !"""),
64:dict(subject="Sans objet",body="""Si la source de l'infection est bien la #YVague maudite#W, le mieux à faire est de lancer un programme de brouillage sur la zone où l'on suppose que la Vague se trouve, afin de stopper la propagation. Il nous faudra pour cela l'aide de Helba.

Rends-toi au Net Slum. J'ai aussi trouvé les mots-clés qui y mènent directement :
#B%1 Pulsating Truth's Core#W."""),
65:dict(subject="Pit%%9",body="""Fid@h=l6 va s'e&fuir *u (%%eh^rs av-c m@n f>agm?nt.

Pit%%9, r4mène-;e !"""),
66:dict(subject="Ordres",body="""Enquête sur une zone infectée. Détails à la boutique d'armes de la #YRoot Town %2#W."""),
67:dict(subject="Parfait",body="""Contacte-moi quand t'es prêt. Laisse-moi faire, je gère. Je t'attends à la Chaos Gate de la #YRoot Town %1#W. Ah, et jette un oeil au Forum avant de venir.
A plus !"""),
68:dict(subject="Sans objet",body="""Tu as su obtenir l'aide de Lios et de Helba. Je suis impressionné.

Et Helba, Reine des Ténèbres,
  a enfin levé son armée.
Apeiron, Roi de la Lumière, appelle...
Contre l'abominable "Vague",
  ensemble ils combattent.

C'est exactement comme dans l'Epitaphe.

Nous ignorons toujours l'origine de la "Vague maudite", mais avec l'aide de Helba et de Lios, nous devrions pouvoir resserrer les recherches. Tout cela, c'est grâce à toi."""),
69:dict(subject="Opération",body="""Tirons la leçon de notre erreur : au lieu de lancer le programme de brouillage sur la zone elle-même, nous allons tenter de mettre en quarantaine la zone où nous pensons que la #YVague#W se trouve. C'est à mon sens la méthode la plus efficace. J'aimerais discuter du plan en détail. Viens au Net Slum."""),
70:dict(subject="Opération 2",body="""Rapports de Lios et de Helba :

Lios :
>Il y a une nouvelle victime.
>Vu l'agitation de notre unité
>chargée d'étouffer l'affaire,
>l'information semble exacte.

Helba :
>Sur le #Yserveur %2#W, le volume de
>données de la zone
>#B%2 Chatting Snaring Twins#W
>augmente. Aucune autre hausse
>notable : frappons là d'abord.

Comme l'indiquent ces rapports,
#B%2 Chatting Snaring Twins#W
semble être la bonne. Je propose d'exécuter notre plan.

Opération : #YTETRAPOD#W

Rassemblement au Net Slum.
Ce sera tout."""),
71:cleared("OUTBREAK"),
72:dict(subject="Par=@r&",body="""Vi&ns à la #Yv*lle %2#W, pit$é. J'ai qu@lque ch5se à te d?re."""),
73:dict(subject="Virus Cores 3",body="""Cherche les Virus Cores nécessaires d'après ces informations :

"""+VC3),
74:dict(subject="En mouvement",body="""L'énorme masse de données que nous pensons être la #YVague maudite#W se déplace toujours. Nos méthodes précédentes échoueront sans doute. Venez à la #YRoot Town %3#W pour une réunion. J'ai validé votre inscription sur le #Yserveur %3#W.

Sélectionnez-le à la Chaos Gate."""),
75:dict(subject="Encore un peu",body="""#0, m&r3i.
Je t'a! peut-=tre de+andé de fa6re une ch>se horr$ble...

Mais pr@te-moi ton ai7e enc5re un 4eu..."""),
76:dict(subject="Rassemblement",body="""Les préparatifs de l'opération sont terminés. Rendez-vous à la #YRoot Town %3#W dès réception de ce mail."""),
77:dict(subject="Forum",body="""Va voir le Forum."""),
78:dict(subject="Pa>don",body="""#0,
Je voulais que tu $^44es Morganna, mais à @au=e de ça, Orca... Pa5don.

Ne c?mbats pas Cubia. &$bia est t6n ombre et celle du Bracelet.

Va!ncre =5bia, c'est 9é8r%%0re le Bracelet. Ne <+*3ts pas Cubia p1ur l'instant."""),
79:dict(subject="Harald",body="""Je ne sais plus quand, mais j'ai discuté avec une IA errante nommée Harald. Après avoir dit ce qu'il avait à dire, il a demandé : "Où est le Sanctuaire ?" Je ne voyais pas de quoi il parlait, mais il insistait, alors je lui ai répondu : "C'est vous qui le savez le mieux." Satisfait, il est parti en marmonnant : "C'est vrai. Je crois que c'était à
#B%0 Reincarnated Purgatorial Altar#W."

Il y a peut-être quelque chose ici :
#B%0 Reincarnated Purgatorial Altar#W."""),
80:dict(subject="Système rétabli",body="""Merci pour votre aide dans le rétablissement du système de #YThe World#W. Profitez à présent du vrai visage de #YThe World#W.

           Lios la tête de mule. :-)"""),
81:dict(subject="Comment vas-tu ?",body="""J'aimerais te donner quelque chose. Viens avec Orca ici :
#B%0 Bursting Passed Over Aqua Field#W."""),
82:dict(subject="Virus Cores 4",body="""Voici de nouvelles informations sur les Virus Cores.

"""+VC3+"""

Serveur #Y%3#W :

Petits monstres : #YVirus Core J#W
Monstres moyens : #YVirus Core K#W
Grands monstres : #YVirus Core L#W
(il y a des exceptions)"""),
83:dict(subject="Sans objet",body="""Je vais ici :
#B%4 Beautiful Someone's Treasure Gem#W."""),
84:dict(subject="Le géant céleste",body="""Avez-vous vu le #Ygéant mystique#W dans le ciel des zones %0 ?!

D'après la rumeur, la flotte aérienne qui transportait le géant il y a des millénaires a eu un accident, et elle erre depuis avec lui pour l'éternité.

#B%0 Hideous Someone's Giant#W

Utilisez ce mot-clé pour percer le mystère de la flotte maudite qui erre dans les cieux !

PS : j'ai oublié de vous le dire, mais j'ai ajouté un #GVirus Core T#W à vos objets."""),
85:dict(subject="Tu fais quoi...",body="""...quand t'es dans ta chambre ? Te contente pas de jouer, sors et fais du sport.
Tu vas grossir =)"""),
86:dict(subject="RE: Ben, des fois...",body=""">A part l'EPS, je joue au foot
>avec mes potes...
>
>Mais juste de temps en temps.

Je joue pas au foot, mais j'aime bien en regarder."""),
87:dict(subject="RE: Et toi ?",body="""Merci de demander !
Je suis dans l'équipe de tennis de mon lycée ! La seule en seconde à être titulaire !

Mon but, c'est de jouer sur le court central de Wimbledon ! Hé hé. :)"""),
88:dict(subject="RE: En seconde...?!",body=""">T'es en seconde, au lycée ?

Ben oui, en seconde. Je te l'avais pas dit ?"""),
89:dict(subject="RE: Moi, en 4e",body=""">...tu savais ?

Ah, t'es en 4e... je vois... Bon, si t'as un souci, viens en parler à ta grande soeur.
...mais oui bien sûr, hé hé ;)"""),
90:dict(subject="Au début",body="""Au début t'étais un peu un cas désespéré, mais en fait t'es pas si mal."""),
91:dict(subject="Tout ça...",body="""Tout arrive en même temps, je compte sur toi, partenaire !"""),
92:dict(subject="C'est Mistral ;)",body="""J'ai fait une tarte aux pommes l'autre jour, mais je l'ai un peu ratée ;( J'ai légèrement cramé la garniture...

Et toi #0, t'aimes quoi ?"""),
93:dict(subject="RE: Tarte aux pommes",body=""">J'adore ça ! Une boule de glace
>vanille sur une tarte aux pommes
>toute chaude, y a pas mieux !

Oui oui ;)
C'est troooop bon.

Mais je suis plus douée pour les plats que pour les desserts."""),
94:dict(subject="RE: Boeuf mijoté",body=""">Le boeuf mijoté, mon plat préféré !

#0, t'aimes le boeuf mijoté ? C'est ma grande spécialité !

Chez nous, on ajoute du beurre à la fin. Comme ça, même avec du boeuf pas cher, c'est super bon :9"""),
95:dict(subject="RE: Tu cuisines bien",body=""">Merci.
>J'essaierai la prochaine fois.

Mais j'en rate plein aussi :/
#0, tu fais les courses, toi ?"""),
96:dict(subject="RE: Des fois...",body=""">On m'y traîne pour porter. :-)
>J'ai halluciné en voyant le prix
>de ce que je mange.

Hé hé, moi j'ai jamais rien acheté au prix normal. Si t'y vas juste avant la fermeture, les produits frais les plus chers sont à plus de moitié prix !!! Et j'adore marchander pour faire encore baisser. :)"""),
97:dict(subject="Dis-moi",body="""Tu cuisines ?
De nos jours, un garçon doit savoir cuisiner s'il veut plaire aux filles. :D"""),
98:dict(subject="Question",body="""Jamais je n'oublierai ce qu'est la jeunesse, mais me voici face à un dilemme, car j'ai le coeur d'un jeune garçon ! Ma jeunesse fut vouée au graphisme ! Et pour toi, que signifie la jeunesse ?"""),
99:dict(subject="De la jeunesse",body="""Ha ha, il se pourrait bien ! Tu dis vrai, Beaux Yeux ! Tu es décidément quelqu'un de confiance ! Et moi, je suis formidable de te faire confiance !! Au fait, Beaux Yeux, les jeux seraient-ils superflus ?"""),
100:dict(subject="RE: C'est bien",body=""">Je trouve ça bien qu'ils existent.
>Y jouer tout le temps, je sais pas,
>mais ça fait vivre des choses
>qu'on vivrait pas autrement.

Tu as parfaitement raison ! Les jeux sont un plaisir, mais n'emploie point de mots tels que "daube" !

Il y a même un dicton : nul besoin de couteau pour achever un créateur de jeux. Il suffit de dire que c'est de la daube."""),
101:dict(subject="RE: Tu es",body=""">quelqu'un qui fait des jeux ?

Je ne répondrai à aucune question sur ma vie privée ! Le mystère a tellement plus d'allure. Ha ha ha ha ha."""),
102:dict(subject="Un peu inquiet",body="""Tu ne sembles guère en forme ces temps-ci. Tu devrais napper une banane au four de sauce à la prune et la manger !"""),
103:dict(subject="Yojimbo",body="""Mon nom vient du personnage "Kuwabatake Sanjuro" dans le classique du cinéma "Yojimbo"."""),
104:dict(subject="RE: Vraiment ?",body=""">Je vois.
>Je croyais que c'était un nom
>ancien, mais ça vient d'un film.
>Il est plutôt classe, ce nom.

J'adore Mifune.
J'ai même sa figurine."""),
105:dict(subject="RE: Waouh",body=""">Elle est comment ?

Le sabre est plutôt réussi, mais j'aurais aimé qu'elle ait aussi cette espèce de vase où l'on met le saké...

Là, elle serait parfaite..."""),
106:dict(subject="RE: C'est",body=""">C'est pas un vase, ça s'appelle
>un "tokkuri".

Je vois ! Ca s'appelle un "tokkuri".

J'ai appris quelque chose aujourd'hui.

Le japonais est très difficile."""),
107:dict(subject="Yojimbo",body="""Si tu as besoin de moi, appelle quand tu veux. Selon les circonstances, je te donnerai un coup de main."""),
108:dict(subject="Ce que j'aime",body="""J'aime la nourriture crue..."""),
109:dict(subject="RE: Ah bon ?",body=""">Comme quoi ?

Le poulpe."""),
110:dict(subject="RE: Moi aussi",body=""">C'est marrant un poulpe, on peut
>rien lui reprocher.

Hm ?
De quoi tu parles ?"""),
111:dict(subject="RE: Hein ?",body=""">T'aimes quoi chez les poulpes ?

La texture.
Je préfère le poulpe, le calmar et le concombre de mer. Tout ce qui est ferme sous la dent.

J'aime surtout les ventouses."""),
112:dict(subject="Hmmm",body="""Je crois qu'on va très bien s'entendre."""),
113:dict(subject="Présentation",body="""Vrai nom : Natsume Oguro, en 3e, 15 ans. Je m'occupe de la bibliothèque du collège. J'ai commencé le jeu pour changer. Je vais sûrement causer plein de soucis, mais merci de m'accepter dans ton équipe."""),
114:dict(subject="RE: Je suis en 4e",body=""">T'as un an de plus que moi.
>Moi aussi j'ai commencé à jouer
>y a pas longtemps.
>
>Je m'amuse bien !

Tu as un an de moins que moi ? Tu avais l'air si fiable que je te croyais plus âgé. Tu joues bien mieux que moi =)

Tu lis des livres ?"""),
115:dict(subject="RE: Je lis",body=""">J'aime la science-fiction. Mais
>les livres coûtent trop cher,
>j'ai pas assez d'argent...

Oh, moi aussi j'adore ça ! Je m'occupe de la bibliothèque parce que comme ça, je lis les nouveautés avant tout le monde =)

Et si ça me plaît, je vais l'acheter en librairie."""),
116:dict(subject="RE: Livres préférés",body=""">T'as pas envie, des fois, de
>relire ton livre préféré ?

Si, après plusieurs lectures, on le ressent autrement. Mon rêve, c'est de remplir mon étagère de mes livres préférés."""),
117:dict(subject="=)",body="""Je suis si contente de pouvoir jouer avec toi, #0 ! J'ai l'impression
que je peux changer. Continue à m'appeler, s'il te plaît :)"""),
118:dict(subject="Vengeance !",body="""J'ai découvert où se trouve le joueur félin qui m'a humilié ! Viens ici :
#B%1 Shapeless Haunted Holy Ground#W
pour en être le témoin !"""),
119:dict(subject="Sans objet",body="""#B%1 Quiet Oblivious Cabbage#W."""),
120:dict(subject="Besoin d'aide",body="""On parle d'une grande épée ici :
#B%1 Bitter Hot-Blooded Sand Trap#W.
Si tu as le temps, accompagne-moi jusqu'au dernier niveau."""),
121:dict(subject="Je serai plus forte !",body="""Bonjour ! Adieu, l'ancienne Natsume bonne à rien ! La prochaine fois qu'on se verra, mon niveau sera #Y10 fois#W plus élevé !! A bientôt !"""),
122:dict(subject="Pas obligé",body="""Mais aide.
#B%1 Bottomless Guffawing Raw Ore#W."""),
123:dict(subject="La cité inversée",body="""La cité inversée dans le ciel. Nul ne connaît son vrai nom. Ni ce qu'il est advenu de ses habitants...

Pour percer ses secrets, rendez-vous ici :
#B%4 Bitter Fantasy Mirror World#W
et voyez de vos propres yeux !"""),
124:dict(subject="Hier",body="""On avait piscine en EPS, et j'ai halluciné du nombre de gens qui savent pas nager..."""),
}

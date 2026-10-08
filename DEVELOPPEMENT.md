# Développement

Ce document explique comment le patch est fabriqué et comment le reconstruire depuis votre propre ISO.

## Prérequis

- Python 3.10+ et [Pillow](https://pypi.org/project/Pillow/) (`pip install pillow`)
- Polices Liberation (`fonts-liberation` sous Debian/Ubuntu) : utilisées pour redessiner les textures
- Votre ISO USA de .hack//Infection (SLUS-202.67, MD5 `eca5b2c41b7833ee38d489002c7aabc4`)
- [xdelta3](https://github.com/jmacd/xdelta-gpl) pour générer le patch

La chaîne a été développée et testée sous Linux. Sous Windows, passez par WSL.

## Reconstruire l'ISO et le patch

```sh
cd romhack
export DOTHACK_ISO="/chemin/vers/Dot Hack Part 1 - Infection (USA).iso"

python3 ext.py "$DOTHACK_ISO"     # extrait SLUS_202.67, les .PRG, DATA.BIN, la scène de l'Épitaphe
python3 scan.py                   # décompresse DATA.BIN dans data/ + data_index.json
python3 tools/build.py            # applique toutes les traductions -> out/
python3 tools/mkiso.py "/chemin/vers/infection-fr.iso"   # copie l'ISO USA puis y écrit out/

xdelta3 -e -9 -B 536870912 -s "$DOTHACK_ISO" "/chemin/vers/infection-fr.iso" dothack-infection-fr.xdelta
```

`build.py` est déterministe : à partir de la même ISO, il produit exactement les mêmes fichiers.

## Organisation

```
romhack/
├── ext.py, scan.py, elf.py     extraction de l'ISO, lecture de l'exécutable (sections, symboles, relocations)
├── tools/                      outils de romhacking
│   ├── build.py                construit tous les fichiers modifiés dans out/
│   ├── mkiso.py                réécrit les fichiers dans l'ISO (en place ou en fin d'image)
│   ├── fontpatch.py            accents dans les polices du jeu
│   ├── mails.py, replies.py    mails du bureau et réponses de Kite (DESKTOP.PRG)
│   ├── bbs.py, toppage.py      forum (TOPPAGE.PRG)
│   ├── elfmod.py               textes de l'exécutable (dialogues, menus, système)
│   ├── gcmn.py                 textes de GCMN.PRG (PNJ, combats, objets, monstres…)
│   ├── ccstex.py               lecture/écriture des textures CCS
│   ├── epitaph.py, news.py, titlemenu.py   textures redessinées
│   └── gchk.py, audit.py, gaudit.py, eaudit.py   contrôles (largeurs, textes oubliés)
└── tr/                         les traductions
    ├── mails_NN.py, replies_fr.py, bbs_NN.py
    ├── elf_NN.py, elf_fix.py
    ├── gcmn_NN.py, gcmn_fix.py, gcmn_menu.py, gcmn_keys.py
    └── names_items.py, names_weapons.py, names_misc.py
```

## Fonctionnement technique

### Fichiers de texte

- `SLUS_202.67` (exécutable), `DATA/DEMO.PRG`, `DESKTOP.PRG`, `GCMN.PRG`, `TOPPAGE.PRG` : texte ASCII, lignes séparées par `\0`.
- Les `.PRG` sont des overlays chargés à `0x400800` (adresse = offset fichier + `0x400800`).
- L'exécutable contient encore sa table de symboles et les sections `.rel*` des overlays : chaque pointeur vers un texte est connu, ce qui permet de **déplacer** les textes au lieu de les remplacer sur place.

### Place pour le français

Le français est plus long que l'anglais. Plutôt que de raccourcir, les textes traduits sont écrits ailleurs et les pointeurs redirigés :

- **DESKTOP.PRG / TOPPAGE.PRG** : fichier agrandi (original + zéros du bss + nouveaux textes), replacé en fin d'ISO.
- **Exécutable** : le tas est décalé (`_end` `0x730600` → `0x7B0600`) et un segment de programme supplémentaire (en-tête n°5) charge les textes en `0x790600`.
- **GCMN.PRG** : fichier agrandi jusqu'à `0x730600` (bss mis dans le fichier, taille bss de l'en-tête à 0).
- Les chaînes sans pointeur propre (fragments, écrans des Livres Ryu) sont remplacées **sur place**, dans la limite de leur emplacement (`names_misc.INPLACE_A`).

Aucune instruction du code du jeu n'est modifiée : uniquement des données, des en-têtes et des pointeurs.

### Moteur de texte

- Codes : `#W #R #G #B #Y` couleurs, `#0` nom du personnage, `%0`… symboles de serveurs, `%9%A` étoile, etc.
- Accents : glyphes inutilisés de la police remplacés (`é={ è=} à=[ ê=] ç=| ù=` â=~ î=\ ô=%F û=%G`, voir `tools/fontpatch.py`).
- `ô` et `û` occupent deux octets : un espace est ajouté en fin de ligne pour compenser.
- Largeurs max (grande police) : dialogues 363 px, mails 408 px, forum 547 px, noms d'objets ~160 px.

### Textures

- `DATA.BIN` : membres gzip alignés sur 2048 octets ; la table des tailles est dans l'exécutable (entrées de `0x2c` octets).
- `STR1E.BIN` / `STR1.BIN` : scènes (Épitaphe, animation de l'écran titre).
- Les textures CCS sont lues et réécrites par `tools/ccstex.py` (8 bpp `0x13`, 4 bpp `0x14`, image retournée verticalement, alpha 0..128).

### Clés des textes de GCMN.PRG

Les dictionnaires `G` de `tr/gcmn_NN.py` sont indexés par numéro de texte. `tr/gcmn_keys.py` associe chaque numéro à une empreinte SHA-1 du texte anglais : l'outil retrouve les textes dans votre copie du jeu sans que le script anglais soit publié ici.

## Contrôles

```sh
python3 tools/gchk.py gcmn_06          # largeur et nombre de lignes d'un fichier de traduction GCMN
python3 tools/gaudit.py                # chaînes de GCMN.PRG non couvertes -> gaudit.txt
python3 tools/eaudit.py                # idem pour l'exécutable -> eaudit.txt
```

## Contribuer

Corrections bienvenues par Issue ou pull request : modifiez le fichier `tr/` concerné, vérifiez avec les contrôles ci-dessus, puis reconstruisez.

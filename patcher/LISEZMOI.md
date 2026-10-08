# Patcher Windows

Script pour appliquer le patch sans installer de logiciel.

1. Placez dans ce dossier :
   - `appliquer_patch.bat` (ce dossier),
   - `dothack-infection-fr.xdelta` (à télécharger dans les [Releases](../../../releases)),
   - `xdelta3.exe` : téléchargez `xdelta3-3.1.0-x86_64.exe.zip` sur [la page officielle de xdelta](https://github.com/jmacd/xdelta-gpl/releases) et extrayez-le ici.
2. Glissez votre ISO USA sur `appliquer_patch.bat`.
3. Une nouvelle ISO `... (FR).iso` est créée à côté de l'originale, qui n'est pas modifiée.

Windows peut afficher un avertissement SmartScreen au premier lancement de `xdelta3.exe` : c'est l'outil officiel, non signé.

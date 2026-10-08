@echo off
setlocal
cd /d "%~dp0"
title .hack//Infection - patch FR
echo ==============================================
echo   .hack//Infection - traduction francaise
echo ==============================================
echo.
if "%~1"=="" (
  echo Glisse ton ISO USA de .hack//Infection sur ce fichier .bat
  echo ^(SLUS-202.67, MD5 eca5b2c41b7833ee38d489002c7aabc4^)
  echo.
  pause
  exit /b 1
)
set "XD="
for %%f in (xdelta3*.exe) do set "XD=%%f"
if not defined XD (
  echo xdelta3.exe introuvable dans ce dossier.
  echo Telecharge-le ici : https://github.com/jmacd/xdelta-gpl/releases
  echo ^(fichier xdelta3-3.1.0-x86_64.exe.zip, a extraire a cote de ce .bat^)
  echo.
  pause
  exit /b 1
)
if not exist "dothack-infection-fr.xdelta" (
  echo dothack-infection-fr.xdelta introuvable dans ce dossier.
  echo Telecharge-le dans les Releases du projet et place-le a cote de ce .bat
  echo.
  pause
  exit /b 1
)
set "OUT=%~dp1%~n1 (FR).iso"
echo ISO d'origine : %~1
echo ISO francaise : %OUT%
echo.
echo Patch en cours, ca prend une ou deux minutes...
"%XD%" -d -f -s "%~1" "dothack-infection-fr.xdelta" "%OUT%"
if errorlevel 1 (
  echo.
  echo ECHEC. Verifie que ton ISO est bien la version USA ^(SLUS-202.67^) non modifiee.
  echo.
  pause
  exit /b 1
)
echo.
echo Termine ! Lance "%OUT%" dans PCSX2.
echo L'ISO d'origine n'a pas ete modifiee.
echo.
pause

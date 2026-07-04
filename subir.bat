@echo off
REM Uso: subir.bat "mensaje del commit"
if "%~1"=="" (
    echo ERROR: falta el mensaje. Uso: subir.bat "mensaje del commit"
    exit /b 1
)

git checkout develop || exit /b 1
git pull origin develop || exit /b 1

echo.
echo === Ficheros que se van a subir ===
git status --short
echo.
set /p CONFIRma="Confirmas subir estos cambios? (s/n): "
if /i not "%CONFIRma%"=="s" (
    echo Cancelado.
    exit /b 0
)

git add .
git commit -m "%~1" || exit /b 1
git push origin develop || exit /b 1
echo.
echo === Subido a develop ===
@echo off
echo ==========================================
echo   Installation der Checklisten Anwendung
echo ==========================================
echo.

REM 1. Prüfen ob Git installiert ist
git --version >nul 2>&1
if errorlevel 1 (
    echo Git ist nicht installiert!
    echo Bitte Git von https://git-scm.com/download/win installieren.
    pause
    exit /b 1
)

REM 2. Prüfen ob Python installiert ist
python --version >nul 2>&1
if errorlevel 1 (
    echo Python ist nicht installiert!
    echo Bitte Python 3.10 oder hoeher installieren: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 3. Repository clonen
echo Lade Projekt von GitHub herunter...
if exist Checklisten (
    echo Ordner "Checklisten" existiert bereits. Loesche alten Stand...
    rmdir /s /q Checklisten
)
git clone https://github.com/Patitobi/Checklisten.git

REM 4. In Projektordner wechseln
cd Checklisten

REM 5. Virtuelle Umgebung anlegen
echo Erstelle virtuelle Umgebung...
python -m venv venv

REM 6. Virtuelle Umgebung aktivieren
call venv\Scripts\activate

REM 7. Flask installieren
echo Installiere Flask...
pip install --upgrade pip
pip install flask

REM 8. Datenordner vorbereiten
if not exist localSave mkdir localSave
if not exist localSave\savedChecklist mkdir localSave\savedChecklist

echo.
echo ==========================================
echo Installation abgeschlossen!
echo Starte den Server mit: server_start.bat
echo ==========================================
pause

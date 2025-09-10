@echo off
REM Wechselt ins Projektverzeichnis
cd /d ../../

REM Aktiviert die virtuelle Umgebung
call venv\Scripts\activate

REM Startet den Flask-Server
python app.py

REM Konsole offen halten (optional)
pause

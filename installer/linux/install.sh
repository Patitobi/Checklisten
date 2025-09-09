#!/bin/bash
echo "=========================================="
echo "   Installation der Checklisten Anwendung"
echo "=========================================="
echo

# 1. Prüfen ob git installiert ist
if ! command -v git &> /dev/null
then
    echo "Fehler: git ist nicht installiert!"
    echo "Bitte installiere es mit: sudo apt install git"
    exit 1
fi

# 2. Prüfen ob python3 installiert ist
if ! command -v python3 &> /dev/null
then
    echo "Fehler: Python3 ist nicht installiert!"
    echo "Bitte installiere es mit: sudo apt install python3 python3-venv"
    exit 1
fi

# 3. Repo klonen
if [ -d "Checklisten" ]; then
    echo "Alter Projektordner gefunden – wird gelöscht..."
    rm -rf Checklisten
fi
echo "Lade Projekt von GitHub..."
git clone https://github.com/Patitobi/Checklisten.git

# 4. Virtuelle Umgebung anlegen
cd Checklisten || exit
echo "Erstelle virtuelle Umgebung..."
python3 -m venv venv

# 5. Virtuelle Umgebung aktivieren & Pakete installieren
echo "Installiere Flask..."
source venv/bin/activate
pip install --upgrade pip
pip install flask

# 6. Datenordner vorbereiten
mkdir -p localSave/savedChecklist

echo
echo "=========================================="
echo " Installation abgeschlossen! "
echo " Starte den Server mit: ./start.sh "
echo "=========================================="

#!/bin/bash
cd "$(dirname "$0")" || exit
source venv/bin/activate
python3 app.py
echo "Server gestartet. Drücke STRG+C zum Beenden."
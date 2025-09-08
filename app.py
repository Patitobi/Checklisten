from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__, template_folder="templates")

DATA_FILE = "localSave/checklisten.json"

# Hilfsfunktionen
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# API-Endpunkte
@app.route("/api/checklisten", methods=["GET"])
def get_checklisten():
    return jsonify(load_data())

@app.route("/api/checklisten", methods=["POST"])
def add_checkliste():
    data = load_data()
    new_entry = request.json
    data.append(new_entry)
    save_data(data)
    return jsonify({"status": "ok", "entry": new_entry})

@app.route("/api/checklist/<path>", methods=["GET"])
def get_checklist(path):
    file_path = os.path.join("carTabell", f"{path}.json")
    if not os.path.exists(file_path):
        return jsonify({}), 404
    with open(file_path, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))

@app.route("/api/saveChecklist", methods=["POST"])
def save_checklist():
    data = request.json
    vehicle_path = os.path.join("localSave/savedChecklist", data["path"])
    os.makedirs(vehicle_path, exist_ok=True)

    file_name = f"{data['datum'].replace(':', '-').replace('T', '_')}.json"
    file_path = os.path.join(vehicle_path, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Update the date in checklisten.json (only the date part)
    checklisten = load_data()
    for entry in checklisten:
        if entry["path"] == data["path"]:
            entry["datum"] = data["datum"].split("T")[0]  # Extract only the date
            break
    save_data(checklisten)

    return jsonify({"status": "ok", "file": file_path})

# Webseite ausliefern
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/displayChecklist.html")
def display_checklist():
    return render_template("displayChecklist.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=false)

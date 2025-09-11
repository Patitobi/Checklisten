from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__, template_folder="templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "localSave/checklisten.json")


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
    file_path = os.path.join(BASE_DIR, "carTabell", f"{path}.json")
    if not os.path.exists(file_path):
        return jsonify({}), 404
    with open(file_path, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))

@app.route("/api/saveChecklist", methods=["POST"])
def save_checklist():
    data = request.json
    vehicle_path = os.path.join(BASE_DIR, "localSave/savedChecklist", data["path"])
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

@app.route("/api/viewChecklist/<path>", methods=["GET"])
def view_checklist(path):
    file_path = os.path.join(BASE_DIR, "localSave/savedChecklist", path)
    if not os.path.exists(file_path):
        return jsonify({"error": "Checkliste nicht gefunden"}), 404

    checklist_files = [f for f in os.listdir(file_path) if f.endswith(".json")]
    checklist_data = []
    for file_name in checklist_files:
        with open(os.path.join(file_path, file_name), "r", encoding="utf-8") as f:
            checklist_data.append(json.load(f))

    return jsonify(checklist_data)

@app.route("/api/detailsChecklist/<path>", methods=["GET"])
def details_checklist(path):
    file_path = os.path.join(BASE_DIR, "localSave/savedChecklist", f"{path}.json")
    if not os.path.exists(file_path):
        return jsonify({"error": "Checkliste nicht gefunden"}), 404

    with open(file_path, "r", encoding="utf-8") as f:
        checklist_data = json.load(f)

    return jsonify(checklist_data)

# Webseite ausliefern
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/displayChecklist.html")
def display_checklist():
    return render_template("displayChecklist.html")

@app.route("/viewChecklist.html")
def view_checklist_page():
    return render_template("viewChecklist.html")

@app.route("/detailsChecklist.html")
def details_Checklist_page():
    return render_template("detailsChecklist.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

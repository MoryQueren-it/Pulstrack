import json
import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DATA_FILE = 'data.json'

DEFAULT_HABITS = [
    {"id": "sport", "name": "Sport & Mouvement", "icon": "fi-rr-gym", "target": 5},
    {"id": "lecture", "name": "Lecture (30 min)", "icon": "fi-rr-book-open-cover", "target": 7},
    {"id": "hydratation", "name": "Hydratation (2L)", "icon": "fi-rr-glass-water", "target": 7},
    {"id": "sommeil", "name": "Sommeil (7h30+)", "icon": "fi-rr-moon-stars", "target": 6},
    {"id": "projets", "name": "Projets Persos", "icon": "fi-rr-laptop-code", "target": 5}
]


def generate_sample_logs():
    today = datetime.now().date()
    sample_logs = {}
    for i in range(1, 15):
        d_str = (today - timedelta(days=i)).isoformat()
        sample_logs[d_str] = []
        if i % 2 == 0 or i < 5:
            sample_logs[d_str].extend(["sport", "hydratation", "sommeil"])
        if i % 3 != 0:
            sample_logs[d_str].extend(["lecture", "projets"])
    return sample_logs


def load_data():
    if not os.path.exists(DATA_FILE):
        initial_data = {
            "habits": DEFAULT_HABITS,
            "logs": generate_sample_logs()
        }
        save_data(initial_data)
        return initial_data

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        if not content:
            initial_data = {
                "habits": DEFAULT_HABITS,
                "logs": generate_sample_logs()
            }
            save_data(initial_data)
            return initial_data
        data = json.loads(content)

    updated = False
    if not data.get("habits"):
        data["habits"] = list(DEFAULT_HABITS)
        updated = True

    if "logs" not in data or not isinstance(data["logs"], dict):
        data["logs"] = generate_sample_logs()
        updated = True

    if updated:
        save_data(data)

    return data


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def calculate_stats(data):
    habits = data.get("habits", [])
    logs = data.get("logs", {})
    today = datetime.now().date()

    streaks = {}
    for h in habits:
        hid = h["id"]
        current_streak = 0
        check_date = today

        if hid not in logs.get(check_date.isoformat(), []):
            check_date -= timedelta(days=1)

        while hid in logs.get(check_date.isoformat(), []):
            current_streak += 1
            check_date -= timedelta(days=1)

        streaks[hid] = current_streak

    best_week = {
        "start": None,
        "end": None,
        "completed": 0,
        "possible": 0,
        "rate": 0,
        "top_habit": "Aucune"
    }

    total_habits = len(habits) if habits else 1
    current_monday = today - timedelta(days=today.weekday())

    for w in range(12):
        w_start = current_monday - timedelta(weeks=w)
        w_end = w_start + timedelta(days=6)
        completed_count = 0
        habit_counts = {h["name"]: 0 for h in habits}

        for d in range(7):
            day_str = (w_start + timedelta(days=d)).isoformat()
            day_logs = logs.get(day_str, [])
            completed_count += len(day_logs)
            for h in habits:
                if h["id"] in day_logs:
                    habit_counts[h["name"]] += 1

        possible_count = total_habits * 7
        rate = round((completed_count / possible_count) * 100) if possible_count > 0 else 0

        if completed_count >= best_week["completed"] and completed_count > 0:
            top_h = max(habit_counts, key=habit_counts.get) if habit_counts else "Aucune"
            best_week = {
                "start": w_start.strftime("%d/%m"),
                "end": w_end.strftime("%d/%m"),
                "completed": completed_count,
                "possible": possible_count,
                "rate": rate,
                "top_habit": top_h
            }

    return {
        "streaks": streaks,
        "best_week": best_week,
        "global_streak": max(streaks.values()) if streaks else 0
    }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/state', methods=['GET'])
def get_state():
    data = load_data()
    stats = calculate_stats(data)
    return jsonify({
        "habits": data["habits"],
        "logs": data["logs"],
        "stats": stats,
        "today": datetime.now().date().isoformat()
    })


@app.route('/api/toggle', methods=['POST'])
def toggle_habit():
    req = request.json or {}
    date_str = req.get('date')
    habit_id = req.get('habit_id')

    if not date_str or not habit_id:
        return jsonify({"error": "date et habit_id requis"}), 400

    data = load_data()
    if date_str not in data["logs"]:
        data["logs"][date_str] = []

    if habit_id in data["logs"][date_str]:
        data["logs"][date_str].remove(habit_id)
    else:
        data["logs"][date_str].append(habit_id)

    save_data(data)
    return jsonify({"status": "ok", "stats": calculate_stats(data), "logs": data["logs"]})


@app.route('/api/habits', methods=['POST'])
def add_habit():
    req = request.json or {}
    name = req.get('name', '').strip()
    icon = req.get('icon', 'fi-rr-check').strip()

    if not name:
        return jsonify({"error": "Nom requis"}), 400

    data = load_data()
    habit_id = name.lower().replace(" ", "_") + "_" + str(int(datetime.now().timestamp()))[-4:]
    new_habit = {
        "id": habit_id,
        "name": name,
        "icon": icon if icon.startswith("fi-") else f"fi-rr-{icon}",
        "target": 7
    }
    data["habits"].append(new_habit)
    save_data(data)
    return jsonify({"status": "ok", "habit": new_habit})


@app.route('/api/habits/<habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    data = load_data()
    data["habits"] = [h for h in data["habits"] if h["id"] != habit_id]
    for d in data["logs"]:
        if habit_id in data["logs"][d]:
            data["logs"][d].remove(habit_id)
    save_data(data)
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
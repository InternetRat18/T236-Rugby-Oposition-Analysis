from pathlib import Path
import sqlite3
from flask import Flask, jsonify, request
from analysis import get_dashboard_analysis

ROOT = Path(__file__).resolve().parent
DATABASE = ROOT / "MainDB.db"
app = Flask(__name__, static_folder="dashboard UI and filter", static_url_path="")

def connect_db():
    if not DATABASE.exists():
        return None
    connection = sqlite3.connect(str(DATABASE))
    connection.row_factory = sqlite3.Row
    return connection

def get_events():
    connection = connect_db()
    if connection is None:
        return None, (jsonify({"error": "Database not found. Run ExtractData.py and import the match CSV first."}), 404)
    try:
        tables = {r["name"] for r in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        if "AllData" not in tables:
            return None, (jsonify({"error": "The database exists but does not contain the AllData table. Import the match CSV first."}), 404)
        rows = [dict(row) for row in connection.execute('SELECT * FROM "AllData"')]
        return rows, None
    finally:
        connection.close()

@app.get("/")
def index():
    return app.send_static_file("index.html")

@app.get("/api/events")
def events():
    rows, error = get_events()
    if error:
        return error
    filters = {
        "teamId": request.args.get("teamId", ""),
        "playerId": request.args.get("playerId", ""),
        "actionId": request.args.get("actionId", ""),
        "period": request.args.get("period", ""),
    }
    if any(filters.values()):
        from analysis import _match_rows
        rows = _match_rows(rows, filters)
    return jsonify({"count": len(rows), "events": rows})

@app.post("/api/analysis")
def analysis():
    payload = request.get_json(silent=True) or {}
    filters = payload.get("filters") or {}
    rows, error = get_events()
    if error:
        return error
    from analysis import _match_rows
    filtered = _match_rows(rows, filters)
    return jsonify(get_dashboard_analysis(filtered))

if __name__ == "__main__":
    app.run()

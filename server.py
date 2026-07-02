"""
Progress Tracker — local Flask server
Serves the progress-tracker.html page and handles JSON read/write.
Usage:
    python server.py [--port PORT]

Default port: 5050 (avoid common dev ports like 5000)
After launch, opens http://127.0.0.1:5050/ in default browser.
"""
import argparse
import json
import sys
import webbrowser
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "progress.json"

app = Flask(__name__, static_folder=str(BASE_DIR))


@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "progress-tracker.html")


@app.route("/progress-tracker.html")
def tracker_html():
    return send_from_directory(BASE_DIR, "progress-tracker.html")


@app.route("/progress.json")
def get_progress():
    if not JSON_PATH.exists():
        return jsonify({"updatedAt": "", "projects": []}), 200
    try:
        with JSON_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data), 200
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON: {e}"}), 500


@app.route("/save", methods=["POST"])
def save_progress():
    payload = request.get_json(silent=True)
    if not payload or "projects" not in payload:
        return jsonify({"error": "Missing 'projects' field"}), 400

    new_data = {
        "updatedAt": payload.get("updatedAt") or "",
        "projects": payload["projects"],
    }

    try:
        with JSON_PATH.open("w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)
            f.write("\n")
    except OSError as e:
        return jsonify({"error": f"Write failed: {e}"}), 500

    return jsonify({"ok": True, "updatedAt": new_data["updatedAt"]}), 200


@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "Not found"}), 404


def main():
    parser = argparse.ArgumentParser(description="Progress Tracker local server")
    parser.add_argument("--port", type=int, default=5050, help="Port (default 5050)")
    parser.add_argument("--no-open", action="store_true", help="Skip auto-open browser")
    args = parser.parse_args()

    if not JSON_PATH.exists():
        print(f"[WARN] {JSON_PATH.name} not found — creating empty one")
        JSON_PATH.write_text(json.dumps({"updatedAt": "", "projects": []}, indent=2), encoding="utf-8")

    url = f"http://127.0.0.1:{args.port}/"
    print(f"[INFO] Progress Tracker running at {url}")
    print(f"[INFO] JSON path: {JSON_PATH}")

    if not args.no_open:
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"[WARN] Could not auto-open browser: {e}")

    try:
        app.run(host="127.0.0.1", port=args.port, debug=False, use_reloader=False)
    except OSError as e:
        if e.errno == 10048 or "address already in use" in str(e).lower():
            print(f"[ERROR] Port {args.port} busy. Try --port <other>")
            sys.exit(1)
        raise


if __name__ == "__main__":
    main()

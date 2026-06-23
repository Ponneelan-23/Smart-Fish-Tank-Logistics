from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

from fish_tank_model import (
    read_latest_data,
    read_history,
    get_dashboard_summary
)

# ======================================================
# Flask Setup
# ======================================================

app = Flask(__name__)
CORS(app)

# ======================================================
# Frontend Path
# ======================================================

BASE_DIR = os.path.dirname(__file__)

FRONTEND_FOLDER = os.path.join(
    BASE_DIR,
    "..",
    "frontend"
)

CSS_FOLDER = os.path.join(
    FRONTEND_FOLDER,
    "css"
)

JS_FOLDER = os.path.join(
    FRONTEND_FOLDER,
    "js"
)

ASSETS_FOLDER = os.path.join(
    FRONTEND_FOLDER,
    "assets"
)

# ======================================================
# Frontend Routes
# ======================================================

@app.route("/")
def home():
    return send_from_directory(
        FRONTEND_FOLDER,
        "index.html"
    )


@app.route("/css/<path:filename>")
def serve_css(filename):
    return send_from_directory(
        CSS_FOLDER,
        filename
    )


@app.route("/js/<path:filename>")
def serve_js(filename):
    return send_from_directory(
        JS_FOLDER,
        filename
    )


@app.route("/assets/<path:filename>")
def serve_assets(filename):
    return send_from_directory(
        ASSETS_FOLDER,
        filename
    )

# ======================================================
# API Routes
# ======================================================

@app.route("/api/latest")
def api_latest():

    data = read_latest_data()

    if data is None:

        return jsonify({
            "success": False,
            "message": "No sensor data available"
        })

    return jsonify({
        "success": True,
        "data": data
    })


@app.route("/api/history")
def api_history():

    history = read_history()

    return jsonify({
        "success": True,
        "count": len(history),
        "data": history
    })


@app.route("/api/dashboard")
def api_dashboard():

    dashboard = get_dashboard_summary()

    if dashboard is None:

        return jsonify({
            "success": False,
            "message": "No dashboard data available"
        })

    return jsonify({
        "success": True,
        "data": dashboard
    })

# ======================================================
# Health Check
# ======================================================

@app.route("/api/status")
def api_status():

    return jsonify({
        "success": True,
        "system": "Fish Tank Logistics",
        "mqtt": "Connected via mqtt_listener.py",
        "database": "CSV Storage",
        "version": "1.1"
    })

# ======================================================
# Run Server
# ======================================================

if __name__ == "__main__":

    print("\n====================================")
    print("Fish Tank Logistics Backend Started")
    print("====================================")
    print("Frontend : http://127.0.0.1:5000")
    print("Latest   : http://127.0.0.1:5000/api/latest")
    print("History  : http://127.0.0.1:5000/api/history")
    print("Status   : http://127.0.0.1:5000/api/status")
    print("====================================\n")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
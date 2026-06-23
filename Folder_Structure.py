import os

base_path = r"D:\COLLEGE\Power House\Projects\Fish Tank Logistics\Web_Fish_Log"

folders = [
    "backend",
    "frontend",
    "frontend/css",
    "frontend/js",
    "frontend/assets",
    "frontend/assets/icons",
    "data"
]

files = [
    "backend/app.py",
    "backend/mqtt_listener.py",
    "backend/fish_tank_model.py",
    "backend/requirements.txt",

    "frontend/index.html",
    "frontend/css/style.css",
    "frontend/js/app.js",

    "data/sensor_data.csv",

    "README.md"
]

for folder in folders:
    os.makedirs(os.path.join(base_path, folder), exist_ok=True)

for file in files:
    filepath = os.path.join(base_path, file)

    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            pass

print("✅ Fish Tank Logistics project structure created successfully!")

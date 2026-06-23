import pandas as pd
import os

# ======================================================
# CSV File Path
# ======================================================

CSV_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "sensor_data.csv"
)

# ======================================================
# Tank Status Logic
# ======================================================

def get_tank_status(
    temperature,
    turbidity,
    water_level
):
    try:

        # Critical Conditions

        if temperature < 20 or temperature > 35:
            return "Critical"

        if turbidity > 700:
            return "Critical"

        if water_level < 20:
            return "Critical"

        # Warning Conditions

        if turbidity > 400:
            return "Warning"

        if water_level < 40:
            return "Warning"

        return "Healthy"

    except:
        return "Unknown"


# ======================================================
# Latest Sensor Data
# ======================================================

def read_latest_data():

    try:

        if not os.path.exists(CSV_FILE):
            return None

        df = pd.read_csv(CSV_FILE)

        if df.empty:
            return None

        latest = df.iloc[-1]

        temperature = float(latest["temperature"])
        turbidity = float(latest["turbidity_ntu"])
        water_level = float(latest["water_level_percent"])

        status = get_tank_status(
            temperature,
            turbidity,
            water_level
        )

        return {
            "timestamp": str(latest["timestamp"]),

            "temperature": round(temperature, 2),

            "turbidity": round(
                turbidity,
                2
            ),

            "water_level": round(
                water_level,
                1
            ),

            "ph": None,

            "do": None,

            "status": status
        }

    except Exception as e:

        print(
            "Latest Data Error:",
            e
        )

        return None


# ======================================================
# Historical Data
# ======================================================

def read_history(limit=50):

    try:

        if not os.path.exists(CSV_FILE):
            return []

        df = pd.read_csv(CSV_FILE)

        if df.empty:
            return []

        df = df.tail(limit)

        history = []

        for _, row in df.iterrows():

            history.append({

                "timestamp":
                    str(row["timestamp"]),

                "temperature":
                    float(row["temperature"]),

                "turbidity":
                    float(row["turbidity_ntu"]),

                "water_level":
                    float(row["water_level_percent"])
            })

        return history

    except Exception as e:

        print(
            "History Error:",
            e
        )

        return []


# ======================================================
# Dashboard Summary (Optional)
# ======================================================

def get_dashboard_summary():

    latest = read_latest_data()

    if latest is None:
        return None

    return {

        "temperature":
            latest["temperature"],

        "turbidity":
            latest["turbidity"],

        "water_level":
            latest["water_level"],

        "ph":
            latest["ph"],

        "do":
            latest["do"],

        "status":
            latest["status"],

        "timestamp":
            latest["timestamp"]
    }
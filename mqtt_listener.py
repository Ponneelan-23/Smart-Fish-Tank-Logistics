import json
import csv
import os
from datetime import datetime
import paho.mqtt.client as mqtt

# ======================================================
# MQTT Configuration
# ======================================================

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "tce/ponneelan/temp"

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
# Create CSV Header if Missing
# ======================================================

def initialize_csv():

    if not os.path.exists(CSV_FILE):

        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "timestamp",
                "temperature",
                "turbidity_raw",
                "turbidity_voltage",
                "turbidity_ntu",
                "water_distance_cm",
                "water_level_cm",
                "water_level_percent",
                "ph",
                "do"
            ])

        print("CSV file created with headers")


# ======================================================
# Save Data to CSV
# ======================================================

def save_to_csv(data):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    row = [
        timestamp,

        data.get("temperature"),

        data.get("turbidity_raw"),
        data.get("turbidity_voltage"),
        data.get("turbidity_ntu"),

        data.get("water_distance_cm"),
        data.get("water_level_cm"),
        data.get("water_level_percent"),

        None,   # Future pH Sensor
        None    # Future DO Sensor
    ]

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)
        writer.writerow(row)

    print("\nSaved to CSV:")
    print(row)


# ======================================================
# MQTT Callbacks
# ======================================================

def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("\nConnected to MQTT Broker")
        print("Subscribed to:", TOPIC)

        client.subscribe(TOPIC)

    else:

        print("Connection Failed:", rc)


def on_message(client, userdata, msg):

    try:

        payload = msg.payload.decode()

        print("\n===================================")
        print("MQTT Message Received")
        print("===================================")
        print(payload)

        data = json.loads(payload)

        print("\nParsed Data")
        print("Temperature        :", data.get("temperature"))
        print("Turbidity Raw      :", data.get("turbidity_raw"))
        print("Turbidity Voltage  :", data.get("turbidity_voltage"))
        print("Turbidity NTU      :", data.get("turbidity_ntu"))
        print("Distance (cm)      :", data.get("water_distance_cm"))
        print("Water Level (cm)   :", data.get("water_level_cm"))
        print("Water Level (%)    :", data.get("water_level_percent"))

        save_to_csv(data)

    except Exception as e:

        print("\nError Processing MQTT Message")
        print(e)


# ======================================================
# Main
# ======================================================

initialize_csv()

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

print("===================================")
print("Fish Tank MQTT Listener Started")
print("===================================")
print("Broker :", BROKER)
print("Topic  :", TOPIC)
print("===================================")

client.connect(BROKER, PORT, 60)

client.loop_forever()
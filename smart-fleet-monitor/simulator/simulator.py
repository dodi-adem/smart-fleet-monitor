import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

# --- Configuration -------------------------------------------
MQTT_BROKER = "fleet_mosquitto"
MQTT_PORT   = 1883

CARS = ["CAR_01", "CAR_02", "CAR_03", "CAR_04", "CAR_05"]

# Starting positions around Messina, Sicily
BASE_POSITIONS = {
    "CAR_01": {"lat": 38.1157, "lon": 15.6441},
    "CAR_02": {"lat": 38.1200, "lon": 15.6500},
    "CAR_03": {"lat": 38.1100, "lon": 15.6400},
    "CAR_04": {"lat": 38.1250, "lon": 15.6350},
    "CAR_05": {"lat": 38.1080, "lon": 15.6480},
}

# --- Location Publisher --------------------------------------
def publish_location(client, car_id, position):
    position["lat"] += random.uniform(-0.001, 0.001)
    position["lon"] += random.uniform(-0.001, 0.001)

    payload = {
        "car_id":    car_id,
        "timestamp": datetime.now().isoformat(),
        "lat":       round(position["lat"], 6),
        "lon":       round(position["lon"], 6),
        "speed_kmh": round(random.uniform(20, 120), 1),
        "heading":   round(random.uniform(0, 360), 1)
    }

    topic = f"fleet/{car_id}/location"
    client.publish(topic, json.dumps(payload))
    print(f"[LOCATION] {car_id} → lat: {payload['lat']}, lon: {payload['lon']}, speed: {payload['speed_kmh']} km/h")

# --- Fuel Publisher ------------------------------------------
def publish_fuel(client, car_id, fuel_state):
    fuel_state["level"] -= random.uniform(0.01, 0.05)
    fuel_state["level"]  = max(0, fuel_state["level"])

    payload = {
        "car_id":           car_id,
        "timestamp":        datetime.now().isoformat(),
        "fuel_level_pct":   round(fuel_state["level"], 2),
        "consumption_rate": round(random.uniform(5.0, 12.0), 2)
    }

    topic = f"fleet/{car_id}/fuel"
    client.publish(topic, json.dumps(payload))
    print(f"[FUEL]     {car_id} → level: {payload['fuel_level_pct']}%, consumption: {payload['consumption_rate']} L/100km")

# --- Engine Publisher ----------------------------------------
def publish_engine(client, car_id):
    payload = {
        "car_id":    car_id,
        "timestamp": datetime.now().isoformat(),
        "rpm":       round(random.uniform(800, 4000), 0),
        "status":    "running"
    }

    topic = f"fleet/{car_id}/engine"
    client.publish(topic, json.dumps(payload))
    print(f"[ENGINE]   {car_id} → rpm: {payload['rpm']}")

# --- Main ----------------------------------------------------
if __name__ == "__main__":
    client = mqtt.Client(client_id="fleet_simulator")
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()

    print("Smart Fleet Simulator Starting...")
    print(f"   Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    print(f"   Simulating {len(CARS)} cars\n")

    positions   = {car_id: BASE_POSITIONS[car_id].copy() for car_id in CARS}
    fuel_states = {car_id: {"level": random.uniform(50, 100)} for car_id in CARS}
    tick = 0

    try:
        while True:
            print(f"\n--- Tick {tick} ---")
            for car_id in CARS:
                publish_location(client, car_id, positions[car_id])
                publish_fuel(client, car_id, fuel_states[car_id])
                publish_engine(client, car_id)
                time.sleep(3)
            tick += 1

    except KeyboardInterrupt:
        print("\nSimulator stopped.")
        client.disconnect()
# --- MongoDB Handler -----------------------------------------

def store_location(mongo_db, payload):
    collection = mongo_db["location_telemetry"]
    document = {
        "car_id":    payload["car_id"],
        "timestamp": payload["timestamp"],
        "lat":       payload["lat"],
        "lon":       payload["lon"],
        "speed_kmh": payload["speed_kmh"],
        "heading":   payload["heading"]
    }
    collection.insert_one(document)
    print(f"[MONGO] Location stored for {payload['car_id']}")

def store_engine(mongo_db, payload):
    collection = mongo_db["engine_telemetry"]
    document = {
        "car_id":    payload["car_id"],
        "timestamp": payload["timestamp"],
        "rpm":       payload["rpm"],
        "status":    payload["status"]
    }
    collection.insert_one(document)
    print(f"[MONGO] Engine stored for {payload['car_id']}")

import paho.mqtt.client as mqtt
import json
import time
import pymysql
import pymongo
from neo4j import GraphDatabase
from datetime import datetime

from handlers.mongo_handler import store_location, store_engine
from handlers.mysql_handler import store_fuel_log, store_trip
from handlers.neo4j_handler import store_location_node

# --- Configuration -------------------------------------------
MQTT_BROKER = "fleet_mosquitto"
MQTT_PORT   = 1883

# MySQL
MYSQL_HOST  = "fleet_mysql"
MYSQL_PORT     = 3306
MYSQL_USER     = "fleetuser"
MYSQL_PASSWORD = "fleetpass"
MYSQL_DB       = "fleet_db"

# MongoDB
MONGO_URI   = "mongodb://fleetuser:fleetpass@fleet_mongo:27017/?authSource=admin"
MONGO_DB  = "fleet_telemetry"

# Neo4j
NEO4J_URI   = "bolt://fleet_neo4j:7687"
NEO4J_USER     = "neo4j"
NEO4J_PASSWORD = "fleetpass"

# --- Database Connections ------------------------------------
def connect_mysql():
    return pymysql.connect(
        host        = MYSQL_HOST,
        port        = MYSQL_PORT,
        user        = MYSQL_USER,
        password    = MYSQL_PASSWORD,
        database    = MYSQL_DB,
        cursorclass = pymysql.cursors.DictCursor
    )

def connect_mongo():
    client = pymongo.MongoClient(MONGO_URI)
    return client[MONGO_DB]

def connect_neo4j():
    return GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD)
    )
    
    
# --- MQTT Callbacks ------------------------------------------
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("[MQTT] Connected to broker")
        client.subscribe("fleet/#")
        print("[MQTT] Subscribed to fleet/#")
    else:
        print(f"[MQTT] Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        topic   = msg.topic

        print(f"[MQTT] Received message on topic: {topic}")

        if "/location" in topic:
            store_location(userdata["mongo"], payload)
            store_location_node(userdata["neo4j"], payload)

        elif "/fuel" in topic:
            store_fuel_log(userdata["mysql"], payload)

        elif "/engine" in topic:
            store_engine(userdata["mongo"], payload)
        time.sleep(3)

    except Exception as e:
        print(f"[MQTT] Error processing message: {e}")
        
# --- Main ----------------------------------------------------
if __name__ == "__main__":
    print("Smart Fleet Subscriber Starting...")

    # Connect to all three databases
    mysql_conn   = connect_mysql()
    mongo_db     = connect_mongo()
    neo4j_driver = connect_neo4j()

    print("[DB] Connected to MySQL")
    print("[DB] Connected to MongoDB")
    print("[DB] Connected to Neo4j")

    # Bundle all connections into userdata
    userdata = {
        "mysql": mysql_conn,
        "mongo": mongo_db,
        "neo4j": neo4j_driver
    }

    # Setup MQTT client
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id = "fleet_subscriber"
    )
    client.user_data_set(userdata)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_forever()
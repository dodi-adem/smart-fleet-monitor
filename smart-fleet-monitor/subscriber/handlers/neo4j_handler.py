# --- Neo4j Handler -------------------------------------------

def get_city_zone(lat):
    if lat > 38.12:
        return "North Messina"
    elif lat < 38.11:
        return "South Messina"
    else:
        return "Central Messina"

def store_location_node(neo4j_driver, payload):
    zone = get_city_zone(payload["lat"])

    with neo4j_driver.session() as session:
        session.run("""
            MERGE (c:Car {car_id: $car_id})

            MERGE (l:Location {
                lat: $lat,
                lon: $lon
            })
            SET l.last_seen = $timestamp

            MERGE (city:City {name: $zone})

            MERGE (c)-[r:PASSED_THROUGH]->(l)
            SET r.speed_kmh  = $speed_kmh,
                r.timestamp  = $timestamp

            MERGE (l)-[:BELONGS_TO]->(city)
        """,
            car_id    = payload["car_id"],
            lat       = round(payload["lat"], 3),
            lon       = round(payload["lon"], 3),
            speed_kmh = payload["speed_kmh"],
            timestamp = payload["timestamp"],
            zone      = zone
        )
        print(f"[NEO4J] Location node stored for {payload['car_id']} in {zone}")
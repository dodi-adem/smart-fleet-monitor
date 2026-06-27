# --- MySQL Handler -------------------------------------------

def store_fuel_log(mysql_conn, payload):
    try:
        with mysql_conn.cursor() as cursor:
            sql = """
                INSERT INTO fuel_logs (car_id, timestamp, fuel_level_pct, consumption_rate)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (
                payload["car_id"],
                payload["timestamp"],
                payload["fuel_level_pct"],
                payload["consumption_rate"]
            ))
        mysql_conn.commit()
        print(f"[MYSQL] Fuel log stored for {payload['car_id']}")
    except Exception as e:
        print(f"[MYSQL] Error storing fuel log: {e}")
        mysql_conn.rollback()

def store_trip(mysql_conn, trip_data):
    try:
        with mysql_conn.cursor() as cursor:
            sql = """
                INSERT INTO trips (trip_id, car_id, start_time, end_time,
                                   distance_km, avg_speed_kmh, fuel_used_liters, efficiency_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                trip_data["trip_id"],
                trip_data["car_id"],
                trip_data["start_time"],
                trip_data["end_time"],
                trip_data["distance_km"],
                trip_data["avg_speed_kmh"],
                trip_data["fuel_used_liters"],
                trip_data["efficiency_score"]
            ))
        mysql_conn.commit()
        print(f"[MYSQL] Trip stored for {trip_data['car_id']}")
    except Exception as e:
        print(f"[MYSQL] Error storing trip: {e}")
        mysql_conn.rollback()

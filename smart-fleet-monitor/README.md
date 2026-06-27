# Smart Fleet Monitor

A real-time fleet tracking system that collects telemetry data from vehicles
via MQTT and stores it across three different databases based on data type.

## Stack

- **Mosquitto** — MQTT broker
- **MySQL** — structured fuel and trip data
- **MongoDB** — raw telemetry storage
- **Neo4j** — route graph analysis
- **Python** — simulator, subscriber, data routing
- **Streamlit** — live dashboard
- **Docker** — full containerization

## Run

```bash
docker compose up -d --build
```

Dashboard available at `http://localhost:8501`

## Stop

```bash
docker compose down
```

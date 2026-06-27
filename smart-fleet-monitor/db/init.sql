CREATE DATABASE IF NOT EXISTS fleet_db;
USE fleet_db;

CREATE TABLE IF NOT EXISTS vehicles (
    car_id VARCHAR(20) PRIMARY KEY,
    model VARCHAR(50) NOT NULL,
    plate VARCHAR(20) NOT NULL,
    year INT NOT NULL
);

CREATE TABLE IF NOT EXISTS trips (
    trip_id VARCHAR(50) PRIMARY KEY,
    car_id VARCHAR(20) NOT NULL,
    start_time DATETIME,
    end_time DATETIME,
    distance_km FLOAT DEFAULT 0,
    avg_speed_kmh FLOAT DEFAULT 0,
    fuel_used_liters FLOAT DEFAULT 0,
    efficiency_score FLOAT DEFAULT 0,
    FOREIGN KEY (car_id) REFERENCES vehicles(car_id)
);

CREATE TABLE IF NOT EXISTS fuel_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    car_id VARCHAR(20) NOT NULL,
    timestamp DATETIME NOT NULL,
    fuel_level_pct FLOAT NOT NULL,
    consumption_rate FLOAT NOT NULL,
    FOREIGN KEY (car_id) REFERENCES vehicles(car_id)
);

INSERT IGNORE INTO vehicles (car_id, model, plate, year) VALUES
    ('CAR_01', 'Fiat Panda',      'ME123AA', 2021),
    ('CAR_02', 'Fiat 500',        'ME456BB', 2020),
    ('CAR_03', 'Lancia Ypsilon',  'ME789CC', 2022),
    ('CAR_04', 'Alfa Romeo Mito', 'ME321DD', 2019),
    ('CAR_05', 'Ford Fiesta',     'ME654EE', 2021);

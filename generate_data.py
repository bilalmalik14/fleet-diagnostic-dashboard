import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta

# Setup
fake = Faker()
conn = sqlite3.connect("fleet_data.db")
cursor = conn.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS vehicle_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id TEXT,
    timestamp TEXT,
    speed REAL,
    fuel_level REAL,
    latitude REAL,
    longitude REAL
)''')

# Simulate 5 vehicles, each with many entries
vehicle_ids = [fake.license_plate() for _ in range(5)]
base_time = datetime.now()

for i in range(1000):
    vehicle_id = random.choice(vehicle_ids)
    timestamp = (base_time + timedelta(minutes=i)).isoformat()
    speed = round(random.uniform(40, 120), 2)
    fuel_level = round(random.uniform(10, 100), 2)
    lat = float(fake.latitude())
    lon = float(fake.longitude())

    cursor.execute(
        "INSERT INTO vehicle_data (vehicle_id, timestamp, speed, fuel_level, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)",
        (vehicle_id, timestamp, speed, fuel_level, lat, lon)
    )

# Finalize
conn.commit()
conn.close()

print("✅ Data generated successfully for 5 vehicles.")

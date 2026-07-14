import psycopg2
import os
from dotenv import load_dotenv

# Read the hidden .env file
load_dotenv()

# Grab the variables
DB_URI = os.getenv("DB_URI")


#SQL Schema commands to build Tables
Create_SQL_Tables = """
CREATE TABLE IF NOT EXISTS Rentals (
    neighborhood_ID SERIAL PRIMARY KEY,
    city VARCHAR(100),
    neighborhood_name VARCHAR(100),
    average_monthly_rent NUMERIC(10,2),
    listing_count INT
);
CREATE TABLE IF NOT EXISTS Workplace_Hubs (
    hub_id SERIAL PRIMARY KEY,
    hub_name VARCHAR (100),
    hub_address VARCHAR (255)
);
CREATE TABLE IF NOT EXISTS CommuteCache (
    neighborhood_id INT REFERENCES Rentals(neighborhood_id),
    hub_id INT REFERENCES Workplace_Hubs(hub_id),
    driving_distance_miles NUMERIC(6, 2),
    driving_time_minutes NUMERIC(6, 2),
    rush_hour_time_minutes NUMERIC(6, 2),
    transit_time_minutes NUMERIC(6, 2),
    estimated_daily_tolls NUMERIC(6, 2),
    PRIMARY KEY (neighborhood_id, hub_id)
);
"""
try:
    #Open connection
    conn=psycopg2.connect(DB_URI)
    cursor = conn.cursor()
    #Execute Table creation script
    cursor.execute(Create_SQL_Tables)
    #Save changes permanently
    conn.commit()
    print("Tables cretead successfully")

    #Clean up connection
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error, Could not connect to database: {e}")
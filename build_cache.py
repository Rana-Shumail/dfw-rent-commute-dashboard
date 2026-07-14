import psycopg2
import googlemaps
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Pull the variables into your script
DB_URI = os.getenv("DB_URI")
GOOGLE_KEY = os.getenv("GOOGLE_MAPS_KEY")


gmaps = googlemaps.Client(key=GOOGLE_KEY)

# Connect to the database
conn = psycopg2.connect(DB_URI)
cursor = conn.cursor()

# Pull all our saved neighborhoods and hubs out of the database
cursor.execute("SELECT neighborhood_id, neighborhood_name, city FROM Rentals;")
neighborhoods = cursor.fetchall() # This gets a list of all 8 places

cursor.execute("SELECT hub_id, hub_name, hub_address FROM Workplace_Hubs;")
hubs = cursor.fetchall() # This gets a list of all 5 hubs

#  Use nested loops to pair every neighborhood with every hub automatically
for rent_id, rent_name, city in neighborhoods:
    for hub_id, hub_name, hub_addr in hubs:
        
        # Combine the neighborhood name and city for Google (e.g., "Deep Ellum, Dallas, TX")
        origin_address = f"{rent_name}, {city}, TX"
        destination_address = hub_addr
        
        print(f"Calculating: {origin_address} -> {hub_name}")
        
        # Ask Google for the driving data
        response = gmaps.distance_matrix(
            origins=origin_address,
            destinations=destination_address,
            mode="driving"
        )
        
        #  Extract the math numbers
        meters = response['rows'][0]['elements'][0]['distance']['value']
        miles = meters / 1609.34
        
        seconds = response['rows'][0]['elements'][0]['duration']['value']
        minutes = seconds / 60
        
        # Save this specific pair to the database
        cursor.execute("""
            INSERT INTO CommuteCache (neighborhood_id, hub_id, driving_distance_miles, driving_time_minutes)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (neighborhood_id, hub_id) DO NOTHING;
        """, (rent_id, hub_id, miles, minutes))
        
        # Pause for half a second so we don't overwhelm the API
        time.sleep(0.5)

#  Save everything and close
conn.commit()
cursor.close()
conn.close()

print("All 40 commute combinations have been successfully calculated and saved!")
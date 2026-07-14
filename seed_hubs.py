import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

# Grab the variables
DB_URI = os.getenv("DB_URI")

# Core workplace hubs in DFW
HUBS = [
    ("Downtown Dallas", "1500 Marilla St, Dallas, TX 75201"),
    ("Legacy West (Plano)", "5908 Headquarters Dr, Plano, TX 75024"),
    ("Las Colinas (Irving)", "220 E Las Colinas Blvd, Irving, TX 75039"),
    ("Frisco North Tollway Corridor", "6101 Frisco Square Blvd, Frisco, TX 75034"),
    ("Downtown Fort Worth", "200 Texas St, Fort Worth, TX 76102")
]

try:
    conn = psycopg2.connect(DB_URI)
    cursor = conn.cursor()

    #loop through each hub and insert into Workplace_Hubs table
    for name, address in HUBS:
        # %s to prevent sql injecetion attacks
        cursor.execute(
            "INSERT INTO Workplace_Hubs (hub_name, hub_address) VALUES (%s, %s);",
            (name,address)
        )
    conn.commit()
    print("Workplace hubs seeded!")

    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error Seeding : {e}")

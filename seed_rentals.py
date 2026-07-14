import psycopg2
import os
from dotenv import load_dotenv

# Read the hidden .env file
load_dotenv()

#  Grab the variables
DB_URI = os.getenv("DB_URI")

#Neighborhood rent baseline DFW
RENTAL_DATA = [
    # (City, Neighborhood Name, Avg Monthly Rent, Sample Size/Listing Count)
    ("Dallas", "Deep Ellum", 1850.00, 45),
    ("Dallas", "Uptown", 2300.00, 60),
    ("Plano", "Legacy West Area", 2100.00, 35),
    ("Frisco", "Frisco Square Area", 1950.00, 40),
    ("Irving", "Las Colinas Urban Center", 1800.00, 50),
    ("Denton", "Downtown Denton", 1350.00, 25),
    ("Fort Worth", "Downtown Fort Worth", 1750.00, 30),
    ("Arlington", "UTA / Downtown Arlington", 1250.00, 20)
]

try:
    conn =psycopg2.connect(DB_URI)
    cursor = conn.cursor()

    #Loop and execute database insertion
    for city,neighborhood,rent,count in RENTAL_DATA:
        cursor.execute(
        """INSERT INTO Rentals (city,neighborhood_name,average_monthly_rent,listing_count)
        VALUES (%s,%s,%s,%s);""",
        (city,neighborhood,rent,count)
        )
    conn.commit()
    print("Rental data seeded successfully!")
    cursor.close()
    conn.close()

except Exception as e:
    print(f"Error seeding: {e}")
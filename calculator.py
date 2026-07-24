import psycopg2
import googlemaps
import os
from dotenv import load_dotenv

#Read env file
load_dotenv()

#Pull the variables
DB_URI = os.getenv("DB_URI")
GOOGLE_KEY = os.getenv("GOOGLE_MAPS_KEY")

#Connect to DataBase
conn = psycopg2.connect(DB_URI)
cursor = conn.cursor()

#Join Rental and commutecache for hub id
target_hub_id = 1 #For Dallas (For testing)

query = """
SELECT
    rentals.neighborhood_name,
    rentals.city,
    rentals.average_monthly_rent,
    commutecache.driving_distance_miles,
    commutecache.driving_time_minutes
FROM
    Rentals
INNER JOIN
    commutecache ON rentals.neighborhood_id = commutecache.neighborhood_id
WHERE
    commutecache.hub_id = %s;
"""
#Execute the query
cursor.execute(query,[target_hub_id])
#Fetch matching rows
rows =cursor.fetchall()

def normalized_list(numbers):
    #Convert all numbers to float
    float_nums = [float(n) for n in numbers]

    minimum = min(float_nums)
    maximum = max(float_nums)

    #Avoid zero devision error
    if maximum==minimum:
        return [0.0 for _ in float_nums]

    #Calculate normalized values
    normalized = []
    for value in float_nums:
        norm_value = (value-minimum)/(maximum-minimum)
        normalized.append(norm_value)

    return normalized


#Extract rent and commute lists from SQL results
rents  = [row[2] for row in rows]
commutes = [row[4] for row in rows]

#Normalize both feature sets
norm_rents = normalized_list(rents)
norm_commutes = normalized_list(commutes)

#Debug prints to verify
print("---Raw Query Results--")
print(rows)
print("\n -- Normalized Values ---")
print("Normalized rents", norm_rents)
print("Normalized commutes",norm_commutes)

#Trade off Calculation

results = []
for i in range(len(rows)):
    neighborhood_name = rows[i][0]
    raw_rent = rows[i][2]
    raw_commute = rows[i][4]

    #Calculate weighted score(Trade-off)
    score = (0.5 * norm_rents[i]) + (0.5 * norm_commutes[i])

    #Store clean summary dictionaries
    results.append({
        "neighborhood":neighborhood_name,
        "rent":float(raw_rent),
        "commute_mins":float(raw_commute),
        "score":round(score, 3)
    })

#Sorting the results by Best Trade-Off (Lowest scores first)
sorted_results = sorted(results, key=lambda x: x["score"])
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("DB_URI")


def normalized_list(numbers):
    float_nums = [float(n) for n in numbers]
    minimum = min(float_nums)
    maximum = max(float_nums)

    if maximum == minimum:
        return [0.0 for _ in float_nums]

    normalized = []
    for value in float_nums:
        norm_value = (value - minimum) / (maximum - minimum)
        normalized.append(norm_value)

    return normalized


def calculate_tradeoffs(target_hub_id=1, rent_weight=0.5):
    conn = psycopg2.connect(DB_URI)
    cursor = conn.cursor()

    query = """
    SELECT
        Rentals.neighborhood_name,
        Rentals.city,
        Rentals.average_monthly_rent,
        CommuteCache.driving_distance_miles,
        CommuteCache.driving_time_minutes
    FROM
        Rentals
    INNER JOIN
        CommuteCache ON Rentals.neighborhood_id = CommuteCache.neighborhood_id
    WHERE
        CommuteCache.hub_id = %s;
    """

    cursor.execute(query, [target_hub_id])
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rows:
        return []

    # Extract raw numeric lists
    rents = [row[2] for row in rows]
    commutes = [row[4] for row in rows]

    # Normalize between 0.0 and 1.0
    norm_rents = normalized_list(rents)
    norm_commutes = normalized_list(commutes)

    commute_weight = 1.0 - float(rent_weight)
    results = []

    for i in range(len(rows)):
        score = (float(rent_weight) * norm_rents[i]) + (commute_weight * norm_commutes[i])

        results.append({
            "neighborhood": rows[i][0],
            "city": rows[i][1],
            "rent": float(rows[i][2]),
            "distance_miles": float(rows[i][3]),
            "commute_mins": float(rows[i][4]),
            "score": round(score, 3)
        })

    # Crucial line: Return the sorted list back to the caller!
    return sorted(results, key=lambda x: x["score"])


if __name__ == "__main__":
    test_output = calculate_tradeoffs(1, 0.5)
    print("Test successful! Returned rows:", len(test_output))
    for item in test_output[:3]:
        print(item)
# DFW Rent vs. Commute Trade-Off Dashboard

An interactive full-stack analytics dashboard designed to solve the classic Dallas–Fort Worth urban dilemma: balancing rental affordability against daily highway commute duration. 

The application dynamically computes multi-variable trade-off rankings across key DFW neighborhoods based on user-weighted priorities using Min-Max normalization.

---

## Features

- **Dynamic Priority Weighting:** Adjust rent vs. commute priority on a continuous 0.0 to 1.0 scale via an interactive slider.
- **Multi-Hub Routing:** Switch between major regional employment hubs (Downtown Dallas, Legacy West / Plano, Downtown Fort Worth).
- **Sub-50ms Response Latency:** Precomputed routing caches eliminate live external mapping API bottlenecks.
- **Automated Keep-Alive:** Scheduled GitHub Actions keep the remote PostgreSQL database active indefinitely.

---

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Database:** PostgreSQL (Supabase), `psycopg2`
- **Routing & Geodata:** Google Maps Routes / Distance Matrix API
- **Frontend:** Vanilla JavaScript (ES6+), HTML5, CSS3 (zero build tools / dependencies)
- **CI/CD / Automation:** GitHub Actions

---

## Architecture & Math Model

### 1. Relational Schema
- `Rentals`: Stores neighborhood centroids, municipal names, and median rental rates.
- `CommuteCache`: Precomputed matrix containing driving distances (miles) and durations (minutes) from neighborhood centroids to primary regional workplace hubs.

### 2. Normalization & Scoring
Because monthly rent (e.g., \$1,250–\$2,300) and commute times (e.g., 7–45 mins) exist on vastly different scales, raw sums would heavily bias toward rent. Both dimensions are scaled into non-dimensional unit intervals using **Min-Max Feature Scaling**:

$$z_i = \frac{x_i - \min(X)}{\max(X) - \min(X)}$$

Where $z_i \in [0, 1]$. The composite penalty score is then calculated as:

$$\text{Score} = (w_{\text{rent}} \cdot z_{\text{rent}}) + ((1 - w_{\text{rent}}) \cdot z_{\text{commute}})$$

Lower composite scores reflect superior trade-off alignment for the user's specific preferences.

---

## Project Structure

```text
├── .github/
│   └── workflows/
│       └── keep-alive.yml      # Automated Supabase ping workflow
├── frontend/
│   ├── index.html              # Clean UI skeleton & styling
│   └── app.js                  # DOM manipulation & asynchronous API fetch client
├── calculator.py               # SQL queries, Min-Max math, & ranking algorithms
├── main.py                     # FastAPI application endpoints & CORS handling
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
└── .gitignore                  # Exclusion rules for secrets and virtualenvs

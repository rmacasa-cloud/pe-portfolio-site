import os

from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Pages that drive the dynamic navigation bar. The context_processor below
# injects this into every template, so the nav is built from one source.
PAGES = [
    {"name": "Home", "endpoint": "index"},
    {"name": "Experience", "endpoint": "experience"},
    {"name": "Education", "endpoint": "education"},
    {"name": "Hobbies", "endpoint": "hobbies"},
    {"name": "Travel", "endpoint": "travel"},
]


@app.context_processor
def inject_pages():
    """Make the nav pages available to every template automatically."""
    return {"pages": PAGES}


# Work experience, rendered with a Jinja {% for %} loop (no hardcoded repetition).
EXPERIENCE = [
    {
        "role": "Undergraduate Research Assistant",
        "org": "UCSB Systems and Networking Lab",
        "dates": "Dec 2025 – Present",
        "points": [
            "Migrated 8 metric endpoints from 5s HTTP polling to Gorilla WebSocket "
            "streaming via event-driven deltas.",
            "Refactored the NetVibe speedtest pipeline to backend Prometheus scraping "
            "across 3 microservices and a 10-node cluster.",
            "Implemented JWT middleware in Go securing 20+ API routes with "
            "user-context forwarding.",
            "Built a Go ICMP library tracking RTT across 30+ targets, batching latency "
            "into InfluxDB and SQLite.",
        ],
    },
    {
        "role": "Full-Stack Developer",
        "org": "ACM Industry @ UCSB – IV Outfitters",
        "dates": "Jan 2026 – Present",
        "points": [
            "Building an automation system processing 25+ weekly orders with Next.js, "
            "FastAPI, and PostgreSQL.",
            "Integrated Printavo and vendor APIs to automate PO generation and "
            "shipment tracking.",
            "Implemented Celery + Redis task queues running 6-hour polling cycles to "
            "sync tracking data.",
        ],
    },
    {
        "role": "Software Engineering Intern",
        "org": "Willamette Valley Rheumatology Clinic",
        "dates": "Jun 2025 – Sep 2025",
        "points": [
            "Developed Python automation tools handling patient intake and insurance "
            "across ~50 daily visits.",
            "Built data-validation pipelines enforcing consistency across intake, "
            "insurance, and documentation.",
            "Migrated manual record management into centralized digital workflows, "
            "cutting redundant data entry.",
        ],
    },
]


# Education, also rendered with a Jinja {% for %} loop.
EDUCATION = [
    {
        "school": "University of California, Santa Barbara",
        "degree": "B.S. in Computer Science",
        "dates": "Expected June 2028",
        "honors": "Dean's Honors · GPA 3.91/4.0",
        "coursework": [
            "Data Structures & Algorithms",
            "Computer Architecture",
            "Object-Oriented Programming",
        ],
    },
]


@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/experience")
def experience():
    return render_template("experience.html", title="Experience", experience=EXPERIENCE)


@app.route("/education")
def education():
    return render_template("education.html", title="Education", education=EDUCATION)


# Hobbies. Each entry names a candidate image basename; the actual image is
# resolved against whatever files exist in static/img (any common extension),
# so a missing file simply yields a clean text-only card instead of a broken
# image.
IMG_DIR = os.path.join(app.static_folder, "img")
_IMG_EXTENSIONS = (".jfif", ".jpg", ".jpeg", ".png", ".webp", ".gif")

HOBBIES = [
    {
        "name": "Basketball",
        "image": "basketball",
        "description": "Pickup games and watching the league whenever I get the chance.",
    },
    {
        "name": "Foodie",
        "image": "food",
        "description": "Always hunting for the next great meal and new cuisines to try.",
    },
    {
        "name": "Video Games",
        "image": "videogame",
        "description": "Unwinding with competitive and story-driven games alike.",
    },
    {
        "name": "Movies & Anime",
        "image": "anime",
        "description": "Long-running anime series and a good movie night.",
    },
]


def _resolve_image(basename):
    """Return 'img/<file>' if a matching image exists in static/img, else None."""
    for ext in _IMG_EXTENSIONS:
        if os.path.exists(os.path.join(IMG_DIR, basename + ext)):
            return "img/" + basename + ext
    return None


for _hobby in HOBBIES:
    _hobby["image_path"] = _resolve_image(_hobby["image"])


@app.route("/hobbies")
def hobbies():
    return render_template("hobbies.html", title="Hobbies", hobbies=HOBBIES)


# Places visited, plotted as Leaflet markers. Coordinates are hardcoded so the
# map needs no geocoding API and the page carries zero secrets.
PLACES = [
    {"name": "Belize", "lat": 17.1899, "lng": -88.4976},
    {"name": "Italy", "lat": 41.8719, "lng": 12.5674},
    {"name": "Germany", "lat": 51.1657, "lng": 10.4515},
    {"name": "Philippines", "lat": 12.8797, "lng": 121.7740},
    {"name": "Switzerland", "lat": 46.8182, "lng": 8.2275},
    {"name": "Ireland", "lat": 53.4129, "lng": -8.2439},
    {"name": "Japan", "lat": 36.2048, "lng": 138.2529},
    {"name": "Mexico", "lat": 23.6345, "lng": -102.5528},
    {"name": "Puerto Rico", "lat": 18.2208, "lng": -66.5901},
    {"name": "Cuba", "lat": 21.5218, "lng": -77.7812},
    {"name": "France", "lat": 46.2276, "lng": 2.2137},
    {"name": "Portugal", "lat": 39.3999, "lng": -8.2245},
    {"name": "Spain", "lat": 40.4637, "lng": -3.7492},
    {"name": "Belgium", "lat": 50.5039, "lng": 4.4699},
    {"name": "Canada", "lat": 56.1304, "lng": -106.3468},
    {"name": "New York City", "lat": 40.7128, "lng": -74.0060},
]


@app.route("/map")
def travel():
    return render_template("map.html", title="Travel", places=PLACES)

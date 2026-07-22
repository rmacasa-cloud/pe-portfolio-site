import os
import datetime
import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from peewee import MySQLDatabase, SqliteDatabase, Model, CharField, TextField, DateTimeField
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    db = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    db = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


db.connect()
db.create_tables([TimelinePost])


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
        "role": "Software Engineer Intern",
        "org": "Associated Environmental Systems",
        "dates": "Jun 2026 – Sep 2026",
        "points": [
            "Architected a full-stack coordinator dashboard (Next.js, TypeScript, Prisma, "
            "PostgreSQL) as sole engineer, replacing a legacy spreadsheet workflow used by "
            "150+ technicians.",
            "Unified 3 coordinator workflows — calibration, certificates, and coordination "
            "— into one REST API.",
            "Cut daily coordination turnaround ~60% by shipping the MVP end to end and "
            "deploying it to Vercel.",
        ],
    },
    {
        "role": "Undergraduate Researcher",
        "org": "Oregon State University – TRUE-AI Lab",
        "dates": "Jun 2026 – Present",
        "points": [
            "Building a generation-and-verification pipeline that prompts frontier LLMs to "
            "synthesize real-time OS schedulers, auto-checked against formal schedulability "
            "tests, targeting a workshop paper.",
            "Benchmarked generated schedulers across 1,000 task sets, matching "
            "Rate-Monotonic/EDF baselines on 93% while isolating 27 constrained-deadline "
            "failures.",
        ],
    },

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

@app.route("/timeline")
def timeline():
    return render_template("timeline.html", title="Timeline")


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


@app.route("/api/timeline_post", methods=["POST"])
def create_timeline_post():
    data = request.get_json()

    if "name" not in data or not data["name"]:
        return "Invalid name", 400
    if "email" not in data or not data["email"] or "@" not in data["email"]:
        return "Invalid email", 400
    if "content" not in data or not data["content"]:
        return "Invalid content", 400
    
    post = TimelinePost.create(
        name=data["name"],
        email=data["email"],
        content=data["content"],
    )
    return jsonify(model_to_dict(post)), 201


@app.route("/api/timeline_post", methods=["GET"])
def get_timeline_posts():
    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    return jsonify([model_to_dict(p) for p in posts])


@app.route("/api/timeline_post/<int:post_id>", methods=["DELETE"])
def delete_timeline_post(post_id):
    post = TimelinePost.get_or_none(TimelinePost.id == post_id)
    if post is None:
        return jsonify({"error": "not found"}), 404
    post.delete_instance()
    return jsonify({"deleted": post_id}), 200
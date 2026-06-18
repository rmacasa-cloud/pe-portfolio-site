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


@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/experience")
def experience():
    return render_template("experience.html", title="Experience")


@app.route("/education")
def education():
    return render_template("education.html", title="Education")


@app.route("/hobbies")
def hobbies():
    return render_template("hobbies.html", title="Hobbies")


@app.route("/map")
def travel():
    return render_template("map.html", title="Travel")

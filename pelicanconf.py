from __future__ import annotations

import os
from pathlib import Path

# Core site settings
AUTHOR = "Positronic Robotics"
SITENAME = "Positronic Robotics — Infrastructure for ML Robotics"
SITESUBTITLE = "Infrastructure for ML Robotics"
SITEURL = os.getenv("SITEURL", "https://positronic.ro").rstrip("/")
SITEDESCRIPTION = "Machine learning in robotics is still mostly broken. We're fixing this by building two core pieces: ⚡ Positronic Runtime — immediate-mode, Python-native middleware to wire cameras, arms, sensors, and inference. Simple to read, extend, and ship. 📂 Data OS for Robotics — a dataset format that handles multi-rate sensor data natively, plus a web UI to browse, label, filter, and curate episodes."

# Content paths
PATH = "content"
PAGE_PATHS = ["pages"]
PAGE_EXCLUDES: list[str] = []
ARTICLE_PATHS: list[str] = ["blog"]
STATIC_PATHS: list[str] = ["neapolis_deck"]

# Theme
THEME = "theme/positronic"

# Output
OUTPUT_PATH = "output"
DELETE_OUTPUT_DIRECTORY = False

# URLs
PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"
INDEX_SAVE_AS = "blog.html"

TIMEZONE = "Europe/Nicosia"
DEFAULT_LANG = "en"
DEFAULT_PAGINATION = False
RELATIVE_URLS = True

# Clean unused Pelican pages we don't need for a single-page site
DIRECT_TEMPLATES: list[str] = ["index"]
TAGS_SAVE_AS = ""
CATEGORY_SAVE_AS = ""
AUTHORS_SAVE_AS = ""
ARCHIVES_SAVE_AS = ""
CATEGORIES_SAVE_AS = ""

# Disable feed generation for this single-page site
FEED_ALL_ATOM = None
FEED_ALL_RSS = None
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
FEED_MAX_ITEMS = 0

# Markdown settings
MARKDOWN = {
    "extensions": ["markdown.extensions.extra", "markdown.extensions.codehilite"],
}

# Convenience helpers
BASE_DIR = Path(__file__).parent.resolve()
THEME_STATIC_DIR = Path(THEME) / "static"
if not THEME_STATIC_DIR.exists():
    THEME_STATIC_DIR.mkdir(parents=True, exist_ok=True)

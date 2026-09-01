from __future__ import annotations

import os
from pathlib import Path

# Core site settings
AUTHOR = "Positronic Robotics"
SITENAME = "Positronic Robotics"
SITESUBTITLE = "The new standard of Physical AI eval"
PRODUCTION_ORIGIN = "https://positronic.ro"
SITEURL = os.getenv("SITEURL", PRODUCTION_ORIGIN).rstrip("/")

# A search result shows about 155 characters of the description and cuts the rest.
SITEDESCRIPTION = (
    "Positronic Robotics runs independent evaluation for physical AI. Send a checkpoint, "
    "get video and a score for every run on real robots, back the same day."
)
BLOG_DESCRIPTION = (
    "Notes from Positronic Robotics on evaluating physical AI: how we measure robot "
    "policies, what the numbers mean, and what the leaderboard shows."
)

# RELATIVE_URLS rewrites SITEURL per page, so a canonical and an og:url need their own
# absolute base. It always points at production, which also keeps preview builds out of
# the index.
CANONICAL_BASE = os.getenv("CANONICAL_BASE", PRODUCTION_ORIGIN).rstrip("/")

# Content paths
PATH = "content"
PAGE_PATHS = ["pages"]
PAGE_EXCLUDES: list[str] = []
ARTICLE_PATHS: list[str] = ["blog"]
STATIC_PATHS: list[str] = ["neapolis_deck", "nebius-berlin-0426", "extra"]

# Files a browser or a phone looks for at the site root, by name.
ROOT_FILES = [
    "favicon.ico",
    "icon-192.png",
    "icon-512.png",
    "apple-touch-icon.png",
    "site.webmanifest",
]
EXTRA_PATH_METADATA = {f"extra/{name}": {"path": name} for name in ROOT_FILES}

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
DIRECT_TEMPLATES: list[str] = ["index", "sitemap", "robots"]
SITEMAP_SAVE_AS = "sitemap.xml"
ROBOTS_SAVE_AS = "robots.txt"
# A direct template is looked up by name plus each of these, so a template keeps the
# extension of the file it writes.
TEMPLATE_EXTENSIONS: list[str] = [".html", ".xml", ".txt"]
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
    "extensions": ["markdown.extensions.extra", "markdown.extensions.codehilite", "markdown.extensions.toc"],
}

# Convenience helpers
BASE_DIR = Path(__file__).parent.resolve()
THEME_STATIC_DIR = Path(THEME) / "static"
if not THEME_STATIC_DIR.exists():
    THEME_STATIC_DIR.mkdir(parents=True, exist_ok=True)

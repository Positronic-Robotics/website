from __future__ import annotations

import os
from pathlib import Path

# Core site settings
AUTHOR = "Positronic Robotics"
SITENAME = "Positronic Robotics"
SITESUBTITLE = "The new standard of Physical AI eval"
SITEURL = os.getenv("SITEURL", "https://positronic.ro").rstrip("/")

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
CANONICAL_BASE = os.getenv("CANONICAL_BASE", "https://positronic.ro").rstrip("/")

# Content paths
PATH = "content"
PAGE_PATHS = ["pages"]
PAGE_EXCLUDES: list[str] = []
ARTICLE_PATHS: list[str] = ["blog"]
STATIC_PATHS: list[str] = ["neapolis_deck", "nebius-berlin-0426", "extra"]

# Files a browser, a crawler or a phone looks for at the site root.
EXTRA_PATH_METADATA = {
    "extra/favicon.ico": {"path": "favicon.ico"},
    "extra/icon-192.png": {"path": "icon-192.png"},
    "extra/icon-512.png": {"path": "icon-512.png"},
    "extra/apple-touch-icon.png": {"path": "apple-touch-icon.png"},
    "extra/site.webmanifest": {"path": "site.webmanifest"},
    "extra/robots.txt": {"path": "robots.txt"},
}

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
DIRECT_TEMPLATES: list[str] = ["index", "sitemap"]
SITEMAP_SAVE_AS = "sitemap.xml"
# A direct template is looked up by name plus each of these, so the sitemap keeps
# the extension of the file it writes.
TEMPLATE_EXTENSIONS: list[str] = [".html", ".xml"]
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

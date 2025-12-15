from __future__ import annotations

import os

from pelicanconf import *  # noqa: F401,F403

# Production overrides
SITEURL = os.getenv("SITEURL", "https://positronic.ro").rstrip("/")
RELATIVE_URLS = False


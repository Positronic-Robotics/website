"""Renders the Docs page from the client guide in the public positronic repository, read once per build.

The guide is `client/README.md` in Positronic-Robotics/positronic, the guide that the console's Get
started page names as the full reference. The build reads it at the tag of the latest `positronic`
release on PyPI, the version that `uv tool install positronic` installs. `DOCS_REF` pins another git
ref, and `DOCS_SOURCE` names a local Markdown file (the tests pass a fixture). A link relative to the
guide becomes a GitHub link at that ref. A failed read fails the build.
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

import markdown
from pelican import signals

GUIDE_PLACEHOLDER = "{CLIENT_GUIDE}"
CONTENTS_PLACEHOLDER = "{CLIENT_GUIDE_CONTENTS}"
REF_PLACEHOLDER = "{CLIENT_GUIDE_REF}"
REPO = "Positronic-Robotics/positronic"
GUIDE_PATH = "client/README.md"
RELEASE_URL = "https://pypi.org/pypi/positronic/json"

_guide: dict[str, str] | None = None


def _get(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read()


def latest_release_tag() -> str:
    return "v" + json.loads(_get(RELEASE_URL))["info"]["version"]


def guide_url(ref: str) -> str:
    return f"https://github.com/{REPO}/blob/{ref}/{GUIDE_PATH}"


def _absolute(target: str, ref: str) -> str:
    if re.match(r"[a-z]+:|#", target):
        return target
    return urllib.parse.urljoin(guide_url(ref), target)


def render(text: str, ref: str) -> dict[str, str]:
    """The guide as HTML with no title, its table of contents, and the ref it was read at."""
    body = re.sub(r"\A# [^\n]*\n", "", text.lstrip())
    body = re.sub(r"\]\(([^)\s]+)\)", lambda m: f"]({_absolute(m.group(1), ref)})", body)
    md = markdown.Markdown(
        extensions=["extra", "toc"], extension_configs={"toc": {"toc_depth": "2"}}
    )
    html = md.convert(body)
    if "<h2" not in html:
        raise ValueError("the client guide has no sections")
    return {GUIDE_PLACEHOLDER: html, CONTENTS_PLACEHOLDER: md.toc, REF_PLACEHOLDER: ref}


def _read(pelican) -> None:
    global _guide
    settings = pelican.settings
    ref = settings.get("DOCS_REF") or latest_release_tag()
    source = settings.get("DOCS_SOURCE")
    if source:
        text = Path(source).read_text()
    else:
        text = _get(f"https://raw.githubusercontent.com/{REPO}/{ref}/{GUIDE_PATH}").decode()
    _guide = render(text, ref)


def _fill(content) -> None:
    text = getattr(content, "_content", None)
    if not text or GUIDE_PLACEHOLDER not in text:
        return
    assert _guide is not None
    for placeholder, value in _guide.items():
        text = text.replace(placeholder, value)
    content._content = text


def register() -> None:
    signals.initialized.connect(_read)
    signals.content_object_init.connect(_fill)

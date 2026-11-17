"""Renders the Docs page from the client guide in the public positronic repository, read once per build.

The guide is `client/README.md` in Positronic-Robotics/positronic, the guide that the console's Get
started page names as the full reference. The build reads it at the tag of the latest `positronic`
release on PyPI, the version that `uv tool install positronic` installs. `DOCS_REF` pins another git
ref, and `DOCS_SOURCE` names a local Markdown file (the tests pass a fixture). A link relative to the
guide becomes a GitHub link at that ref. The home page shows the guide's first `positronic eval run`
command. A failed read, or a guide with no sections or no such command, fails the build.
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from html import escape as html_escape
from pathlib import Path

import markdown
from pelican import signals

GUIDE_PLACEHOLDER = "{CLIENT_GUIDE}"
CONTENTS_PLACEHOLDER = "{CLIENT_GUIDE_CONTENTS}"
REF_PLACEHOLDER = "{CLIENT_GUIDE_REF}"
SUBMIT_PLACEHOLDER = "{CLIENT_SUBMIT_COMMAND}"
SUBMIT_SECTION = "## From the command line"
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


def submit_command(text: str) -> str:
    """The first `positronic eval run` command in the guide's command-line section, with no comment."""
    section = text.partition(f"\n{SUBMIT_SECTION}\n")[2].split("\n## ", 1)[0]
    for line in section.splitlines():
        command = re.sub(r"\s+#.*", "", line).strip()
        if command.startswith(("positronic eval run", "uv run positronic eval run")):
            return command
    raise ValueError(f"the client guide names no `positronic eval run` command under {SUBMIT_SECTION!r}")


def render(text: str, ref: str) -> dict[str, str]:
    """The guide as HTML with no title, its table of contents, the ref it was read at, and its submit command."""
    body = re.sub(r"\A# [^\n]*\n", "", text.lstrip())
    body = re.sub(r"\]\(([^)\s]+)\)", lambda m: f"]({_absolute(m.group(1), ref)})", body)
    md = markdown.Markdown(
        extensions=["extra", "toc"], extension_configs={"toc": {"toc_depth": "2"}}
    )
    html = md.convert(body)
    if "<h2" not in html:
        raise ValueError("the client guide has no sections")
    return {
        GUIDE_PLACEHOLDER: html,
        CONTENTS_PLACEHOLDER: md.toc,
        REF_PLACEHOLDER: ref,
        SUBMIT_PLACEHOLDER: html_escape(submit_command(text)),
    }


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
    if not text or not any(placeholder in text for placeholder in (GUIDE_PLACEHOLDER, SUBMIT_PLACEHOLDER)):
        return
    assert _guide is not None
    for placeholder, value in _guide.items():
        text = text.replace(placeholder, value)
    content._content = text


def register() -> None:
    signals.initialized.connect(_read)
    signals.content_object_init.connect(_fill)

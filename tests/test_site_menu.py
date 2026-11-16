"""The menu of every page, and the Pricing and Docs pages that it opens on the website."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
APP = "https://console.positronic.ro"
PAGES = ["index.html", "pricing.html", "docs.html", "about.html", "blog.html", "privacy.html", "terms.html", "introducing-phail.html"]


@pytest.fixture(scope="module")
def site(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("output")
    subprocess.run(
        [sys.executable, "-m", "pelican", "content", "-s", "publishconf.py", "-o", str(out), "-q"],
        cwd=ROOT,
        env={"PYTHONPATH": str(ROOT)},
        check=True,
    )
    return out


def _block(html: str, pattern: str) -> str:
    match = re.search(pattern, html, re.S)
    assert match, pattern
    return match.group(0)


def _links(block: str) -> list[tuple[str, str]]:
    return [(text.strip(), href) for href, text in re.findall(r'<a href="([^"]+)"[^>]*>([^<]*)</a>', block)]


def test_every_page_has_the_same_menu(site: Path) -> None:
    for page in PAGES:
        html = (site / page).read_text()
        site_nav = _block(html, r'<nav aria-label="Site">.*?</nav>')
        app_nav = _block(html, r'<nav class="navbar-app".*?</nav>')
        assert _links(site_nav) == [
            ("Pricing", "https://positronic.ro/pricing"),
            ("Docs", "https://positronic.ro/docs"),
            ("For labs", "https://positronic.ro/#talk"),
            ("About", "https://positronic.ro/about"),
            ("Blog", "https://positronic.ro/blog"),
        ], page
        assert _links(app_nav) == [("Log in", f"{APP}/signin")], page


def test_the_logo_goes_home(site: Path) -> None:
    header = _block((site / "index.html").read_text(), r'<header class="navbar">.*?</header>')
    assert '<a href="https://positronic.ro/" class="navbar-brand">' in header


def test_only_sign_in_and_account_links_leave_for_the_console(site: Path) -> None:
    # The terms define the console's pricing page by its address, so they keep that link.
    for page in (page for page in PAGES if page != "terms.html"):
        html = (site / page).read_text()
        assert "{APP_URL}" not in html, page
        console = set(re.findall(rf'href="{APP}(/[^"]*)"', html))
        assert console <= {"/signin", "/account"}, (page, console)


def test_pricing_and_docs_center_their_buttons_like_the_home_page(site: Path) -> None:
    for page in ("pricing.html", "docs.html"):
        hero = _block((site / page).read_text(), r'<section class="page-head">.*?</section>')
        assert f'<div class="actions"><a class="act act-primary" href="{APP}/signin">Sign up</a></div>' in hero, page
    css = (ROOT / "theme/positronic/static/css/platform.css").read_text()
    assert "justify-content: flex-start" not in css

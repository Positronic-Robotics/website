"""The home page is one headline and two buttons; the old home page is the For labs page at /labs."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from conftest import build_site

APP = "https://console.positronic.ro"
HEADLINE = "Test your physical AI on real robots and in sim."


@pytest.fixture(scope="module")
def site(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("output")
    build_site(out).check_returncode()
    return out


def _main(html: str) -> str:
    match = re.search(r"<main>(.*?)</main>", html, re.S)
    assert match, "no main"
    return match.group(1)


def test_home_is_the_headline_and_two_buttons(site: Path) -> None:
    main = _main((site / "index.html").read_text())
    sections = re.findall(r"<section\b.*?</section>", main, re.S)
    assert sections == [
        f'<section class="hero"><h1>{HEADLINE}</h1><div class="actions">'
        f'<a class="act act-primary" href="{APP}/signin">Get started</a>'
        '<a class="act act-ghost" href="/labs#talk">Talk to us</a></div></section>'
    ]
    assert re.sub(r"<section\b.*?</section>|<div class=\"home\">|</div>|\s", "", main, flags=re.S) == ""


def test_home_title_names_the_headline(site: Path) -> None:
    html = (site / "index.html").read_text()
    assert "<title>Positronic Robotics: test your physical AI on real robots and in sim</title>" in html


def test_home_keeps_the_banner_and_the_footer(site: Path) -> None:
    html = (site / "index.html").read_text()
    assert '<aside class="announce" id="announce"' in html
    assert '<footer class="site-footer">' in html
    assert 'id="contact-form"' not in html


def test_labs_carries_the_old_home_page(site: Path) -> None:
    main = _main((site / "labs.html").read_text())
    assert "<h1>The new standard&nbsp;of <em>Physical AI evaluation</em></h1>" in main
    assert "<figcaption>Andy Chen, Head of Robotics, Runway</figcaption>" in main
    assert '<a class="act act-primary" href="#talk">Talk to us</a>' in main
    assert '<a class="act act-ghost" href="https://phail.ai">See the leaderboard' in main
    assert re.findall(r'<span class="card-label">([^<]+)</span>', main) == ["Problem", "Method", "Protocol"]
    assert 'read the <a href="https://arxiv.org/abs/2605.29710">PhAIL paper</a> on arXiv.' in main
    assert '<section class="band close" id="talk">' in main
    assert '<form class="contact" id="contact-form">' in main
    assert "contact.js" in (site / "labs.html").read_text()


def test_no_link_opens_the_contact_form_on_the_home_page(site: Path) -> None:
    pages = sorted(site.rglob("*.html"))
    assert pages
    for page in pages:
        hrefs = re.findall(r'href="([^"]+)"', page.read_text())
        stale = [h for h in hrefs if h.endswith("/#talk") or (h.startswith("#talk") and page.name != "labs.html")]
        assert stale == [], page.relative_to(site)


def test_labs_is_in_the_sitemap(site: Path) -> None:
    locs = re.findall(r"<loc>([^<]+)</loc>", (site / "sitemap.xml").read_text())
    assert "https://positronic.ro/labs" in locs
    assert "https://positronic.ro/" in locs

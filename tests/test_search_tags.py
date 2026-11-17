"""Each page gives a search engine and a link preview its own description, a wide card image and the company profiles."""

from __future__ import annotations

import json
import re
import struct
from pathlib import Path

import pytest
from conftest import build_site

ORIGIN = "https://positronic.ro"
NEW_PAGES = ("index", "pricing", "docs", "labs")


@pytest.fixture(scope="module")
def site(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("output")
    build_site(out).check_returncode()
    return out


def _meta(html: str, key: str) -> str:
    values = re.findall(rf'<meta (?:name|property)="{re.escape(key)}" content="([^"]*)" />', html)
    assert len(values) == 1, (key, values)
    return values[0]


def test_each_new_page_has_its_own_description_of_at_most_155_characters(site: Path) -> None:
    descriptions = {}
    for name in NEW_PAGES:
        html = (site / f"{name}.html").read_text()
        descriptions[name] = _meta(html, "description")
        assert _meta(html, "og:description") == descriptions[name], name
        assert len(descriptions[name]) <= 155, (name, len(descriptions[name]))
    assert len(set(descriptions.values())) == len(NEW_PAGES), descriptions


def test_home_description_names_the_product(site: Path) -> None:
    description = _meta((site / "index.html").read_text(), "description")
    assert description == (
        "Positronic Robotics tests physical AI on real robots and in sim. Your coding agent submits the model; "
        "you get video, robot data and a score. Pay as you go."
    )


def test_labs_title_names_physical_ai_evaluation(site: Path) -> None:
    html = (site / "labs.html").read_text()
    assert "<title>Physical AI evaluation for labs — Positronic Robotics</title>" in html
    assert _meta(html, "description").startswith("Independent physical AI evaluation for labs")


def _jpeg_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    at = 2
    while data[at + 1] not in (0xC0, 0xC1, 0xC2):
        at += 2 + int.from_bytes(data[at + 2 : at + 4], "big")
    height, width = struct.unpack(">HH", data[at + 5 : at + 9])
    return width, height


def test_every_page_shows_a_wide_card_in_a_link_preview(site: Path) -> None:
    pages = sorted(site.glob("*.html")) + sorted(site.glob("press/*.html"))
    assert pages
    for page in pages:
        html = page.read_text()
        assert _meta(html, "twitter:card") == "summary_large_image", page.name
        assert _meta(html, "twitter:site") == "@positronic_ro", page.name
        card = _meta(html, "og:image")
        assert card.startswith(f"{ORIGIN}/media/social-card"), (page.name, card)
        size = (int(_meta(html, "og:image:width")), int(_meta(html, "og:image:height")))
        assert _jpeg_size(site / card.removeprefix(f"{ORIGIN}/")) == size == (1200, 630), (page.name, card)


def test_labs_shares_the_card_of_its_own_film(site: Path) -> None:
    cards = {name: _meta((site / f"{name}.html").read_text(), "og:image") for name in NEW_PAGES}
    assert cards == {
        "index": f"{ORIGIN}/media/social-card.jpg",
        "pricing": f"{ORIGIN}/media/social-card.jpg",
        "docs": f"{ORIGIN}/media/social-card.jpg",
        "labs": f"{ORIGIN}/media/social-card-labs.jpg",
    }


def test_home_names_the_company_and_its_profiles(site: Path) -> None:
    html = (site / "index.html").read_text()
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    assert len(blocks) == 1
    organization = json.loads(blocks[0])
    assert organization["@type"] == "Organization"
    assert organization["description"] == _meta(html, "description")
    assert organization["sameAs"] == [
        "https://github.com/Positronic-Robotics",
        "https://www.linkedin.com/company/positronic-robotics",
        "https://x.com/positronic_ro",
    ]


def test_no_title_or_description_offers_free_credits(site: Path) -> None:
    for page in sorted(site.rglob("*.html")):
        html = page.read_text()
        head = re.search(r"<head>(.*?)</head>", html, re.DOTALL)
        assert head, page.name
        tags = re.findall(r'<title>[^<]*</title>|content="[^"]*"', head.group(1))
        offers = [tag for tag in tags if re.search(r"\bfree\b|welcome credit", tag, re.IGNORECASE)]
        assert offers == [], (page.relative_to(site), offers)

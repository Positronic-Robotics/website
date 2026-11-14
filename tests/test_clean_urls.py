"""The host answers 308 on `<name>.html`, so the build must name only the address without it."""

from __future__ import annotations

import re
from pathlib import Path


def _pages(site: Path) -> list[Path]:
    return sorted(site.glob("*.html")) + sorted(site.glob("press/*.html"))


def test_canonical_and_og_url_name_the_address_without_html(site: Path) -> None:
    for page in _pages(site):
        html = page.read_text()
        for attr in ("canonical", "og:url"):
            urls = re.findall(rf'(?:rel="{attr}" href|property="{attr}" content)="([^"]+)"', html)
            assert urls, f"{page.name} has no {attr}"
            assert not any(u.endswith(".html") for u in urls), f"{page.name} {attr}: {urls}"


def test_sitemap_names_the_address_without_html(site: Path) -> None:
    locs = re.findall(r"<loc>([^<]+)</loc>", (site / "sitemap.xml").read_text())
    assert "https://positronic.ro/about" in locs
    assert "https://positronic.ro/physical-ai-evaluation" not in locs
    assert [loc for loc in locs if loc.endswith(".html")] == []


def test_internal_links_name_the_address_without_html(site: Path) -> None:
    for page in _pages(site):
        hrefs = re.findall(r'href="([^"]+)"', page.read_text())
        internal = [h for h in hrefs if not h.startswith("http") or h.startswith("https://positronic.ro")]
        assert [h for h in internal if ".html" in h] == [], page.name


def test_each_page_is_still_written_as_an_html_file(site: Path) -> None:
    for name in ("index", "about", "blog", "404"):
        assert (site / f"{name}.html").is_file()
    assert (site / "press" / "phail-launch.html").is_file()


def test_the_removed_evaluation_page_redirects_to_about(site: Path) -> None:
    rules = [line.split() for line in (site / "_redirects").read_text().splitlines()]
    assert ["/physical-ai-evaluation", "/about", "301"] in rules
    assert ["/physical-ai-evaluation.html", "/about", "301"] in rules
    assert not (site / "physical-ai-evaluation.html").exists()


def test_about_opens_on_the_lab_film(site: Path) -> None:
    html = (site / "about.html").read_text()
    assert 'class="ev-film-video"' in html
    assert "film.js" in html

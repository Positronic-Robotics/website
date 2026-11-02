"""The host answers 308 on `<name>.html`, so the build must name only the address without it."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


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
    assert "https://positronic.ro/physical-ai-evaluation" in locs
    assert [loc for loc in locs if loc.endswith(".html")] == []


def test_internal_links_name_the_address_without_html(site: Path) -> None:
    for page in _pages(site):
        hrefs = re.findall(r'href="([^"]+)"', page.read_text())
        internal = [h for h in hrefs if not h.startswith("http") or h.startswith("https://positronic.ro")]
        assert [h for h in internal if ".html" in h] == [], page.name


def test_each_page_is_still_written_as_an_html_file(site: Path) -> None:
    for name in ("index", "about", "blog", "physical-ai-evaluation", "404"):
        assert (site / f"{name}.html").is_file()
    assert (site / "press" / "phail-launch.html").is_file()

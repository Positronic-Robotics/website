"""The menu of every page, and the Pricing page that it opens on the website."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from conftest import PRICE_LIST, build_site

ROOT = Path(__file__).resolve().parent.parent
APP = "https://console.positronic.ro"
PAGES = ["index.html", "pricing.html", "about.html", "blog.html", "privacy.html", "terms.html", "introducing-phail.html"]


@pytest.fixture(scope="module")
def site(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("output")
    build_site(out).check_returncode()
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
            ("Docs", f"{APP}/start"),
            ("For labs", "https://positronic.ro/#talk"),
            ("About", "https://positronic.ro/about"),
            ("Blog", "https://positronic.ro/blog"),
        ], page
        assert _links(app_nav) == [("Log in / Sign up", f"{APP}/signin")], page
        assert 'class="navbar-start"' in app_nav, page


def test_the_logo_goes_home(site: Path) -> None:
    header = _block((site / "index.html").read_text(), r'<header class="navbar">.*?</header>')
    assert '<a href="https://positronic.ro/" class="navbar-brand">' in header


def test_only_sign_in_account_and_docs_links_leave_for_the_console(site: Path) -> None:
    # The terms define the console's pricing page by its address, so they keep that link.
    for page in (page for page in PAGES if page != "terms.html"):
        html = (site / page).read_text()
        assert "{APP_URL}" not in html, page
        console = set(re.findall(rf'href="{APP}(/[^"]*)"', html))
        assert console <= {"/signin", "/account", "/start"}, (page, console)


def test_pricing_centers_its_buttons_like_the_home_page(site: Path) -> None:
    hero = _block((site / "pricing.html").read_text(), r'<section class="page-head">.*?</section>')
    assert f'<div class="actions"><a class="act act-primary" href="{APP}/signin">Sign up</a>' in hero
    assert '<a class="act act-ghost" href="/#talk">Talk to us</a>' in hero
    css = (ROOT / "theme/positronic/static/css/platform.css").read_text()
    assert "justify-content: flex-start" not in css


def test_the_website_has_no_copy_of_the_console_get_started_page(site: Path) -> None:
    assert not (site / "docs.html").exists()


def test_pricing_rates_come_from_the_price_list(site: Path) -> None:
    # The fixture: 1000 units a credit, $5 a credit, so 1 unit is $0.005.
    rows = re.findall(r"<tr data-episode=\"([^\"]+)\" data-minute=\"([^\"]+)\"><td>([^<]+)</td>.*?<td class=\"pf-total\">([^<]+)</td>",
                      (site / "pricing.html").read_text())
    assert rows == [
        ("10", "10", "Real robot: Franka DROID", "$30"),
        ("10", "10", "Real robot: two-arm YAM", "$30"),
        ("0.02", "0.5", "RoboLab simulator", "$1.02"),
        ("0.01", "0.1", "MolmoSpaces simulator, model on your server", "$0.21"),
    ]


def test_pricing_names_volume_discounts_next_to_a_talk_to_us_button(site: Path) -> None:
    rates = _block((site / "pricing.html").read_text(), r'<section class="band close" id="rates">.*?</section>')
    assert '<div class="pf-volume"><p>Volume discounts for committed spend.</p><a class="act act-ghost" href="/#talk">Talk to us</a></div>' in rates


def test_pricing_does_not_name_the_credit_price(site: Path) -> None:
    html = (site / "pricing.html").read_text()
    assert "One credit is" not in html
    assert "{CREDIT_PRICE}" not in html


def test_pricing_shows_the_episode_total_in_the_accent_colour() -> None:
    css = (ROOT / "theme/positronic/static/css/platform.css").read_text()
    assert ".platform .pf-rates .pf-total { font-weight: 600; color: var(--accent, #b1e74f); }" in css


def test_a_simulator_with_no_display_name_fails_the_build(tmp_path: Path) -> None:
    price_list = json.loads(PRICE_LIST.read_text())
    price_list["sim"][0]["simulator"] = "newsim"
    source = tmp_path / "pricing.json"
    source.write_text(json.dumps(price_list))
    result = build_site(tmp_path / "out", source)
    assert result.returncode != 0
    assert "newsim" in result.stderr + result.stdout


def test_an_unreadable_price_list_fails_the_build(tmp_path: Path) -> None:
    assert build_site(tmp_path / "out", tmp_path / "missing.json").returncode != 0

"""The menu and footer of every page, the product home page, For labs and About."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
APP = "https://console.positronic.ro"
PAGES = ["index.html", "pricing.html", "docs.html", "labs.html", "about.html", "blog.html", "privacy.html", "terms.html", "introducing-phail.html"]


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
        site_nav = _block(html, r'<nav class="navbar-site".*?</nav>')
        app_nav = _block(html, r'<nav class="navbar-app".*?</nav>')
        assert _links(site_nav) == [
            ("Pricing", "https://positronic.ro/pricing"),
            ("Docs", "https://positronic.ro/docs"),
            ("For labs", "https://positronic.ro/labs"),
            ("About", "https://positronic.ro/about"),
            ("Blog", "https://positronic.ro/blog"),
        ], page
        assert _links(app_nav) == [("Log in", f"{APP}/signin")], page


def test_the_logo_goes_home_and_the_menu_has_no_home_item(site: Path) -> None:
    header = _block((site / "index.html").read_text(), r'<header class="navbar">.*?</header>')
    assert '<a href="https://positronic.ro/" class="navbar-brand">' in header
    for word in (">Home<", "Leaderboard", "Platform<", "Talk to us", "Sign up", "Get started"):
        assert word not in header, word


def test_the_footer_links_privacy_terms_and_social(site: Path) -> None:
    footer = _block((site / "index.html").read_text(), r'<footer class="site-footer">.*?</footer>')
    links = dict(_links(footer))
    assert links["Privacy policy"] == "https://positronic.ro/privacy"
    assert links["Terms of service"] == "https://positronic.ro/terms"
    assert links["LinkedIn"] == "https://www.linkedin.com/company/positronic-robotics"
    assert links["X"] == "https://x.com/positronic_ro"
    assert links["GitHub"] == "https://github.com/Positronic-Robotics/positronic"
    assert links["Discord"] == "https://discord.gg/PXvBy4NBgv"


def test_the_home_page_leads_with_sign_up_and_ends_with_it(site: Path) -> None:
    html = (site / "index.html").read_text()
    assert "{APP_URL}" not in html
    hero = _block(html, r'<section class="hero pf-hero">.*?</section>')
    assert f'<a class="act act-primary" href="{APP}/signin">Sign up</a>' in hero
    assert "pay per run" in hero
    assert html.count(f'<a class="act act-primary" href="{APP}/signin">Sign up</a>') == 2
    assert html.rindex("Sign up") > html.index('id="questions"')


def test_the_home_page_shows_proof_right_under_the_hero(site: Path) -> None:
    html = (site / "index.html").read_text()
    proof = _block(html, r'<section class="standing proof".*?</section>')
    assert html.index("</section>", html.index("pf-hero")) < html.index("standing proof") < html.index('class="reel"')
    assert 'aria-label="Runway"' in proof and "Andy Chen, Head of Robotics, Runway" in proof
    assert "Black Forest Labs" in proof
    assert 'aria-label="Nebius"' in proof and "Founding partner of PhAIL" in proof
    assert "Mimic" not in html


def test_the_home_page_carries_the_product_bands_and_a_line_for_labs(site: Path) -> None:
    html = (site / "index.html").read_text()
    order = ["what-you-can-run", "what-you-get", "agents", "start", "prices", "labs", "questions", "go"]
    positions = [html.index(f'id="{band}"') for band in order]
    assert positions == sorted(positions)
    assert '<a href="/labs">' in _block(html, r'<section class="band" id="labs">.*?</section>')


def test_labs_page_names_the_program_and_ends_in_the_form(site: Path) -> None:
    html = (site / "labs.html").read_text()
    program = _block(html, r'<section class="band" id="program">.*?</section>')
    for part in ("Set up", "Run", "Report", "Invoice"):
        assert f"<b>{part}</b>" in program
    assert "Runway" in html and "Black Forest Labs" in html
    assert html.rindex('id="contact-form"') > html.index('id="proof"')
    assert '<link rel="canonical" href="https://positronic.ro/labs" />' in html


def test_about_opens_on_why_we_exist_then_traction_team_backers_contact(site: Path) -> None:
    html = (site / "about.html").read_text()
    lede = _block(html, r'<p class="hero-lede">.*?</p>')
    assert "Positronic Robotics builds the trust layer for physical AI" in lede
    order = ['class="ev-film', 'id="traction"', ">Team<", ">Backing<", 'id="talk"']
    positions = [html.index(mark) for mark in order]
    assert positions == sorted(positions)
    assert "Based in Berlin." in html and "Paphos, Cyprus" in html


def test_sitemap_lists_the_labs_page(site: Path) -> None:
    assert "<loc>https://positronic.ro/labs</loc>" in (site / "sitemap.xml").read_text()


def test_only_sign_in_and_account_links_leave_for_the_console(site: Path) -> None:
    for page in ("index.html", "pricing.html", "docs.html", "labs.html", "about.html"):
        html = (site / page).read_text()
        console = set(re.findall(rf'href="{APP}(/[^"]*)"', html))
        assert console <= {"/signin", "/account"}, (page, console)

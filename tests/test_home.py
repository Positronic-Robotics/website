"""The home page leads with the product; the old home page is the For labs page at /labs."""

from __future__ import annotations

import json
import re
from decimal import Decimal
from pathlib import Path

import pytest
from conftest import PRICE_LIST, build_site

ROOT = Path(__file__).resolve().parent.parent
APP = "https://console.positronic.ro"


@pytest.fixture(scope="module")
def site(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("output")
    build_site(out).check_returncode()
    return out


def _main(html: str) -> str:
    match = re.search(r"<main>(.*?)</main>", html, re.DOTALL)
    assert match, "no main"
    return match.group(1)


def _sections(site: Path) -> list[str]:
    return re.findall(r"<section\b.*?</section>", _main((site / "index.html").read_text()), re.DOTALL)


def _band(site: Path, label: str) -> str:
    bands = [s for s in _sections(site) if f'<span class="label">{label}</span>' in s]
    assert len(bands) == 1, label
    return bands[0]


def test_home_opens_on_the_headline_a_sub_line_and_two_buttons(site: Path) -> None:
    assert _sections(site)[0] == (
        '<section class="hero"><h1>Test your physical AI on <em>real robots</em> and in sim.</h1>'
        '<p class="hero-lede">Submit from your terminal. Get a video and a score for every episode.</p>'
        '<div class="actions actions-even">'
        f'<a class="act act-primary" href="{APP}/signin">Get started</a>'
        '<a class="act act-ghost" href="/labs#talk">Talk to us</a></div></section>'
    )


def test_home_and_labs_headlines_share_the_hero_accent(site: Path) -> None:
    for page in ("index.html", "labs.html"):
        hero = _main((site / page).read_text()).split("</section>", 1)[0]
        assert re.search(r'<section class="hero"><h1>[^<]*<em>[^<]+</em>', hero), page
    css = (ROOT / "theme/positronic/static/css/home.css").read_text()
    assert css.count(".home h1 em {") == 1


def test_home_sections_come_in_the_approved_order(site: Path) -> None:
    def name(section: str) -> str:
        label = re.search(r'<span class="label">([^<]+)</span>', section)
        return label.group(1) if label else re.match(r'<section class="([^"]+)"', section).group(1)

    assert [name(s) for s in _sections(site)] == ["hero", "reel", "trusted", "proof", "How it works", "Where it runs"]
    main = _main((site / "index.html").read_text())
    assert "Proof" not in main and "What you get back" not in main


def test_the_two_hero_buttons_share_one_size(site: Path) -> None:
    css = (ROOT / "theme/positronic/static/css/home.css").read_text()
    assert ".home .actions-even { display: grid; grid-template-columns: repeat(2, 11rem); }" in css
    assert ".home .actions-even .act { justify-content: center; }" in css


def test_how_it_works_is_four_plain_steps(site: Path) -> None:
    band = _band(site, "How it works")
    steps = re.findall(r'<li><span class="step-verb">([^<]+)</span><p>(.*?)</p></li>', band)
    assert steps == [
        ("1. Sign up", f'Create an account in the <a href="{APP}/signin">console</a> and add funds.'),
        ("2. Connect your model", "A container image, or an endpoint you serve."),
        ("3. Choose where it runs", "Real robots or simulators, and the tasks."),
        ("4. Get the results", "We run the episodes. You get a video, the robot data and a score for each one."),
    ]
    main = _main((site / "index.html").read_text())
    assert "<pre" not in main and "<code" not in main and "positronic eval" not in main


def _environments(site: Path) -> list[tuple[str, str, str]]:
    return re.findall(
        r'<li class="env"><span class="env-kind">([^<]+)</span><span class="env-name">([^<]+)</span>'
        r'<span class="env-price">([^<]+)</span></li>',
        _band(site, "Where it runs"),
    )


def test_where_it_runs_prices_a_two_minute_episode_from_the_price_list(site: Path) -> None:
    # The fixture: 1000 units a credit, $5 a credit. A 2-min rig episode is 2000 + 2 x 2000 units;
    # RoboLab (hosted only) 4 + 2 x 100 units; MolmoSpaces (own server only) 2 + 2 x 20 units.
    assert _environments(site) == [
        ("Real robot", "Franka DROID", "from $30 per 2-min episode"),
        ("Real robot", "Two-arm YAM", "from $30 per 2-min episode"),
        ("Simulator", "RoboLab", "from $1.02 per 2-min episode"),
        ("Simulator", "MolmoSpaces", "from $0.21 per 2-min episode"),
    ]
    band = _band(site, "Where it runs")
    assert '<a href="/pricing">' in band
    assert "{PRICE_ENVIRONMENTS}" not in band


def test_each_home_figure_is_the_cheapest_default_total_on_pricing(tmp_path: Path) -> None:
    # Both hostings of each simulator, so the home page must take the cheaper one.
    price_list = json.loads(PRICE_LIST.read_text())
    price_list["sim"] += [
        {"simulator": "robolab", "hosting": "own_server", "price": {"episode_units": 3, "minute_units": 60, "duration_rounding_sec": 10}},
        {"simulator": "molmospaces", "hosting": "hosted", "price": {"episode_units": 5, "minute_units": 300, "duration_rounding_sec": 10}},
    ]
    source = tmp_path / "pricing.json"
    source.write_text(json.dumps(price_list))
    build_site(tmp_path / "out", source).check_returncode()
    totals = re.findall(r'<tr data-episode="[^"]+" data-minute="[^"]+"><td>([^<]+)</td>.*?<td class="pf-total">\$([^<]+)</td>',
                        (tmp_path / "out" / "pricing.html").read_text())
    rows = {"Franka DROID": "Real robot: Franka DROID", "Two-arm YAM": "Real robot: two-arm YAM",
            "RoboLab": "RoboLab simulator", "MolmoSpaces": "MolmoSpaces simulator"}
    for _kind, name, price in _environments(tmp_path / "out"):
        cheapest = min((Decimal(total) for row, total in totals if row.startswith(rows[name])), default=None)
        assert cheapest is not None, name
        assert price == f"from ${cheapest:f} per 2-min episode", name


def test_where_it_runs_lists_only_the_simulators_the_price_list_names(tmp_path: Path) -> None:
    price_list = json.loads(PRICE_LIST.read_text())
    price_list["sim"] = [line for line in price_list["sim"] if line["simulator"] == "robolab"]
    source = tmp_path / "pricing.json"
    source.write_text(json.dumps(price_list))
    build_site(tmp_path / "out", source).check_returncode()
    html = (tmp_path / "out" / "index.html").read_text()
    assert re.findall(r'<span class="env-name">([^<]+)</span>', html) == ["Franka DROID", "Two-arm YAM", "RoboLab"]


def test_the_clip_of_one_public_phail_run_sits_under_the_buttons(site: Path) -> None:
    reel = _sections(site)[1]
    assert re.findall(r'<video [^>]*src="([^"]+)"', reel) == ["/media/episode-1086.mp4"]
    assert 'poster="/media/episode-1086-poster.jpg"' in reel
    assert '<span class="run-task">Put the banana on the plate on the left</span>' in reel
    assert '<span class="run-model">Ai2 MolmoAct2</span>' in reel
    assert '<span class="run-score">Success in 13 s</span>' in reel
    clip = ROOT / "content/media/episode-1086.mp4"
    assert clip.stat().st_size < 5_000_000
    assert (site / "media/episode-1086.mp4").is_file() and (site / "media/episode-1086-poster.jpg").is_file()


def test_trusted_by_links_each_logo_to_where_it_names_us(site: Path) -> None:
    trusted = _sections(site)[2]
    assert '<p class="trusted-label">Trusted by</p>' in trusted
    links = re.findall(r'<a class="trusted-(\w+)" href="([^"]+)"><svg [^>]*aria-label="([^"]+)"', trusted)
    assert links == [
        ("runway", "https://runway.com/research/praxis-1-video-pretraining-to-robot-control#real", "Runway"),
        ("bfl", "https://bfl.ai/models/flux-3-action", "Black Forest Labs"),
        ("nebius", "/press/phail-launch", "Nebius"),
    ]
    assert (site / "press/phail-launch.html").is_file()


def test_the_quote_is_the_runway_quote_on_labs_word_for_word(site: Path) -> None:
    proof = _sections(site)[3]
    assert 'class="label"' not in proof
    line = re.search(r"<blockquote>([^<]+)</blockquote>", proof).group(1)
    labs_quote = re.search(r"<blockquote>([^<]+)</blockquote>", (site / "labs.html").read_text()).group(1)
    assert line == labs_quote
    assert "<figcaption>Andy Chen, Head of Robotics, Runway</figcaption>" in proof


def test_home_ends_on_the_line_to_for_labs(site: Path) -> None:
    main = _main((site / "index.html").read_text())
    last = '<p class="home-more">Running evals at scale? See <a href="/labs">For labs</a>.</p>'
    assert last in main
    assert main.rindex("</section>") < main.index(last)


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

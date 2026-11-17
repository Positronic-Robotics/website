"""The home page leads with the product; the old home page is the For labs page at /labs."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from conftest import PRICE_LIST, build_site

APP = "https://console.positronic.ro"
HEADLINE = "Test your physical AI on real robots and in sim."


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
        f'<section class="hero"><h1>{HEADLINE}</h1>'
        '<p class="hero-lede">Submit from your terminal. Get a video and a score for every episode.</p>'
        '<div class="actions">'
        f'<a class="act act-primary" href="{APP}/signin">Get started</a>'
        '<a class="act act-ghost" href="/labs#talk">Talk to us</a></div></section>'
    )


def test_home_sections_come_in_the_approved_order(site: Path) -> None:
    labels = [re.search(r'<span class="label">([^<]+)</span>', s) for s in _sections(site)[1:]]
    assert [m.group(1) for m in labels if m] == ["How it works", "Where it runs", "What you get back", "Proof"]


def test_how_it_works_shows_the_submit_command_from_the_client_guide(site: Path) -> None:
    band = _band(site, "How it works")
    assert re.findall(r'<span class="step-verb">([^<]+)</span>', band) == [
        "1. Sign up",
        "2. Submit with one command",
        "3. Watch the results",
    ]
    command = "uv run positronic eval run --eval=&lt;name&gt; --policy-image=org/policy@sha256:…"
    assert f'<pre class="cmd"><code>{command}</code></pre>' in band
    assert "{CLIENT_SUBMIT_COMMAND}" not in band
    assert f'href="{APP}/signin"' in band


def test_a_guide_with_no_submit_command_fails_the_build(tmp_path: Path) -> None:
    guide = tmp_path / "guide.md"
    guide.write_text("# A title\n\n## Registering\n\n```bash\nplatform-register\n```\n")
    result = build_site(tmp_path / "out", guide=guide)
    assert result.returncode != 0
    assert "positronic eval run" in result.stderr + result.stdout


def test_where_it_runs_prices_each_environment_from_the_price_list(site: Path) -> None:
    band = _band(site, "Where it runs")
    # The fixture: 1000 units a credit, $5 a credit. The rig episode is 2000 units; the
    # cheapest RoboLab episode 4 units, the cheapest MolmoSpaces episode 2 units.
    envs = re.findall(
        r'<li class="env"><span class="env-kind">([^<]+)</span><span class="env-name">([^<]+)</span>'
        r'<span class="env-price">([^<]+)</span></li>',
        band,
    )
    assert envs == [
        ("Real robot", "Franka DROID", "from $10 per episode"),
        ("Real robot", "Two-arm YAM", "from $10 per episode"),
        ("Simulator", "RoboLab", "from $0.02 per episode"),
        ("Simulator", "MolmoSpaces", "from $0.01 per episode"),
    ]
    assert '<a href="/pricing">' in band
    assert "{PRICE_ENVIRONMENTS}" not in band


def test_where_it_runs_lists_only_the_simulators_the_price_list_names(tmp_path: Path) -> None:
    price_list = json.loads(PRICE_LIST.read_text())
    price_list["sim"] = [line for line in price_list["sim"] if line["simulator"] == "robolab"]
    source = tmp_path / "pricing.json"
    source.write_text(json.dumps(price_list))
    build_site(tmp_path / "out", source).check_returncode()
    html = (tmp_path / "out" / "index.html").read_text()
    assert re.findall(r'<span class="env-name">([^<]+)</span>', html) == ["Franka DROID", "Two-arm YAM", "RoboLab"]


def test_what_you_get_back_is_one_public_phail_run(site: Path) -> None:
    band = _band(site, "What you get back")
    assert re.findall(r'<video [^>]*src="([^"]+)"', band) == ["https://phail.ai/api/episode/1086/video?v=d893698644b5bb11"]
    assert '<span class="run-task">Put the banana on the plate on the left</span>' in band
    assert '<span class="run-model">Ai2 MolmoAct2</span>' in band
    assert '<span class="run-score">Success in 13 s</span>' in band
    assert '<a href="https://phail.ai/benchmark/droid#episodes">' in band


def test_proof_links_the_leaderboard_and_quotes_runway_word_for_word(site: Path) -> None:
    band = _band(site, "Proof")
    line = re.search(r"<blockquote>([^<]+)</blockquote>", band).group(1)
    assert line == "Positronic lets us evaluate checkpoints continuously as we train, so we can course-correct our research quickly."
    labs_quote = re.search(r"<blockquote>([^<]+)</blockquote>", (site / "labs.html").read_text()).group(1)
    assert labs_quote.startswith(line + " ")
    assert "<figcaption>Andy Chen, Head of Robotics, Runway</figcaption>" in band
    assert 'href="https://phail.ai"' in band


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

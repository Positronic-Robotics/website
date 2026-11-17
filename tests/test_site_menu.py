"""The menu of every page, and the Pricing and Docs pages that it opens on the website."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from conftest import CONSOLE_SCRIPT, PRICE_LIST, build_site

ROOT = Path(__file__).resolve().parent.parent
APP = "https://console.positronic.ro"
PAGES = ["index.html", "labs.html", "pricing.html", "docs.html", "about.html", "blog.html", "privacy.html", "terms.html", "introducing-phail.html"]


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
            ("Docs", "https://positronic.ro/docs"),
            ("For labs", "https://positronic.ro/labs"),
            ("About", "https://positronic.ro/about"),
            ("Blog", "https://positronic.ro/blog"),
        ], page
        assert _links(app_nav) == [("Log in / Sign up", f"{APP}/signin")], page
        assert 'class="navbar-start"' in app_nav, page


def test_for_labs_is_current_only_on_the_labs_page(site: Path) -> None:
    for page in PAGES:
        site_nav = _block((site / page).read_text(), r'<nav aria-label="Site">.*?</nav>')
        current = re.findall(r'<a href="[^"]+" class="is-current" aria-current="page">([^<]+)</a>', site_nav)
        assert ("For labs" in current) == (page == "labs.html"), page


def test_the_logo_goes_home(site: Path) -> None:
    header = _block((site / "index.html").read_text(), r'<header class="navbar">.*?</header>')
    assert '<a href="https://positronic.ro/" class="navbar-brand">' in header


def test_only_sign_in_account_and_docs_links_leave_for_the_console(site: Path) -> None:
    # The terms define the console's pricing page by its address, so they keep that link.
    for page in (page for page in PAGES if page != "terms.html"):
        html = (site / page).read_text()
        assert "{APP_URL}" not in html, page
        console = set(re.findall(rf'href="{APP}(/[^"]*)"', html))
        assert console <= {"/signin", "/account"}, (page, console)


def test_pricing_centers_its_buttons_like_the_home_page(site: Path) -> None:
    hero = _block((site / "pricing.html").read_text(), r'<section class="page-head">.*?</section>')
    assert f'<div class="actions"><a class="act act-primary" href="{APP}/signin">Sign up</a>' in hero
    assert '<a class="act act-ghost" href="/labs#talk">Talk to us</a>' in hero
    css = (ROOT / "theme/positronic/static/css/platform.css").read_text()
    assert "justify-content: flex-start" not in css


GUIDE = "https://github.com/Positronic-Robotics/positronic/blob/main/client/README.md"


DOCS_SECTIONS = [("quick-start", "Quick start"), ("what-the-agent-does", "What the agent does"), ("full-guide", "Full guide")]


def test_docs_sections_take_the_label_rail_like_the_other_pages(site: Path) -> None:
    main = _block((site / "docs.html").read_text(), r"<main>.*?</main>")
    assert "docs-nav" not in main and "<h2" not in main
    sections = re.findall(
        r'<section class="band(?: close)?" id="([^"]+)"><div class="rail"><span class="label">([^<]+)'
        r'<a class="anchor" href="#([^"]+)" aria-label="Link to ([^"]+)">#</a></span></div><div class="col">', main)
    assert [(anchor, title) for anchor, title, _, _ in sections] == DOCS_SECTIONS
    assert all(anchor == target and title == label for anchor, title, target, label in sections)
    assert main.count('<section class="band') == len(DOCS_SECTIONS)


def test_docs_open_on_the_agent_quick_start(site: Path) -> None:
    main = _block((site / "docs.html").read_text(), r"<main>.*?</main>")
    assert main.index('id="quick-start"') < main.index('<div class="prompt">') < main.index('id="what-the-agent-does"')
    assert re.findall(r'<span class="step-verb">([^<]+)</span>', main) == ["1. Sign in", "2. Add credits", "3. Submit"]
    assert "Claude Code, Codex or another coding agent" in main


def test_docs_put_get_started_where_the_console_steps_were(site: Path) -> None:
    main = _block((site / "docs.html").read_text(), r"<main>.*?</main>")
    assert "Without an agent" not in main and f"{APP}/start" not in main
    cta = f'<div class="actions docs-cta"><a class="act act-primary" href="{APP}/signin">Get started</a></div>'
    assert main.index("</ol>") < main.index(cta) < main.index('id="full-guide"')


def test_docs_show_the_console_agent_prompt_with_a_copy_button(site: Path) -> None:
    html = (site / "docs.html").read_text()
    prompt = _block(html, r'<div class="prompt">.*?</div>')
    assert '<pre><code id="agent-prompt">Help me test a policy.\n1. Install the tool.\n2. Ask help@example.com for credits.</code></pre>' in prompt
    assert '<button class="act act-ghost prompt-copy" type="button" data-copy="agent-prompt">Copy</button>' in prompt
    assert "copy.js" in html
    assert "{AGENT_PROMPT}" not in html


def test_docs_link_the_full_guide_on_github_and_embed_none_of_it(site: Path) -> None:
    main = _block((site / "docs.html").read_text(), r"<main>.*?</main>")
    assert f'<a href="{GUIDE}">client/README.md</a>' in main
    assert "pf-guide" not in main and "Registering" not in main


def test_a_console_script_without_the_prompt_fails_the_build(tmp_path: Path) -> None:
    script = tmp_path / "console.js"
    script.write_text(CONSOLE_SCRIPT.read_text().replace("id:`agent-prompt`", "id:`other`"))
    result = build_site(tmp_path / "out", console_script=script)
    assert result.returncode != 0
    assert "agent-prompt" in result.stderr + result.stdout


def test_a_prompt_that_names_an_unknown_string_fails_the_build(tmp_path: Path) -> None:
    script = tmp_path / "console.js"
    script.write_text(CONSOLE_SCRIPT.read_text().replace("${hr}", "${zz}"))
    assert build_site(tmp_path / "out", console_script=script).returncode != 0


def test_an_unreadable_console_script_fails_the_build(tmp_path: Path) -> None:
    assert build_site(tmp_path / "out", console_script=tmp_path / "missing.js").returncode != 0


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


def test_pricing_names_volume_discounts_once_above_a_plain_talk_to_us_button(site: Path) -> None:
    html = (site / "pricing.html").read_text()
    head = _block(html, r'<section class="page-head">.*?</section>')
    assert "Volume discounts for committed spend.</p>" in head
    assert '<a class="act act-ghost" href="/labs#talk">Talk to us</a>' in head
    assert html.count("Volume discounts for committed spend.</p>") == 1


def test_pricing_does_not_name_the_credit_price(site: Path) -> None:
    html = (site / "pricing.html").read_text()
    assert "One credit is" not in html
    assert "{CREDIT_PRICE}" not in html


def test_pricing_shows_the_episode_total_in_the_accent_colour() -> None:
    css = (ROOT / "theme/positronic/static/css/platform.css").read_text()
    assert ".platform .pf-rates .pf-total { font-weight: 600; color: var(--accent, #b1e74f); }" in css


def test_pricing_keeps_each_figure_and_length_on_one_line() -> None:
    css = (ROOT / "theme/positronic/static/css/platform.css").read_text()
    assert ".platform .pf-rates td + td { white-space: nowrap; font-variant-numeric: tabular-nums; }" in css


def test_pricing_columns_have_fixed_widths(site: Path) -> None:
    html = (site / "pricing.html").read_text()
    cols = re.findall(r"<col(?: class=\"([^\"]+)\")?>", _block(html, r"<colgroup>.*?</colgroup>"))
    assert cols == ["", "pf-c-figure", "pf-c-op", "pf-c-figure", "pf-c-op", "pf-c-length", "pf-c-op", "pf-c-figure"]
    assert len(cols) == len(re.findall(r"<th[ >]", _block(html, r"<thead>.*?</thead>")))
    css = (ROOT / "theme/positronic/static/css/platform.css").read_text()
    assert ".platform .pf-rates { table-layout: fixed; }" in css


def test_pricing_writes_the_length_in_minutes_with_one_decimal(site: Path) -> None:
    html = (site / "pricing.html").read_text()
    lengths = re.findall(r'class="pf-length-value">([^<]+)<', html)
    assert lengths and set(lengths) == {"2.0 min"}
    script = (ROOT / "theme/positronic/static/js/pricing.js").read_text()
    assert 'return (seconds / 60).toFixed(1) + " min";' in script


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

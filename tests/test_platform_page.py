"""The /platform product page, its search and social tags, and the calls to action that lead to it."""

from __future__ import annotations

import re
from pathlib import Path

APP = "https://console.positronic.ro"
BOOKING = "https://calendar.notion.so/meet/sergeyarkhangelskiy/website-call"
NEED_SOMETHING_ELSE = (
    '<p class="act-alt">Need something else? Email <a href="mailto:hi@positronic.ro">hi@positronic.ro</a> '
    f'or <a href="{BOOKING}">book a meeting</a>.</p>'
)


def meta(html: str, attr: str, name: str) -> str:
    match = re.search(rf'<meta {attr}="{re.escape(name)}" content="([^"]*)"', html)
    assert match, name
    return match.group(1)


def test_platform_page_plays_the_launch_video(site: Path) -> None:
    html = (site / "platform.html").read_text()
    assert '<source src="/media/self-checkout-video.mp4" type="video/mp4">' in html
    assert 'poster="/media/self-checkout-video-poster.jpg"' in html
    assert (site / "media" / "self-checkout-video.mp4").is_file()
    assert (site / "media" / "self-checkout-video-poster.jpg").is_file()


def test_platform_page_opens_self_check_out_and_offers_a_person(site: Path) -> None:
    html = (site / "platform.html").read_text()
    assert "{APP_URL}" not in html
    assert html.count(f'<a class="act act-primary" href="{APP}/start">Evaluate your model</a>') == 2
    assert html.count(NEED_SOMETHING_ELSE) == 2


def test_platform_page_has_its_search_and_social_tags(site: Path) -> None:
    html = (site / "platform.html").read_text()
    assert "<title>Positronic Platform: test your robot model on our robots</title>" in html
    assert '<link rel="canonical" href="https://positronic.ro/platform" />' in html
    assert meta(html, "property", "og:url") == "https://positronic.ro/platform"
    assert len(meta(html, "name", "description")) <= 155
    assert meta(html, "property", "og:image") == "https://positronic.ro/media/self-checkout-video-poster.jpg"
    assert meta(html, "name", "twitter:card") == "summary_large_image"


def test_a_page_with_no_image_keeps_the_icon_as_its_small_card(site: Path) -> None:
    html = (site / "about.html").read_text()
    assert meta(html, "property", "og:image") == "https://positronic.ro/icon-512.png"
    assert meta(html, "name", "twitter:card") == "summary"


def test_platform_page_has_the_favicon(site: Path) -> None:
    html = (site / "platform.html").read_text()
    assert '<link rel="icon" href="/favicon.ico"' in html
    assert '<link rel="apple-touch-icon" href="/apple-touch-icon.png"' in html


def test_home_page_main_button_opens_self_check_out(site: Path) -> None:
    html = (site / "index.html").read_text()
    assert "{APP_URL}" not in html
    assert f'<a class="act act-primary" href="{APP}/start">Evaluate your model</a>' in html
    assert '<a class="act act-ghost" href="/platform">How it works</a>' in html
    assert NEED_SOMETHING_ELSE in html


def test_no_page_has_a_bare_send_or_submit_button(site: Path) -> None:
    for page in ("index.html", "about.html", "platform.html"):
        html = (site / page).read_text()
        assert not re.search(r">\s*(Send|Submit)\s*</(button|a)>", html), page


def test_sitemap_lists_the_platform_page(site: Path) -> None:
    assert "<loc>https://positronic.ro/platform</loc>" in (site / "sitemap.xml").read_text()


def test_a_blog_post_keeps_the_icon_as_its_small_card(site: Path) -> None:
    html = (site / "introducing-phail.html").read_text()
    assert meta(html, "property", "og:image") == "https://positronic.ro/icon-512.png"
    assert meta(html, "name", "twitter:card") == "summary"

"""The /platform product page and the home page button that leads to it."""

from __future__ import annotations

import re
from pathlib import Path

APP = "https://console.positronic.ro"


def test_platform_page_plays_the_launch_video(site: Path) -> None:
    html = (site / "platform.html").read_text()
    assert '<source src="/media/self-checkout-video.mp4" type="video/mp4">' in html
    assert 'poster="/media/self-checkout-video-poster.jpg"' in html
    assert (site / "media" / "self-checkout-video.mp4").is_file()
    assert (site / "media" / "self-checkout-video-poster.jpg").is_file()


def test_platform_page_links_the_web_app(site: Path) -> None:
    html = (site / "platform.html").read_text()
    assert "{APP_URL}" not in html
    assert f'<a class="act act-primary" href="{APP}/start">Get started</a>' in html
    assert f'<a class="act act-ghost" href="{APP}/pricing">See prices</a>' in html


def test_platform_page_has_the_favicon(site: Path) -> None:
    html = (site / "platform.html").read_text()
    assert '<link rel="icon" href="/favicon.ico"' in html
    assert '<link rel="apple-touch-icon" href="/apple-touch-icon.png"' in html


def test_home_page_has_a_button_to_the_platform_page(site: Path) -> None:
    html = (site / "index.html").read_text()
    assert re.search(r'<a class="act act-primary" href="/platform">Test your model on our robots</a>', html)


def test_sitemap_lists_the_platform_page(site: Path) -> None:
    assert "<loc>https://positronic.ro/platform</loc>" in (site / "sitemap.xml").read_text()

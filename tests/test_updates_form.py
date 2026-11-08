"""The "Keep in touch" form in the footer of every page, which posts its address straight to phail.ai."""

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


def _footer(html: str) -> str:
    match = re.search(r'<footer class="site-footer">.*?</footer>', html, re.DOTALL)
    assert match, "no footer"
    return match.group(0)


def test_every_page_footer_carries_the_same_form(site: Path) -> None:
    pages = [site / "index.html", site / "about.html", site / "privacy.html", site / "blog.html"]
    footers = {_footer(page.read_text()) for page in pages if page.exists()}
    assert len(footers) == 1
    [footer] = footers
    assert '<form class="updates-form" id="updates-form" method="post" action="https://phail.ai/api/subscribe"' in footer
    assert 'type="email" name="email"' in footer and 'name="company"' in footer
    assert "Unsubscribe anytime." in footer
    assert all("subscribe.js" in page.read_text() for page in pages if page.exists())


SCRIPT = ROOT / "theme" / "positronic" / "static" / "js" / "subscribe.js"


def test_the_form_script_posts_to_the_form_action_and_reports_no_analytics_event() -> None:
    script = SCRIPT.read_text()
    assert "fetch(form.action," in script
    assert "plausible" not in script and "gtag" not in script


def test_no_function_stands_between_the_form_and_phail() -> None:
    assert not (ROOT / "functions" / "api" / "subscribe.js").exists()


def test_the_privacy_policy_names_the_updates_list(site: Path) -> None:
    policy = (site / "privacy.html").read_text()
    assert "Updates list" in policy
    assert "Keep in touch" in policy

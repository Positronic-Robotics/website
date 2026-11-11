"""The "Keep in touch" form in the footer of every page, which posts its address straight to phail.ai."""

from __future__ import annotations

import html
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
    assert "novalidate" not in footer  # the browser checks the address when the script does not run
    assert 'type="email" name="email"' in footer and 'name="company"' in footer
    assert "Unsubscribe anytime." in footer
    assert all("subscribe.js" in page.read_text() for page in pages if page.exists())


SCRIPT = ROOT / "theme" / "positronic" / "static" / "js" / "subscribe.js"

# Must equal VALID_EMAIL in phail.ai's phail/interest.py, which refuses any other address with 400.
PHAIL_EMAIL_PATTERN = r"[A-Za-z0-9_][A-Za-z0-9_.%+'\-]*@[A-Za-z0-9_\-]+(\.[A-Za-z0-9_\-]+)+"


def test_the_address_field_checks_the_rule_phail_checks(site: Path) -> None:
    field = re.search(r'<input type="email" name="email" id="updates-email"[^>]*>', _footer((site / "index.html").read_text()))
    assert field, "no address field"
    assert html.unescape(re.search(r'pattern="([^"]*)"', field.group(0)).group(1)) == PHAIL_EMAIL_PATTERN


def test_the_form_script_posts_to_the_form_action_and_reports_no_analytics_event() -> None:
    script = SCRIPT.read_text()
    assert "fetch(form.action," in script
    assert "noValidate" not in script  # the browser's email check runs before the submit event
    assert "plausible" not in script and "gtag" not in script


def test_no_function_stands_between_the_form_and_phail() -> None:
    assert not (ROOT / "functions" / "api" / "subscribe.js").exists()


def test_the_privacy_policy_names_the_updates_list(site: Path) -> None:
    policy = (site / "privacy.html").read_text()
    assert "Updates list" in policy
    assert "Keep in touch" in policy


def test_the_privacy_policy_names_the_sheet_copy_of_the_updates_list(site: Path) -> None:
    policy = (site / "privacy.html").read_text()
    assert "copy of the list in a Google Sheet" in policy
    assert "a copy of the updates list" in policy

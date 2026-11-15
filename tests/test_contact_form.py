"""The contact form asks where the visitor heard of us, and the browser posts the lead with the answer to phail.ai."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

# Must equal HEARD_FROM_CHANNELS in phail.ai's phail/interest.py, which stores the lead.
CHANNELS = [
    "linkedin",
    "x",
    "search",
    "referral",
    "event",
    "media",
    "other",
]


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


def _form(html: str) -> str:
    match = re.search(r'<form class="contact" id="contact-form">.*?</form>', html, re.S)
    assert match, "no contact form"
    return match.group(0)


def test_home_and_about_carry_the_same_form(site: Path) -> None:
    assert _form((site / "index.html").read_text()) == _form((site / "about.html").read_text())


def test_the_form_asks_the_channel_as_a_required_dropdown_above_the_fields(site: Path) -> None:
    form = _form((site / "index.html").read_text())
    heard = re.search(r'<div class="contact-heard">(.*?)</div>', form, re.S)
    assert heard, "no channel dropdown"
    select = re.search(r'<select id="contact-heard" name="heard_from" required>(.*?)</select>', heard.group(1), re.S)
    assert select, "the channel dropdown is not required"
    assert select.group(1).startswith('<option value="" disabled selected>')
    assert re.findall(r'<option value="([^"]+)">', select.group(1)) == CHANNELS
    detail = re.search(r'<input [^>]*name="heard_from_detail"[^>]*>', heard.group(1))
    assert detail, "no detail field for Other"
    assert "required" not in detail.group(0)
    assert form.index("contact-heard") < form.index('name="email"')


SCRIPT = ROOT / "theme" / "positronic" / "static" / "js" / "contact.js"


def test_the_browser_posts_the_lead_straight_to_phail_with_its_source_and_page() -> None:
    script = SCRIPT.read_text()
    assert 'var LEADS_URL = "https://phail.ai/api/interest";' in script
    assert "fetch(LEADS_URL," in script
    assert 'body.source = "positronic-home";' in script
    assert "body.page = window.location.pathname;" in script


def test_no_function_stands_between_the_form_and_phail() -> None:
    assert not (ROOT / "functions" / "api" / "contact.js").exists()

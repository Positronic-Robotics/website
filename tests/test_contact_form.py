"""The contact form asks where the visitor heard of us, and the lead carries the answer to phail.ai."""

from __future__ import annotations

import json
import re
import shutil
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


def test_the_form_offers_every_channel_and_an_unanswered_default(site: Path) -> None:
    form = _form((site / "index.html").read_text())
    select = re.search(r'<select id="contact-heard" name="heard_from">(.*?)</select>', form, re.S)
    assert select, "no channel selector"
    values = re.findall(r'<option value="([^"]*)"', select.group(1))
    assert values == ["", *CHANNELS]
    assert "required" not in select.group(0)
    assert 'name="heard_from_detail"' in form


RUNNER = """
import { onRequestPost } from "./contact.mjs";
const sent = [];
globalThis.fetch = async (url, init) => { sent.push(JSON.parse(init.body)); return new Response("{}"); };
const [body, referer] = process.argv.slice(2);
const headers = referer ? { referer } : {};
const request = new Request("https://positronic.ro/api/contact", { method: "POST", body, headers });
const response = await onRequestPost({ request });
console.log(JSON.stringify({ status: response.status, sent }));
"""


def _post(tmp_path: Path, body: dict, referer: str = "") -> dict:
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is not installed")
    shutil.copy(ROOT / "functions" / "api" / "contact.js", tmp_path / "contact.mjs")
    (tmp_path / "run.mjs").write_text(RUNNER)
    out = subprocess.run(
        [node, "run.mjs", json.dumps(body), referer], cwd=tmp_path, capture_output=True, text=True, check=True
    )
    return json.loads(out.stdout)


def _arrival(first_source: str, last_source: str) -> dict:
    fields = {}
    for which, source in (("first", first_source), ("last", last_source)):
        for field in ("utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "referrer", "landing_page", "at"):
            fields[f"{which}_{field}"] = ""
        fields[f"{which}_utm_source"] = source
    return fields


def test_the_function_forwards_the_channel_and_both_arrivals(tmp_path: Path) -> None:
    body = {
        "email": "lead@lab.example.edu",
        "note": "hi",
        "heard_from": "other",
        "heard_from_detail": " CoRL booth ",
        **_arrival("linkedin", "newsletter"),
        "first_referrer": "https://www.linkedin.com/",
        "last_landing_page": "/blog",
    }
    result = _post(tmp_path, body, referer="https://positronic.ro/about?utm_source=x")
    assert result["status"] == 200
    [lead] = result["sent"]
    assert lead["source"] == "positronic-home"
    assert lead["heard_from"] == "other"
    assert lead["heard_from_detail"] == "CoRL booth"
    assert lead["page"] == "/about"
    assert lead["first_utm_source"] == "linkedin"
    assert lead["first_referrer"] == "https://www.linkedin.com/"
    assert lead["last_utm_source"] == "newsletter"
    assert lead["last_landing_page"] == "/blog"
    assert lead["last_utm_term"] == ""


def test_the_function_forwards_no_field_outside_the_lead(tmp_path: Path) -> None:
    [lead] = _post(tmp_path, {"email": "lead@lab.example.edu", "utm_source": "x", "referrer": "y", "admin": 1})["sent"]
    assert not {"utm_source", "referrer", "admin"} & lead.keys()
    assert lead["first_utm_source"] == ""
    assert lead["page"] == ""


def test_the_function_sends_empty_strings_for_a_field_that_is_not_text(tmp_path: Path) -> None:
    result = _post(tmp_path, {"email": "lead@lab.example.edu", "heard_from": ["x"], "first_referrer": 5})
    [lead] = result["sent"]
    assert lead["heard_from"] == ""
    assert lead["first_referrer"] == ""

"""The "Keep in touch" form in the footer of every page, and the function that hands its address to phail.ai."""

from __future__ import annotations

import json
import re
import shutil
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
    match = re.search(r'<footer class="site-footer">.*?</footer>', html, re.S)
    assert match, "no footer"
    return match.group(0)


def test_every_page_footer_carries_the_same_form(site: Path) -> None:
    pages = [site / "index.html", site / "about.html", site / "privacy.html", site / "blog.html"]
    footers = {_footer(page.read_text()) for page in pages if page.exists()}
    assert len(footers) == 1
    [footer] = footers
    assert '<form class="updates-form" id="updates-form" method="post" action="/api/subscribe"' in footer
    assert 'type="email" name="email"' in footer and 'name="company"' in footer
    assert "Unsubscribe anytime." in footer
    assert all("subscribe.js" in page.read_text() for page in pages if page.exists())


def test_the_form_script_reports_no_analytics_event() -> None:
    script = (ROOT / "theme" / "positronic" / "static" / "js" / "subscribe.js").read_text()
    assert "plausible" not in script and "gtag" not in script


def test_the_privacy_policy_names_the_updates_list(site: Path) -> None:
    policy = (site / "privacy.html").read_text()
    assert "Updates list" in policy
    assert "Keep in touch" in policy


RUNNER = """
import { onRequestPost } from "./subscribe.mjs";
const sent = [];
const [body, upstreamStatus, contentType] = process.argv.slice(2);
globalThis.fetch = async (url, init) => { sent.push({ url, body: JSON.parse(init.body) }); return new Response("{}", { status: Number(upstreamStatus) }); };
const headers = contentType ? { "content-type": contentType } : {};
const request = new Request("https://positronic.ro/api/subscribe", { method: "POST", body, headers });
const response = await onRequestPost({ request });
console.log(JSON.stringify({ status: response.status, text: await response.text(), sent }));
"""


def _post(tmp_path: Path, body: object, upstream_status: int = 200, content_type: str = "") -> dict:
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is not installed")
    shutil.copy(ROOT / "functions" / "api" / "subscribe.js", tmp_path / "subscribe.mjs")
    (tmp_path / "run.mjs").write_text(RUNNER)
    raw = body if isinstance(body, str) else json.dumps(body)
    out = subprocess.run(
        [node, "run.mjs", raw, str(upstream_status), content_type],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(out.stdout)


def test_the_function_sends_only_the_address_to_phail(tmp_path: Path) -> None:
    result = _post(tmp_path, {"email": " reader@lab.example.edu ", "note": "x", "admin": 1})
    assert result["status"] == 200
    assert result["sent"] == [{"url": "https://phail.ai/api/subscribe", "body": {"email": "reader@lab.example.edu"}}]


def test_a_form_the_browser_posts_without_script_is_sent_and_answered_in_text(tmp_path: Path) -> None:
    form = "company=&email=reader%40lab.example.edu"
    result = _post(tmp_path, form, content_type="application/x-www-form-urlencoded")
    assert result["status"] == 200
    assert result["text"] == "Thanks, you are on the list."
    assert [s["body"] for s in result["sent"]] == [{"email": "reader@lab.example.edu"}]


@pytest.mark.parametrize("body", [{"email": "no-at-sign"}, {"email": 5}, {}, "[1]", "not json"])
def test_the_function_refuses_a_body_with_no_address_and_sends_nothing(tmp_path: Path, body: object) -> None:
    result = _post(tmp_path, body)
    assert result["status"] == 400
    assert result["sent"] == []


def test_a_bot_that_fills_the_hidden_field_is_answered_and_nothing_is_sent(tmp_path: Path) -> None:
    result = _post(tmp_path, {"email": "bot@spam.example.com", "company": "Acme"})
    assert result["status"] == 200
    assert result["sent"] == []


@pytest.mark.parametrize(("upstream", "answer"), [(429, 429), (503, 502), (400, 502)])
def test_a_refusal_from_phail_is_a_failure_for_the_visitor(tmp_path: Path, upstream: int, answer: int) -> None:
    assert _post(tmp_path, {"email": "reader@lab.example.edu"}, upstream)["status"] == answer

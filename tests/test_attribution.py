"""attribution.js keeps the visitor's first arrival and replaces the last one only with a new arrival."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "theme" / "positronic" / "static" / "js" / "attribution.js"

# Runs attribution.js once per view in a fake browser that keeps localStorage across the views.
RUNNER = """
import { readFileSync } from "node:fs";
const source = readFileSync(process.argv[2], "utf8");
const views = JSON.parse(process.argv[3]);
const store = new Map(Object.entries(JSON.parse(process.argv[4])));
const blocked = process.argv[5] === "blocked";
const localStorage = {
  getItem: (k) => { if (blocked) throw new Error("blocked"); return store.has(k) ? store.get(k) : null; },
  setItem: (k, v) => { if (blocked) throw new Error("blocked"); store.set(k, String(v)); },
};
let result;
for (const [url, referrer] of views) {
  const u = new URL(url);
  const window = { location: { search: u.search, host: u.host, pathname: u.pathname } };
  new Function("window", "document", "localStorage", source)(window, { referrer }, localStorage);
  result = { fields: window.positronicArrival.fields(), sources: window.positronicArrival.sources() };
}
console.log(JSON.stringify(result));
"""


def _run(tmp_path: Path, views: list[tuple[str, str]], stored: dict | None = None, blocked: bool = False) -> dict:
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is not installed")
    (tmp_path / "run.mjs").write_text(RUNNER)
    args = [node, "run.mjs", str(SCRIPT), json.dumps(views), json.dumps(stored or {}), "blocked" if blocked else ""]
    out = subprocess.run(args, cwd=tmp_path, capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


LINKEDIN = ("https://positronic.ro/?utm_source=linkedin&utm_medium=social&utm_campaign=launch", "")


def test_a_tagged_landing_is_both_the_first_and_the_last_arrival(tmp_path: Path) -> None:
    fields = _run(tmp_path, [LINKEDIN])["fields"]
    assert fields["first_utm_source"] == fields["last_utm_source"] == "linkedin"
    assert fields["first_utm_campaign"] == "launch"
    assert fields["first_landing_page"] == "/"
    assert fields["first_at"]


def test_a_later_arrival_from_another_site_replaces_the_last_and_keeps_the_first(tmp_path: Path) -> None:
    result = _run(tmp_path, [LINKEDIN, ("https://positronic.ro/blog", "https://www.google.com/")])
    fields = result["fields"]
    assert fields["first_utm_source"] == "linkedin"
    assert fields["last_utm_source"] == ""
    assert fields["last_referrer"] == "https://www.google.com/"
    assert fields["last_landing_page"] == "/blog"
    assert result["sources"] == {"first_source": "linkedin", "last_source": "www.google.com"}


def test_a_direct_view_or_a_page_of_the_same_site_replaces_nothing(tmp_path: Path) -> None:
    views = [LINKEDIN, ("https://positronic.ro/about", "https://positronic.ro/"), ("https://positronic.ro/blog", "")]
    fields = _run(tmp_path, views)["fields"]
    assert fields["last_utm_source"] == "linkedin"
    assert fields["last_landing_page"] == "/"


def test_a_return_from_a_sign_in_provider_is_not_an_arrival(tmp_path: Path) -> None:
    views = [LINKEDIN, ("https://positronic.ro/", "https://auth.workos.com/"), ("https://positronic.ro/", "https://accounts.google.com/")]
    assert _run(tmp_path, views)["fields"]["last_utm_source"] == "linkedin"


def test_a_host_that_only_ends_like_a_sign_in_provider_is_an_arrival(tmp_path: Path) -> None:
    fields = _run(tmp_path, [LINKEDIN, ("https://positronic.ro/", "https://notworkos.com/")])["fields"]
    assert fields["last_referrer"] == "https://notworkos.com/"


def test_a_direct_first_visit_is_the_first_arrival_with_its_landing_page(tmp_path: Path) -> None:
    result = _run(tmp_path, [("https://positronic.ro/about", "")])
    assert result["fields"]["first_landing_page"] == "/about"
    assert result["sources"] == {"first_source": "direct", "last_source": "direct"}


def test_a_first_arrival_older_than_90_days_starts_over(tmp_path: Path) -> None:
    old = {k: "" for k in ("utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "referrer")}
    old.update(utm_source="flyer", landing_page="/", at="2020-01-01T00:00:00.000Z")
    stored = {"positronic-arrival": json.dumps({"first": old, "last": old})}
    fields = _run(tmp_path, [("https://positronic.ro/", "")], stored)["fields"]
    assert fields["first_utm_source"] == ""
    assert fields["first_at"] != old["at"]


def test_blocked_storage_still_gives_the_landing_page_arrival(tmp_path: Path) -> None:
    fields = _run(tmp_path, [LINKEDIN], blocked=True)["fields"]
    assert fields["first_utm_source"] == "linkedin"


@pytest.mark.parametrize("script", sorted((ROOT / "theme" / "positronic" / "static" / "js").glob("*.js")), ids=lambda p: p.name)
def test_every_page_script_parses(script: Path) -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is not installed")
    subprocess.run([node, "--check", str(script)], check=True)

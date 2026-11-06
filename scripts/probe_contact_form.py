#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright>=1.48"]
# ///
"""Fill the contact form of a built or live site in a headless browser and print the request it sends.

Usage
  scripts/probe_contact_form.py http://localhost:8000                 # stub the API, send nothing
  scripts/probe_contact_form.py http://localhost:8000 --before '/blog.html?utm_source=linkedin' \
      --referrer https://www.google.com/                              # an earlier arrival, then the form
  scripts/probe_contact_form.py https://positronic.ro --submit \\
      --email test+source@positronic.ro --note "TEST - lead source selector"

Without `--submit` the probe answers the form's POST itself, so no lead is recorded. The page opens
with UTM tags in its address; attribution.js records them as the first and last arrival, and the form
posts them as first_* and last_* fields, which the probe prints.
"""

import argparse
import json

from playwright.sync_api import Route, sync_playwright

TAGS = "utm_source=probe&utm_medium=test&utm_campaign=lead-source-probe"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url")
    parser.add_argument("--page", default="/")
    parser.add_argument("--submit", action="store_true", help="let the POST reach the server")
    parser.add_argument("--email", default="probe@example.com")
    parser.add_argument("--note", default="TEST - lead source selector")
    parser.add_argument("--channel", default="other")
    parser.add_argument("--detail", default="probe")
    parser.add_argument("--before", action="append", default=[], help="a page to visit before the form page")
    parser.add_argument("--referrer", help="the referrer of the form page's visit")
    args = parser.parse_args()

    sent: list[dict] = []

    def capture(route: Route) -> None:
        sent.append(
            {"referer": route.request.headers.get("referer", ""), "body": json.loads(route.request.post_data or "{}")}
        )
        if args.submit:
            route.continue_()
        else:
            route.fulfill(status=200, content_type="application/json", body='{"ok": true}')

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.route("**/api/contact", capture)
        for before in args.before:
            page.goto(f"{args.base_url.rstrip('/')}{before}")
        page.goto(f"{args.base_url.rstrip('/')}{args.page}?{TAGS}#talk", referer=args.referrer)
        form = page.locator("#contact-form")
        detail = form.locator("input[name=heard_from_detail]")
        print("detail field visible before a pick:", detail.is_visible())
        form.locator("input[name=email]").fill(args.email)
        form.locator("textarea[name=note]").fill(args.note)
        form.locator("select[name=heard_from]").select_option(args.channel)
        print("detail field visible after the pick:", detail.is_visible())
        if detail.is_visible():
            detail.fill(args.detail)
        form.locator("button[type=submit]").click()
        page.wait_for_function(
            "document.querySelector('.contact-status').textContent.startsWith('Got it') || "
            "document.querySelector('.contact-status').classList.contains('is-error')"
        )
        print("status:", page.locator(".contact-status").text_content())
        browser.close()

    print("request sent:", json.dumps(sent, indent=2))


if __name__ == "__main__":
    main()

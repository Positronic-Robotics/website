#!/usr/bin/env python3
"""Compare the price examples on the /platform page with the live price list of the platform.

Usage
  scripts/check_platform_prices.py                              # the page source in this checkout
  scripts/check_platform_prices.py https://positronic.ro/platform

It prints each figure the page must show, and exits 1 when the page does not show one of them.
"""

from __future__ import annotations

import json
import math
import sys
import urllib.request
from pathlib import Path

PRICE_LIST = "https://console.positronic.ro/api/pricing.get"
PAGE = Path(__file__).resolve().parent.parent / "content" / "pages" / "platform.md"


def _get(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "positronic-website-price-check"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode()


def expected_figures(prices: dict) -> list[str]:
    per_credit = prices["units_per_credit"]
    dollars = prices["credit_price"]["unit_amount_minor"] / 100
    rig = prices["rig"]
    fee = rig["episode_units"] / per_credit
    per_minute = rig["units_per_hour"] / 60 / per_credit
    franka = 10 * (fee + 1 * per_minute)
    yam = 4 * (fee + 2 * per_minute)
    robolab = next(e for e in prices["sim_examples"] if e["simulator"] == "robolab" and e["hosting"] == "hosted")
    robolab_credits = robolab["credit_units"] / per_credit
    return [
        f"A credit is ${dollars:g}",
        f"{prices['credit_price']['min_credits']} to {prices['credit_price']['max_credits']:,} credits",
        f"{franka:g} credits",
        f"${franka * dollars:g}",
        f"{yam:g} credits",
        f"${yam * dollars:g}",
        f"{robolab['episodes']} RoboLab episodes",
        f"about {round(robolab_credits)} credits",
        f"about ${math.ceil(robolab_credits) * dollars:g}",
    ]


def main() -> int:
    page = _get(sys.argv[1]) if len(sys.argv) > 1 else PAGE.read_text()
    missing = 0
    for figure in expected_figures(json.loads(_get(PRICE_LIST))):
        found = figure in page
        missing += not found
        print(f"{'ok' if found else 'MISSING'}  {figure}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())

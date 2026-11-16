"""Renders the Pricing page's rate table from the console's public price list, read once per build.

The console serves the list at `<APP_URL>/api/pricing.get` with no key, and its own Pricing page reads
the same list, so the website carries no copy of a price. `PRICING_SOURCE` names another URL or a local
JSON file (the tests pass a fixture). A failed read, or a simulator or hosting with no display name,
fails the build.
"""

from __future__ import annotations

import json
import urllib.request
from decimal import Decimal
from pathlib import Path

from pelican import signals

RATES_PLACEHOLDER = "{PRICE_RATES}"
CREDIT_PRICE_PLACEHOLDER = "{CREDIT_PRICE}"
DEFAULT_LENGTH_SEC = 120

SIMULATOR_NAMES = {"molmospaces": "MolmoSpaces", "robolab": "RoboLab"}
HOSTING_SUFFIX = {"hosted": "", "own_server": ", model on your server"}
RIG_NAMES = ["Real robot: Franka DROID", "Real robot: two-arm YAM"]

_price_list: dict | None = None


def read_price_list(source: str) -> dict:
    if source.startswith(("https://", "http://")):
        with urllib.request.urlopen(source, timeout=30) as response:
            return json.load(response)
    return json.loads(Path(source).read_text())


def _dollars(units: int, price_list: dict) -> Decimal:
    credit_price = price_list["credit_price"]
    if credit_price["currency"] != "usd":
        raise ValueError(f"the price list is in {credit_price['currency']}, the page shows dollars")
    return Decimal(units) / Decimal(price_list["units_per_credit"]) * Decimal(credit_price["unit_amount_minor"]) / 100


def _plain(amount: Decimal) -> str:
    return f"${amount.normalize():f}"


def money(amount: Decimal) -> str:
    """The total as the page's slider script writes it: cents from $1 up, else two significant digits."""
    if amount >= 1:
        return "$" + f"{amount:.2f}".removesuffix(".00")
    return f"${float(f'{amount:.2g}'):g}"


def _row(name: str, episode: Decimal, minute: Decimal) -> str:
    total = episode + minute * DEFAULT_LENGTH_SEC / 60
    op = '<td class="pf-op">{}</td>'.format
    return (
        f'<tr data-episode="{episode.normalize():f}" data-minute="{minute.normalize():f}"><td>{name}</td>'
        f"<td>{_plain(episode)}</td>{op('+')}<td>{_plain(minute)}</td>{op('×')}"
        f'<td class="pf-length-value">2 min</td>{op("=")}<td class="pf-total">{money(total)}</td></tr>'
    )


def rate_rows(price_list: dict) -> str:
    rig = price_list["rig"]
    rig_episode = _dollars(rig["episode_units"], price_list)
    rig_minute = _dollars(rig["units_per_hour"], price_list) / 60
    rows = [_row(name, rig_episode, rig_minute) for name in RIG_NAMES]
    for line in price_list["sim"]:
        simulator, hosting = line["simulator"], line["hosting"]
        if simulator not in SIMULATOR_NAMES:
            raise ValueError(f"the price list names simulator {simulator!r}, which has no display name")
        if hosting not in HOSTING_SUFFIX:
            raise ValueError(f"the price list names hosting {hosting!r}, which has no display name")
        name = f"{SIMULATOR_NAMES[simulator]} simulator{HOSTING_SUFFIX[hosting]}"
        price = line["price"]
        rows.append(_row(name, _dollars(price["episode_units"], price_list), _dollars(price["minute_units"], price_list)))
    return "".join(rows)


def credit_price(price_list: dict) -> str:
    return _plain(_dollars(price_list["units_per_credit"], price_list))


def _read(pelican) -> None:
    global _price_list
    settings = pelican.settings
    _price_list = read_price_list(settings.get("PRICING_SOURCE") or f"{settings['APP_URL']}/api/pricing.get")
    rate_rows(_price_list)  # fail the build before any page is written


def _fill(content) -> None:
    text = getattr(content, "_content", None)
    if not text or RATES_PLACEHOLDER not in text:
        return
    assert _price_list is not None
    content._content = text.replace(RATES_PLACEHOLDER, rate_rows(_price_list)).replace(
        CREDIT_PRICE_PLACEHOLDER, credit_price(_price_list)
    )


def register() -> None:
    signals.initialized.connect(_read)
    signals.content_object_init.connect(_fill)

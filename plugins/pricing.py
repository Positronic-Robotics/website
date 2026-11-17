"""Renders the Pricing page's rate table from the console's public price list, read once per build.

The console serves the list at `<APP_URL>/api/pricing.get` with no key, and its own Pricing page reads
the same list, so the website carries no copy of a price. `PRICING_SOURCE` names another URL or a local
JSON file (the tests pass a fixture). The home page lists each environment at the cost of one episode
of the default length, from the same list and the same math. A failed read, or a simulator or hosting
with no display name, fails the build.
"""

from __future__ import annotations

import json
import urllib.request
from decimal import Decimal
from pathlib import Path

from pelican import signals

RATES_PLACEHOLDER = "{PRICE_RATES}"
ENVIRONMENTS_PLACEHOLDER = "{PRICE_ENVIRONMENTS}"
DEFAULT_LENGTH_SEC = 120

SIMULATOR_NAMES = {"robolab": "RoboLab", "molmospaces": "MolmoSpaces"}
HOSTING_SUFFIX = {"hosted": "", "own_server": ", model on your server"}
RIG_NAMES = ["Real robot: Franka DROID", "Real robot: two-arm YAM"]
ROBOT_NAMES = ["Franka FR3 (DROID)", "Bimanual YAM"]

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


def episode_total(episode: Decimal, minute: Decimal) -> Decimal:
    """One episode of the default length: the Pricing page's total and the home page's figure."""
    return episode + minute * DEFAULT_LENGTH_SEC / 60


def _row(name: str, episode: Decimal, minute: Decimal) -> str:
    op = '<td class="pf-op">{}</td>'.format
    return (
        f'<tr data-episode="{episode.normalize():f}" data-minute="{minute.normalize():f}"><td>{name}</td>'
        f"<td>{_plain(episode)}</td>{op('+')}<td>{_plain(minute)}</td>{op('×')}"
        f'<td class="pf-length-value">2 min</td>{op("=")}<td class="pf-total">{money(episode_total(episode, minute))}</td></tr>'
    )


def _rig_rates(price_list: dict) -> tuple[Decimal, Decimal]:
    rig = price_list["rig"]
    return _dollars(rig["episode_units"], price_list), _dollars(rig["units_per_hour"], price_list) / 60


def _sim_rates(line: dict, price_list: dict) -> tuple[Decimal, Decimal]:
    price = line["price"]
    return _dollars(price["episode_units"], price_list), _dollars(price["minute_units"], price_list)


def rate_rows(price_list: dict) -> str:
    rows = [_row(name, *_rig_rates(price_list)) for name in RIG_NAMES]
    for line in price_list["sim"]:
        simulator, hosting = line["simulator"], line["hosting"]
        if simulator not in SIMULATOR_NAMES:
            raise ValueError(f"the price list names simulator {simulator!r}, which has no display name")
        if hosting not in HOSTING_SUFFIX:
            raise ValueError(f"the price list names hosting {hosting!r}, which has no display name")
        name = f"{SIMULATOR_NAMES[simulator]} simulator{HOSTING_SUFFIX[hosting]}"
        rows.append(_row(name, *_sim_rates(line, price_list)))
    return "".join(rows)


def _read(pelican) -> None:
    global _price_list
    settings = pelican.settings
    _price_list = read_price_list(settings.get("PRICING_SOURCE") or f"{settings['APP_URL']}/api/pricing.get")
    rate_rows(_price_list)  # fail the build before any page is written


def _fill(content) -> None:
    text = getattr(content, "_content", None)
    if not text or not (RATES_PLACEHOLDER in text or ENVIRONMENTS_PLACEHOLDER in text):
        return
    assert _price_list is not None
    text = text.replace(RATES_PLACEHOLDER, rate_rows(_price_list))
    content._content = text.replace(ENVIRONMENTS_PLACEHOLDER, environments(_price_list))


def _environment(kind: str, name: str, total: Decimal) -> str:
    return (
        f'<li class="env"><span class="env-kind">{kind}</span><span class="env-name">{name}</span>'
        f'<span class="env-price">from {money(total)} per {DEFAULT_LENGTH_SEC // 60}-min episode</span></li>'
    )


def environments(price_list: dict) -> str:
    """The home page list: the real robots, then each simulator in the list at its cheapest hosting."""
    rig_total = episode_total(*_rig_rates(price_list))
    items = [_environment("Real robot", name, rig_total) for name in ROBOT_NAMES]
    for simulator, name in SIMULATOR_NAMES.items():
        totals = [episode_total(*_sim_rates(line, price_list)) for line in price_list["sim"] if line["simulator"] == simulator]
        if totals:
            items.append(_environment("Simulator", name, min(totals)))
    return "".join(items)


def register() -> None:
    signals.initialized.connect(_read)
    signals.content_object_init.connect(_fill)

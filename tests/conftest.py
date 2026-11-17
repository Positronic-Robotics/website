"""One build of the site for every test module, from a fake price list and a fake console script, so no test reads the network."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRICE_LIST = ROOT / "tests/fixtures/pricing.json"
CONSOLE_SCRIPT = ROOT / "tests/fixtures/console_script.js"


def build_site(out: Path, price_list: Path = PRICE_LIST, console_script: Path = CONSOLE_SCRIPT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pelican", "content", "-s", "publishconf.py", "-o", str(out), "-q"],
        cwd=ROOT,
        env={
            "PYTHONPATH": str(ROOT),
            "PATH": os.environ.get("PATH", ""),
            "PRICING_SOURCE": str(price_list),
            "AGENT_PROMPT_SOURCE": str(console_script),
        },
        capture_output=True,
        text=True,
        check=False,
    )

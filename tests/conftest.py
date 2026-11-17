"""One build of the site for every test module, from a fake price list and a fake client guide, so no test reads the network."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRICE_LIST = ROOT / "tests/fixtures/pricing.json"
CLIENT_GUIDE = ROOT / "tests/fixtures/client_guide.md"
GUIDE_REF = "v9.9.9"


def build_site(out: Path, price_list: Path = PRICE_LIST, guide: Path = CLIENT_GUIDE) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pelican", "content", "-s", "publishconf.py", "-o", str(out), "-q"],
        cwd=ROOT,
        env={
            "PYTHONPATH": str(ROOT),
            "PATH": os.environ.get("PATH", ""),
            "PRICING_SOURCE": str(price_list),
            "DOCS_SOURCE": str(guide),
            "DOCS_REF": GUIDE_REF,
        },
        capture_output=True,
        text=True,
        check=False,
    )

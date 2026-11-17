"""Shows the console's coding-agent prompt on the Docs page, read from the live console once per build.

The console's Get started page shows the prompt in the element with id `agent-prompt`. The console is
a single-page app, so the build reads its script: the page names it, the element's `text` names the
variable that holds the prompt, and the variable is a list of lines joined by newlines. A
`${name}` in a line takes the text of the plain string `name`. `AGENT_PROMPT_SOURCE` names a local
script instead (the tests pass a fixture). A failed read, or a script in another shape, fails the
build, so the page never shows a stale prompt.
"""

from __future__ import annotations

import html
import re
import urllib.request
from pathlib import Path

from pelican import signals

PLACEHOLDER = "{AGENT_PROMPT}"
_LITERAL = r"`((?:[^`\\]|\\.)*)`"

_prompt: str | None = None


def _get(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "positronic-website-build"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode()


def console_script(app_url: str) -> str:
    page = _get(f"{app_url}/")
    match = re.search(r'<script[^>]*\ssrc="(/assets/[^"]+\.js)"', page)
    if not match:
        raise ValueError(f"{app_url}/ names no script")
    return _get(app_url + match.group(1))


def _unescape(text: str) -> str:
    return re.sub(r"\\(.)", lambda m: "\n" if m.group(1) == "n" else m.group(1), text)


def agent_prompt(script: str) -> str:
    """The prompt as the console shows it, read from the console's script."""
    element = re.search(r"id:`agent-prompt`.{0,200}?text:([\w$]+)", script, re.DOTALL)
    if not element:
        raise ValueError("the console script has no agent-prompt element")
    name = re.escape(element.group(1))
    lines = re.search(rf"(?<![\w$]){name}=\[((?:{_LITERAL},?)+)\]\.join\({_LITERAL}\)", script)
    if not lines:
        raise ValueError(f"the agent prompt {element.group(1)} is not a list of lines")
    parts = [_unescape(part) for part in re.findall(_LITERAL, lines.group(1))]
    prompt = _unescape(lines.group(lines.lastindex)).join(parts)

    def value(reference: re.Match[str]) -> str:
        found = set(re.findall(rf"(?<![\w$]){re.escape(reference.group(1))}=`([^`$\\]*)`", script))
        if len(found) != 1:
            raise ValueError(f"the agent prompt names {reference.group(1)}, which is not one plain string")
        return found.pop()

    return re.sub(r"\$\{([\w$]+)\}", value, prompt)


def _read(pelican) -> None:
    global _prompt
    settings = pelican.settings
    source = settings.get("AGENT_PROMPT_SOURCE")
    script = Path(source).read_text() if source else console_script(settings["APP_URL"])
    _prompt = agent_prompt(script)


def _fill(content) -> None:
    text = getattr(content, "_content", None)
    if not text or PLACEHOLDER not in text:
        return
    assert _prompt is not None
    content._content = text.replace(PLACEHOLDER, html.escape(_prompt, quote=False))


def register() -> None:
    signals.initialized.connect(_read)
    signals.content_object_init.connect(_fill)

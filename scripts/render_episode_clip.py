#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10,<3.13"
# dependencies = ["rerun-sdk==0.30.2", "playwright==1.55.0"]
# ///
"""Render the home page clip of one public PhAIL episode from its Rerun recording.

Usage
  scripts/render_episode_clip.py https://phail.ai/api/episode_rrd/1086?v=9b6b96b000058992 \\
      content/media/episode-1086.mp4

The script downloads the recording, lays out the three camera views above the joint-state and
joint-command plots, and opens it in the Rerun web viewer in a headless Google Chrome. It steps the
viewer through the episode one frame at a time, takes a screenshot of each frame, and encodes the
frames as an H.264 MP4 with ffmpeg. It writes a JPEG poster next to the clip. Google Chrome must be
installed: the camera streams are H.264, which the Chromium that Playwright ships cannot decode.
"""

import argparse
import functools
import http.server
import subprocess
import tarfile
import tempfile
import threading
import time
import urllib.request
from pathlib import Path
from typing import ClassVar

import rerun as rr
import rerun.blueprint as rrb
from playwright.sync_api import sync_playwright

VIEWER_PACKAGE = "https://registry.npmjs.org/@rerun-io/web-viewer/-/web-viewer-0.30.2.tgz"
VIEWER_FILES = ["index.js", "re_viewer.js", "re_viewer_bg.wasm"]
TIMELINE = "recorded"
CAMERAS = [("/image.exterior", "Camera 1"), ("/image.exterior_2", "Camera 2"), ("/image.wrist", "Wrist camera")]
JOINT_COLORS = [0xB1E74FFF, 0x4FC3E7FF, 0xE7A94FFF, 0xE75F8BFF, 0xA98BE7FF, 0x5FE7B2FF, 0xF2F5EAFF]
PLOTS = [("/signals/robot_state.q", "Joint positions"), ("/signals/robot_command.joints", "Joint targets (actions)")]

PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><style>html, body { margin: 0; height: 100%; background: #111; overflow: hidden; }</style></head>
<body><script type="module">
import { WebViewer } from "./viewer/index.js";
const viewer = new WebViewer();
const here = (name) => new URL(name, location.href).href;
await viewer.start(here("episode.rrd"), document.body, {
  hide_welcome_screen: true, render_backend: "webgl", theme: "dark", width: "100%", height: "100%",
  panel_state_overrides: { top: "Hidden", blueprint: "Hidden", selection: "Hidden", time: "Hidden" },
});
window.viewer = viewer;
</script></body></html>
"""


def _download(url: str, path: Path) -> None:
    # phail.ai refuses the default Python client name.
    request = urllib.request.Request(url, headers={"User-Agent": "render-episode-clip/1"})
    with urllib.request.urlopen(request, timeout=300) as response:
        path.write_bytes(response.read())


def _unpack_viewer(package: Path, into: Path) -> None:
    with tarfile.open(package) as archive:
        for name in VIEWER_FILES:
            source = archive.extractfile(f"package/{name}")
            assert source, name
            (into / name).write_bytes(source.read())
    # index.js imports "./re_viewer" with no extension, as a bundler would resolve it.
    (into / "re_viewer").write_bytes((into / "re_viewer.js").read_bytes())


def _plot(origin: str, name: str) -> rrb.TimeSeriesView:
    # Joint i has one colour in both plots, so a state line and its target line read as a pair.
    colors = {f"{origin}/{i}": rr.SeriesLines.from_fields(colors=[color], widths=[2.0]) for i, color in enumerate(JOINT_COLORS)}
    return rrb.TimeSeriesView(origin=origin, name=name, plot_legend=rrb.PlotLegend(visible=False), overrides=colors)


def _layout() -> rrb.Blueprint:
    cameras = rrb.Horizontal(*(rrb.Spatial2DView(origin=origin, name=name) for origin, name in CAMERAS))
    plots = rrb.Horizontal(*(_plot(origin, name) for origin, name in PLOTS))
    return rrb.Blueprint(rrb.Vertical(cameras, plots, row_shares=[2, 3]), collapse_panels=True)


class _Files(http.server.SimpleHTTPRequestHandler):
    extensions_map: ClassVar[dict[str, str]] = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        "": "text/javascript",
        ".js": "text/javascript",
        ".wasm": "application/wasm",
    }

    def log_message(self, *args) -> None:
        pass


def _serve(root: Path) -> http.server.ThreadingHTTPServer:
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(_Files, directory=str(root)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def _capture(url: str, frames: Path, fps: int, width: int, height: int, scale: float, settle_ms: int) -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=scale, color_scheme="dark")
        page.on("console", lambda message: print("viewer:", message.type, message.text[:300]))
        page.on("pageerror", lambda error: print("viewer error:", error))
        page.goto(url)
        page.wait_for_function("window.viewer && window.viewer.get_active_recording_id()", timeout=120_000)
        recording = page.evaluate("window.viewer.get_active_recording_id()")
        # Opened after the recording, the layout replaces the one the recording carries.
        page.evaluate("window.viewer.open(new URL('layout.rbl', location.href).href)")
        page.wait_for_timeout(3000)
        page.evaluate("([r, t]) => { window.viewer.set_playing(r, false); window.viewer.set_active_timeline(r, t); }", [recording, TIMELINE])
        page.wait_for_function("([r, t]) => window.viewer.get_time_range(r, t)", arg=[recording, TIMELINE], timeout=60_000)
        span = page.evaluate("([r, t]) => window.viewer.get_time_range(r, t)", [recording, TIMELINE])
        start, end = int(span["min"]), int(span["max"])
        step = 1_000_000_000 // fps
        # The first seek also loads the video decoders, so it waits longer than the rest.
        page.evaluate("([r, t, x]) => window.viewer.set_current_time(r, t, x)", [recording, TIMELINE, start])
        page.wait_for_timeout(8000)
        count = 0
        for at in range(start, end + 1, step):
            page.evaluate("([r, t, x]) => window.viewer.set_current_time(r, t, x)", [recording, TIMELINE, at])
            page.wait_for_timeout(settle_ms)
            page.screenshot(path=str(frames / f"{count:05d}.png"))
            count += 1
        browser.close()
    return count


def _encode(frames: Path, fps: int, out: Path, out_width: int, crf: int) -> None:
    common = ["nice", "-n", "19", "ffmpeg", "-y", "-loglevel", "error", "-threads", "4"]
    subprocess.run(
        [*common, "-framerate", str(fps), "-i", str(frames / "%05d.png"),
         "-vf", f"scale={out_width}:-2:flags=lanczos", "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", str(out)],
        check=True, timeout=900,
    )
    poster = out.with_name(out.stem + "-poster.jpg")
    last = max(frames.glob("*.png"))
    subprocess.run([*common, "-i", str(last), "-vf", f"scale={out_width}:-2:flags=lanczos", "-q:v", "4", str(poster)], check=True, timeout=120)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("rrd_url", help="the episode's public Rerun recording")
    parser.add_argument("out", type=Path, help="the MP4 to write; the poster goes next to it")
    parser.add_argument("--fps", type=int, default=25)
    parser.add_argument("--width", type=int, default=1000, help="viewport width in CSS pixels")
    parser.add_argument("--height", type=int, default=625, help="viewport height in CSS pixels")
    parser.add_argument("--scale", type=float, default=1.6, help="device pixel ratio of the capture")
    parser.add_argument("--out-width", type=int, default=1440)
    parser.add_argument("--crf", type=int, default=26)
    parser.add_argument("--settle-ms", type=int, default=350, help="wait after each seek for the video frames to decode")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "viewer").mkdir()
        _download(VIEWER_PACKAGE, root / "viewer.tgz")
        _unpack_viewer(root / "viewer.tgz", root / "viewer")
        _download(args.rrd_url, root / "episode.rrd")
        application_id = rr.recording.load_recording(root / "episode.rrd").application_id()
        _layout().save(application_id, root / "layout.rbl")
        (root / "index.html").write_text(PAGE)
        frames = root / "frames"
        frames.mkdir()
        server = _serve(root)
        began = time.monotonic()
        try:
            count = _capture(f"http://127.0.0.1:{server.server_port}/index.html", frames, args.fps, args.width, args.height, args.scale, args.settle_ms)
        finally:
            server.shutdown()
        print(f"captured {count} frames in {time.monotonic() - began:.0f} s")
        _encode(frames, args.fps, args.out, args.out_width, args.crf)
    print(f"wrote {args.out} ({args.out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()

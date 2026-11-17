#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10,<3.13"
# dependencies = ["rerun-sdk[datafusion]==0.30.2", "playwright==1.55.0", "matplotlib==3.9.2", "pillow==10.4.0", "numpy<3"]
# ///
"""Render the home page clip of one public PhAIL episode from its Rerun recording.

Usage
  scripts/render_episode_clip.py https://phail.ai/api/episode_rrd/1086?v=9b6b96b000058992 \\
      content/media/phail-droid-1086.mp4

The script downloads the recording and reads the three raw camera videos and the robot signals
out of it. It renders only the 3D view of the arm in the Rerun web viewer, in a headless Google
Chrome, and draws the joint and gripper plots with matplotlib. It composes the cameras, the arm and
the plots into one frame for each step of the episode and encodes the frames as an H.264 MP4 with
ffmpeg. It writes a JPEG poster next to the clip. Google Chrome must be installed: the Chromium that
Playwright ships cannot run the viewer in this setup.
"""

import argparse
import bisect
import functools
import http.server
import subprocess
import tarfile
import tempfile
import threading
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rerun as rr
import rerun.blueprint as rrb
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

VIEWER_PACKAGE = "https://registry.npmjs.org/@rerun-io/web-viewer/-/web-viewer-0.30.2.tgz"
VIEWER_FILES = ["index.js", "re_viewer.js", "re_viewer_bg.wasm"]
TIMELINE = "recorded"
CAMERAS = ["image.exterior", "image.exterior_2", "image.wrist"]
JOINTS = 7
STATE = "robot_state.q"
COMMAND = "robot_command.joints"
GRIPPER = ["grip", "target_grip"]

GROUND = "#0f110d"
PANEL = "#161814"
TEXT = "#dfe6d2"
DIM = "#7d846f"
ACCENT = "#b1e74f"
TARGET = "#4fc3e7"
JOINT_COLORS = ["#b1e74f", "#4fc3e7", "#e7a94f", "#e75f8b", "#a98be7", "#5fe7b2", "#f2f5ea"]

# Output layout in pixels: two outer cameras on top; the wrist camera, the arm and the plots below.
WIDTH, GAP = 1440, 8
TOP_H = 404
BOTTOM_H = 300
HEIGHT = TOP_H + GAP + BOTTOM_H
WRIST_W, ROBOT_W = 533, 400
PLOTS_W = WIDTH - WRIST_W - ROBOT_W - 2 * GAP
ROBOT_TITLE_PX = 50
# Front right of the arm, high enough to see the gripper fingers open and close.
EYE = rrb.EyeControls3D(kind=rrb.Eye3DKind.Orbital, position=[1.0, 0.6, 0.7], look_target=[0.3, 0.0, 0.4], eye_up=[0, 0, 1], spin_speed=0.0)

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


@dataclass
class Episode:
    start_ns: int
    span_s: float
    # Per camera: the recording time of each video frame, in seconds, and the frame's number in its video.
    frames: dict[str, tuple[list[float], list[int]]]
    # Per signal: sample times in seconds and values.
    signals: dict[str, tuple[np.ndarray, np.ndarray]]


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


def _first(value: object) -> float | None:
    return None if value is None else float(np.asarray(value).ravel()[0])


def _extract(rrd: Path, into: Path) -> Episode:
    """Write each camera's raw video to `into` and read the signals and frame times."""
    signals = [f"{STATE}/{i}" for i in range(JOINTS)] + [f"{COMMAND}/{i}" for i in range(JOINTS)] + GRIPPER
    with rr.server.Server(datasets={"episode": [str(rrd)]}) as server:
        reader = server.client().get_dataset("episode").reader(index=TIMELINE)
        blobs = reader.select(*(f"/{c}:AssetVideo:blob" for c in CAMERAS)).limit(1).to_arrow_table()
        for camera in CAMERAS:
            (into / f"{camera}.mp4").write_bytes(bytes(blobs.column(f"/{camera}:AssetVideo:blob")[0].as_py()[0]))
        columns = [f"/{c}:VideoFrameReference:timestamp" for c in CAMERAS] + [f"/signals/{s}:Scalars:scalars" for s in signals]
        table = reader.select(TIMELINE, *columns).to_arrow_table()
    times = np.array([t.value if hasattr(t, "value") else int(t) for t in table.column(TIMELINE).cast("int64").to_pylist()], dtype=np.int64)
    start = int(times.min())
    seconds = (times - start) / 1e9

    def samples(column: str) -> tuple[np.ndarray, np.ndarray]:
        values = [_first(v) for v in table.column(column).to_pylist()]
        keep = [i for i, v in enumerate(values) if v is not None]
        order = sorted(keep, key=lambda i: seconds[i])
        return seconds[order], np.array([values[i] for i in order])

    frames = {}
    for camera in CAMERAS:
        at, stamp = samples(f"/{camera}:VideoFrameReference:timestamp")
        # The stored videos tick at 100 Hz whatever the camera rate, so a frame's number is its timestamp in 10 ms.
        frames[camera] = (at.tolist(), [round(s / 1e7) for s in stamp])
    return Episode(start, float(seconds.max()), frames, {s: samples(f"/signals/{s}:Scalars:scalars") for s in signals})


def _decode(video: Path, into: Path) -> None:
    into.mkdir()
    subprocess.run(["nice", "-n", "19", "ffmpeg", "-loglevel", "error", "-threads", "4", "-i", str(video), "-vsync", "passthrough", str(into / "%05d.png")],
                   check=True, timeout=600)


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


def _robot_layout() -> rrb.Blueprint:
    view = rrb.Spatial3DView(origin="/3d", name="Robot", eye_controls=EYE, background=[22, 24, 20])
    return rrb.Blueprint(view, collapse_panels=True)


def _capture_robot(url: str, frames: Path, times: list[float], settle_ms: int) -> None:
    """Screenshot the 3D view at each time, with the view's title bar cut off."""
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = browser.new_page(viewport={"width": ROBOT_W, "height": BOTTOM_H + ROBOT_TITLE_PX}, device_scale_factor=2, color_scheme="dark")
        page.on("pageerror", lambda error: print("viewer error:", error))
        page.goto(url)
        page.wait_for_function("window.viewer && window.viewer.get_active_recording_id()", timeout=120_000)
        recording = page.evaluate("window.viewer.get_active_recording_id()")
        # Opened after the recording, the layout replaces the one the recording carries.
        page.evaluate("window.viewer.open(new URL('layout.rbl', location.href).href)")
        page.wait_for_timeout(3000)
        page.evaluate("([r, t]) => { window.viewer.set_playing(r, false); window.viewer.set_active_timeline(r, t); }", [recording, TIMELINE])
        page.wait_for_function("([r, t]) => window.viewer.get_time_range(r, t)", arg=[recording, TIMELINE], timeout=60_000)
        start = int(page.evaluate("([r, t]) => window.viewer.get_time_range(r, t)", [recording, TIMELINE])["min"])
        clip = {"x": 0, "y": ROBOT_TITLE_PX, "width": ROBOT_W, "height": BOTTOM_H}
        for count, at in enumerate(times):
            page.evaluate("([r, t, x]) => window.viewer.set_current_time(r, t, x)", [recording, TIMELINE, start + round(at * 1e9)])
            page.wait_for_timeout(3000 if count == 0 else settle_ms)
            page.screenshot(path=str(frames / f"{count:05d}.png"), clip=clip)
        browser.close()


def _plots(episode: Episode) -> tuple[Image.Image, list[tuple[float, float, float, float]]]:
    """Draw the three plots once; return the image and each plot area as (left, top, right, bottom) pixels."""
    mono = font_manager.FontProperties(family="DejaVu Sans Mono", size=8.5)
    fig = plt.figure(figsize=(PLOTS_W / 100, BOTTOM_H / 100), dpi=100, facecolor=PANEL)
    rows = [("Joint positions", STATE), ("Joint targets", COMMAND), ("Gripper", None)]
    axes = fig.subplots(len(rows), 1, sharex=True, gridspec_kw={"hspace": 0.42, "left": 0.03, "right": 0.97, "top": 0.92, "bottom": 0.03})
    for ax, (title, prefix) in zip(axes, rows, strict=True):
        ax.set_facecolor(GROUND)
        for side in ax.spines.values():
            side.set_visible(False)
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        ax.set_xlim(0, episode.span_s)
        ax.text(0, 1.06, title, transform=ax.transAxes, color=DIM, fontproperties=mono, va="bottom")
        if prefix:
            ax.axhline(0, color="#2a2e25", linewidth=0.8)
            for i, color in enumerate(JOINT_COLORS):
                t, v = episode.signals[f"{prefix}/{i}"]
                ax.step(t, v, where="post", color=color, linewidth=1.3) if prefix == COMMAND else ax.plot(t, v, color=color, linewidth=1.3)
        else:
            ax.set_ylim(-0.1, 1.05)
            for signal, color, name, x in (("grip", ACCENT, "current", 0.62), ("target_grip", TARGET, "target", 0.82)):
                t, v = episode.signals[signal]
                ax.step(t, v, where="post", color=color, linewidth=1.5)
                ax.text(x, 1.06, name, transform=ax.transAxes, color=color, fontproperties=mono, va="bottom")
    fig.canvas.draw()
    image = Image.frombuffer("RGBA", fig.canvas.get_width_height(), fig.canvas.buffer_rgba()).convert("RGB")
    areas = [(b.x0, BOTTOM_H - b.y1, b.x1, BOTTOM_H - b.y0) for b in (ax.get_window_extent() for ax in axes)]
    plt.close(fig)
    return image, areas


def _cover(image: Image.Image, width: int, height: int) -> Image.Image:
    scale = max(width / image.width, height / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.LANCZOS)
    left, top = (resized.width - width) // 2, (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


def _label(draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont, x: int, y: int, text: str) -> None:
    box = draw.textbbox((x + 10, y + 8), text, font=font)
    draw.rectangle((box[0] - 6, box[1] - 4, box[2] + 6, box[3] + 4), fill=(15, 17, 13, 190))
    draw.text((x + 10, y + 8), text, font=font, fill=TEXT)


def _compose(episode: Episode, cameras: dict[str, Path], robot: Path, times: list[float], out: Path) -> None:
    font = ImageFont.truetype(font_manager.findfont("DejaVu Sans Mono"), 15)
    plots, areas = _plots(episode)
    tiles = {
        "image.exterior": (0, 0, (WIDTH - GAP) // 2, TOP_H, "Camera 1"),
        "image.exterior_2": ((WIDTH + GAP) // 2, 0, WIDTH - (WIDTH + GAP) // 2, TOP_H, "Camera 2"),
        "image.wrist": (0, TOP_H + GAP, WRIST_W, BOTTOM_H, "Wrist camera"),
    }
    robot_x, plots_x, bottom_y = WRIST_W + GAP, WRIST_W + ROBOT_W + 2 * GAP, TOP_H + GAP
    for count, at in enumerate(times):
        frame = Image.new("RGB", (WIDTH, HEIGHT), GROUND)
        draw = ImageDraw.Draw(frame, "RGBA")
        for camera, (x, y, w, h, name) in tiles.items():
            stamps, numbers = episode.frames[camera]
            shown = numbers[max(0, bisect.bisect_right(stamps, at) - 1)]
            frame.paste(_cover(Image.open(cameras[camera] / f"{shown + 1:05d}.png").convert("RGB"), w, h), (x, y))
            _label(draw, font, x, y, name)
        frame.paste(Image.open(robot / f"{count:05d}.png").convert("RGB").resize((ROBOT_W, BOTTOM_H), Image.LANCZOS), (robot_x, bottom_y))
        _label(draw, font, robot_x, bottom_y, "Robot")
        frame.paste(plots, (plots_x, bottom_y))
        for left, top, right, bottom in areas:
            cursor = plots_x + left + (right - left) * min(at / episode.span_s, 1.0)
            draw.line((cursor, bottom_y + top, cursor, bottom_y + bottom), fill=TEXT, width=2)
        frame.save(out / f"{count:05d}.png")


def _encode(frames: Path, fps: int, out: Path, crf: int) -> None:
    common = ["nice", "-n", "19", "ffmpeg", "-y", "-loglevel", "error", "-threads", "4"]
    subprocess.run(
        [*common, "-framerate", str(fps), "-i", str(frames / "%05d.png"), "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", str(out)],
        check=True, timeout=900,
    )
    poster = out.with_name(out.stem + "-poster.jpg")
    last = max(frames.glob("*.png"))
    subprocess.run([*common, "-i", str(last), "-q:v", "4", str(poster)], check=True, timeout=120)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("rrd_url", help="the episode's public Rerun recording")
    parser.add_argument("out", type=Path, help="the MP4 to write; the poster goes next to it")
    parser.add_argument("--fps", type=int, default=25)
    parser.add_argument("--crf", type=int, default=26)
    parser.add_argument("--settle-ms", type=int, default=150, help="wait after each seek for the 3D view to redraw")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "viewer").mkdir()
        _download(VIEWER_PACKAGE, root / "viewer.tgz")
        _unpack_viewer(root / "viewer.tgz", root / "viewer")
        _download(args.rrd_url, root / "episode.rrd")
        episode = _extract(root / "episode.rrd", root)
        cameras = {camera: root / f"frames-{camera}" for camera in CAMERAS}
        for camera, into in cameras.items():
            _decode(root / f"{camera}.mp4", into)
        times = [i / args.fps for i in range(int(episode.span_s * args.fps) + 1)]
        application_id = rr.recording.load_recording(root / "episode.rrd").application_id()
        _robot_layout().save(application_id, root / "layout.rbl")
        (root / "index.html").write_text(PAGE)
        robot = root / "robot"
        robot.mkdir()
        server = _serve(root)
        try:
            _capture_robot(f"http://127.0.0.1:{server.server_port}/index.html", robot, times, args.settle_ms)
        finally:
            server.shutdown()
        composed = root / "composed"
        composed.mkdir()
        _compose(episode, cameras, robot, times, composed)
        _encode(composed, args.fps, args.out, args.crf)
    print(f"wrote {args.out} ({args.out.stat().st_size / 1e6:.1f} MB, {len(times)} frames)")


if __name__ == "__main__":
    main()

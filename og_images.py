#!/usr/bin/env python3
"""Make link-preview images (LinkedIn, Facebook, Slack...) from the illustrations.

    python3 og_images.py          make images that are missing or out of date
    python3 og_images.py --all    remake every image

Each SVG in content/illustrations/ becomes static/og/<slug>.jpg, 1200x630, drawn
with the site's own stylesheet in light mode. build.py then points the page's
og:image at it. Link previews can't use SVG, which is why this step exists.

Needs Google Chrome (to draw the SVG) and macOS `sips` (to save as JPEG).
Uses only the standard library, so the system python3 is enough.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ART = ROOT / "content" / "illustrations"
OUT = ROOT / "static" / "og"
CSS = ROOT / "static" / "style.css"
WIDTH, HEIGHT = 1200, 630
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS = ("https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600"
         "&family=Imbue:opsz,wght@10..100,400..600&display=swap")

PAGE = """<!doctype html>
<html data-theme="light"><head><meta charset="utf-8">
<link href="{fonts}" rel="stylesheet">
<link rel="stylesheet" href="{css}">
<style>
  html, body {{ margin: 0; padding: 0; background: var(--paper); overflow: hidden; }}
  svg.art {{ display: block; width: {w}px; height: {h}px; transform: none !important; }}
</style></head>
<body>{svg}</body></html>
"""


def render(svg_path: Path, jpg_path: Path, tmp: Path) -> None:
    svg = svg_path.read_text(encoding="utf-8").strip()
    # Fill the 1200x630 frame; the 2:1 drawings lose a sliver at the sides.
    svg = svg.replace("<svg ", '<svg preserveAspectRatio="xMidYMid slice" ', 1)
    html = tmp / f"{svg_path.stem}.html"
    html.write_text(PAGE.format(fonts=FONTS, css=CSS.as_uri(), w=WIDTH, h=HEIGHT, svg=svg), encoding="utf-8")
    png = tmp / f"{svg_path.stem}.png"
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
         f"--window-size={WIDTH},{HEIGHT}", "--virtual-time-budget=4000",
         f"--screenshot={png}", html.as_uri()],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "88", str(png), "--out", str(jpg_path)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> int:
    if not Path(CHROME).exists():
        print("Google Chrome not found at " + CHROME)
        return 1
    remake_all = "--all" in sys.argv[1:]
    OUT.mkdir(parents=True, exist_ok=True)
    made = 0
    tmp = Path(tempfile.mkdtemp())
    try:
        for svg_path in sorted(ART.glob("*.svg")):
            jpg_path = OUT / f"{svg_path.stem}.jpg"
            newest_input = max(svg_path.stat().st_mtime, CSS.stat().st_mtime)
            if not remake_all and jpg_path.exists() and jpg_path.stat().st_mtime >= newest_input:
                continue
            render(svg_path, jpg_path, tmp)
            made += 1
            print("made", jpg_path.relative_to(ROOT))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # Drop images whose illustration is gone.
    for jpg_path in OUT.glob("*.jpg"):
        if not (ART / f"{jpg_path.stem}.svg").exists():
            jpg_path.unlink()
            print("removed", jpg_path.relative_to(ROOT))
    print(f"{made} image(s) made, {len(list(OUT.glob('*.jpg')))} in {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())

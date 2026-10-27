"""Build the single-file web version: docs/index.html. Run it with:  uv run python build_web.py

The story and the pictures come straight from story.py and sprites.py, so the web page can never drift
away from the Python game. The page needs no server: open the file, or put docs/ on any static host.
"""

import json
from pathlib import Path

import sprites
import story

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web"
OUTPUT = ROOT / "docs" / "index.html"


def story_json():
    """The story as JSON, safe to paste inside a <script> element."""
    data = {"start": story.START_SCENE, "items": story.ITEMS, "scenes": story.SCENES, "endings": story.ENDINGS}
    return json.dumps(data, separators=(",", ":")).replace("</", "<\\/")


def art_json():
    return json.dumps(sprites.export_for_web(), separators=(",", ":")).replace("</", "<\\/")


def build():
    """Return the whole page as text."""
    page = (WEB / "index.template.html").read_text()
    parts = {
        "{{STYLE}}": (WEB / "style.css").read_text(),
        "{{STORY}}": story_json(),
        "{{ART_DATA}}": art_json(),
        "{{ENGINE}}": (WEB / "engine.js").read_text(),
        "{{ART}}": (WEB / "art.js").read_text(),
        "{{UI}}": (WEB / "ui.js").read_text(),
    }
    for token, text in parts.items():
        page = page.replace(token, text)
    return page


if __name__ == "__main__":
    (WEB / "story.json").write_text(story_json() + "\n")
    OUTPUT.write_text(build())
    print("wrote %s (%d KB)" % (OUTPUT.relative_to(ROOT), len(OUTPUT.read_bytes()) // 1024))

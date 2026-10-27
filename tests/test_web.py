"""Tests for specs/web-version.md: the single-file web page must match the Python game exactly.

The JavaScript engine runs inside QuickJS, so these tests need no browser and no Node.
"""

import json
import random
import re
import sqlite3
from pathlib import Path

import pytest
import quickjs

import build_web
import db
import logic
import sprites
import story

ROOT = Path(__file__).resolve().parent.parent
SCENES = list(story.SCENES)
ITEMS = list(story.ITEMS) + ["chainsaw"]
CHOICES = [
    (choice["decision"], choice["value"])
    for scene in story.SCENES.values()
    for choice in scene.get("choices", [])
] + [("sofie", "kiss"), ("nothing", "here")]


# ---- the page is built from the Python story, and is self-contained -------------------


def test_the_embedded_story_is_exactly_the_python_story():
    assert json.loads((ROOT / "web" / "story.json").read_text()) == json.loads(build_web.story_json())


def test_the_committed_page_is_exactly_what_the_build_produces():
    assert (ROOT / "docs" / "index.html").read_text() == build_web.build()


def test_the_page_is_self_contained():
    page = (ROOT / "docs" / "index.html").read_text()
    assert "<title>" in page and "Where" in page
    assert not re.search(r"<script[^>]+src=", page)
    assert not re.search(r"<link[^>]+href=\"(?!https://fonts\.(googleapis|gstatic)\.com|data:)", page)
    assert "localStorage" in page
    assert len(page.encode()) < 600_000


# ---- the JavaScript engine behaves exactly like logic.py -----------------------------


def js_context():
    context = quickjs.Context()
    context.eval("var STORY = " + build_web.story_json() + ";")
    context.eval((ROOT / "web" / "engine.js").read_text())
    context.eval(
        """
        function memoryStorage(initial) {
          const box = {value: initial === undefined ? null : initial};
          return {get: () => box.value, set: (text) => { box.value = text; }, clear: () => { box.value = null; }, box};
        }
        function summary(view) {
          return view === null ? null : view;
        }
        function replay(actions) {
          const storage = memoryStorage();
          const engine = createEngine(STORY, storage);
          engine.startOver(true);
          return actions.map((a) => {
            let result;
            if (a[0] === "go") result = engine.goTo(a[1]);
            else if (a[0] === "take") result = engine.takeItem(a[1]);
            else if (a[0] === "decide") result = engine.decide(a[1], a[2]);
            else result = engine.startOver(a[1]);
            return {
              ok: result.ok, message: result.message, state: engine.loadGame(),
              decisions: Object.entries(engine.getDecisions()), takeable: engine.takeableItems(),
              view: summary(engine.sceneView()),
            };
          });
        }
        """
    )
    return context


def record(db_path, result):
    """Everything observable after one action: the result, the saved game and what the screen shows."""
    return {
        "ok": result["ok"], "message": result["message"], "state": logic.load_game(db_path),
        "decisions": [list(item) for item in logic.get_decisions(db_path).items()],
        "takeable": logic.takeable_items(db_path), "view": logic.scene_view(db_path),
    }


def apply(db_path, action):
    if action[0] == "go":
        return logic.go_to(db_path, action[1])
    if action[0] == "take":
        return logic.take_item(db_path, action[1])
    if action[0] == "decide":
        return logic.decide(db_path, action[1], action[2])
    return logic.start_over(db_path, action[1])


def python_replay(db_path, actions):
    logic.start_over(db_path, confirmed=True)
    return [record(db_path, apply(db_path, action)) for action in actions]


def random_game(db_path, rng, length):
    """Play random but mostly sensible moves in Python. Returns the actions and what Python saw."""
    logic.start_over(db_path, confirmed=True)
    view = logic.scene_view(db_path)
    actions, records = [], []
    while len(actions) < length:
        options = []
        if rng.random() < 0.75 and view is not None:
            options += [("go", move["to"]) for move in view["moves"]]
            options += [("take", item["id"]) for item in view["takeable"]]
            options += [("decide", c["decision"], c["value"]) for c in view["choices"]]
        if not options:
            options = (
                [("go", scene) for scene in SCENES]
                + [("take", item) for item in ITEMS]
                + [("decide", d, v) for d, v in CHOICES]
                + [("restart", False), ("restart", True)]
            )
        action = rng.choice(options)
        if action[0] == "restart" and rng.random() < 0.8:
            continue
        actions.append(action)
        records.append(record(db_path, apply(db_path, action)))
        view = records[-1]["view"]
    return actions, records


SCRIPTED_PATHS = {
    "love": [("decide", "sofie", "help"), ("go", "kiosk"), ("take", "sausage"), ("go", "bench"), ("go", "playground"),
             ("take", "binoculars"), ("go", "hill"), ("decide", "scan", "tram"), ("go", "tramstreet"),
             ("decide", "rescue", "treat"), ("decide", "finish", "thank")],
    "nonumber": [("decide", "sofie", "flirt"), ("go", "kiosk"), ("take", "sausage"), ("go", "bench"),
                 ("go", "playground"), ("take", "binoculars"), ("go", "hill"), ("decide", "scan", "tram"),
                 ("go", "tramstreet"), ("decide", "rescue", "treat"), ("decide", "finish", "apologize")],
    "tram": [("decide", "sofie", "help"), ("go", "playground"), ("take", "binoculars"), ("go", "hill"),
             ("decide", "scan", "tram"), ("go", "tramstreet"), ("decide", "rescue", "grab")],
    "car": [("decide", "sofie", "help"), ("go", "playground"), ("take", "binoculars"), ("go", "hill"),
            ("decide", "scan", "tram"), ("go", "tramstreet"), ("decide", "rescue", "shout")],
}


@pytest.mark.parametrize("ending", list(SCRIPTED_PATHS))
def test_each_ending_is_reachable_in_javascript(ending):
    context = js_context()
    records = json.loads(context.eval("JSON.stringify(replay(%s))" % json.dumps(SCRIPTED_PATHS[ending])))
    assert all(record["ok"] for record in records)
    assert records[-1]["state"]["ending"] == ending


def test_javascript_and_python_agree_on_random_games(monkeypatch):
    # Only for this test: keep the database in memory so thousands of saves stay quick.
    anchor = sqlite3.connect("file:parity?mode=memory&cache=shared", uri=True)

    def memory_connect(path):
        connection = sqlite3.connect("file:parity?mode=memory&cache=shared", uri=True)
        connection.executescript(db.SCHEMA)
        return connection

    monkeypatch.setattr(db, "connect", memory_connect)
    db_path = "unused"
    rng = random.Random(2026)
    context = js_context()
    games = [random_game(db_path, rng, 40) for _ in range(90)]
    games += [(path, python_replay(db_path, path)) for path in SCRIPTED_PATHS.values()]
    reached = set()
    for index, (actions, expected) in enumerate(games):
        actual = json.loads(context.eval("JSON.stringify(replay(%s))" % json.dumps(actions)))
        assert actual == expected, "game %d differs: %s" % (index, actions)
        reached |= {step["state"]["ending"] for step in expected if step["state"]["ending"]}
    anchor.close()
    assert reached == set(story.ENDINGS)


def test_the_saved_game_survives_a_restart_and_bad_saves_are_ignored():
    context = js_context()
    result = json.loads(
        context.eval(
            """
            (function () {
              const storage = memoryStorage();
              const first = createEngine(STORY, storage);
              first.startOver(true);
              first.decide("sofie", "help");
              first.goTo("kiosk");
              first.takeItem("sausage");
              const reopened = createEngine(STORY, storage);
              const afterRestart = {state: reopened.loadGame(), decisions: reopened.getDecisions()};
              const broken = createEngine(STORY, memoryStorage("{not json"));
              const wrongShape = createEngine(STORY, memoryStorage('{"scene": "mars"}'));
              const empty = createEngine(STORY, memoryStorage());
              const refused = createEngine(STORY, {get() { throw new Error("blocked"); }, set() { throw new Error("blocked"); }, clear() {}});
              refused.startOver(true);
              refused.decide("sofie", "flirt");
              return JSON.stringify({
                afterRestart, broken: broken.loadGame(), wrongShape: wrongShape.loadGame(), empty: empty.loadGame(),
                stillPlaysWithoutStorage: refused.getDecisions(),
              });
            })()
            """
        )
    )
    assert result["afterRestart"] == {
        "state": {"scene": "kiosk", "inventory": ["sausage"], "ending": None},
        "decisions": {"sofie": "help"},
    }
    assert result["broken"] is None and result["wrongShape"] is None and result["empty"] is None
    assert result["stillPlaysWithoutStorage"] == {"sofie": "flirt"}


# ---- the scene pictures drawn in JavaScript match the Python pictures ----------------


def painted_pixels(svg):
    """Paint every <path>/<rect> in document order and return {(x, y): colour}. Overlays are returned separately."""
    pixels, overlays = {}, []
    for match in re.finditer(r'<(path|rect)\b([^>]*)/>', svg):
        kind, attributes = match.groups()
        if "opacity" in attributes:
            overlays.append(re.search(r'fill="(#\w+)"', attributes).group(1))
            continue
        color = re.search(r'fill="(#\w+)"', attributes).group(1)
        if kind == "rect":
            x, y, w, h = (int(re.search(name + r'="(\d+)"', attributes).group(1)) for name in ("x", "y", "width", "height"))
            boxes = [(x, y, w, h)]
        else:
            data = re.search(r' d="([^"]*)"', attributes).group(1)
            boxes = [tuple(int(n) for n in m) for m in re.findall(r"M(\d+) (\d+)h(\d+)v(\d+)h-\d+z", data)]
        for x, y, w, h in boxes:
            for px in range(x, x + w):
                for py in range(y, y + h):
                    pixels[(px, py)] = color
    return pixels, overlays


def js_art_context():
    context = quickjs.Context()
    context.eval("var ART_DATA = " + json.dumps(sprites.export_for_web()) + ";")
    context.eval((ROOT / "web" / "art.js").read_text())
    context.eval("var art = createArt(ART_DATA);")
    return context


def test_the_park_background_is_the_same_picture():
    assert js_art_context().eval("art.parkBackground()") == sprites.park_background()


@pytest.mark.parametrize("scene", SCENES)
def test_scene_pictures_match_the_python_pictures_pixel_for_pixel(scene):
    context = js_art_context()
    for sofie in (None, "flirt"):
        for rescue in (None, "treat"):
            for ending in (None, "love", "nonumber", "tram", "car"):
                decisions = {}
                if sofie:
                    decisions["sofie"] = sofie
                if rescue:
                    decisions["rescue"] = rescue
                expected = sprites.scene_art(scene, decisions, ending)
                actual = context.eval("art.sceneArt(%s, %s, %s)" % (json.dumps(scene), json.dumps(decisions), json.dumps(ending)))
                assert painted_pixels(actual) == painted_pixels(expected), (scene, decisions, ending)

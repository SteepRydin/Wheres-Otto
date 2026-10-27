"""Pixel art for Where's Otto?. Every picture is a list of coloured squares drawn as crisp SVG.

A "rect" is (x, y, width, height, colour) in pixel units. Nothing here knows about the game rules.
"""

import math
import random

LEAF_COLORS = ["#f6c344", "#f2a22c", "#e8761f", "#d9531e", "#b8401a"]


# ---- drawing helpers ---------------------------------------------------------------


def _paths(rects):
    """Draw rects in order as few <path> elements as possible.

    Rects share a layer (one <path> per colour) only while no rect covers a pixel already painted in a
    different colour in that layer; otherwise a new layer starts, so later rects always stay on top.
    """
    layers = []
    pixels, by_color = {}, {}
    for x, y, w, h, color in rects:
        cells = [(px, py) for px in range(x, x + w) for py in range(y, y + h)]
        if any(pixels.get(cell, color) != color for cell in cells):
            layers.append(by_color)
            pixels, by_color = {}, {}
        for cell in cells:
            pixels[cell] = color
        by_color.setdefault(color, []).append("M%d %dh%dv%dh-%dz" % (x, y, w, h, w))
    layers.append(by_color)
    return "".join(
        '<path fill="%s" d="%s"/>' % (color, "".join(parts))
        for layer in layers
        for color, parts in layer.items()
    )


def _svg(width, height, body, css_class="", aspect="xMidYMid meet"):
    return (
        '<svg class="%s" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="%s" '
        'shape-rendering="crispEdges">%s</svg>' % (css_class, width, height, aspect, body)
    )


def _grid(rows, palette, ox=0, oy=0):
    """Turn rows of characters into rects. '.' is transparent; runs of one colour become one rect."""
    rects = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            char = row[x]
            start = x
            while x < len(row) and row[x] == char:
                x += 1
            if char != ".":
                rects.append((ox + start, oy + y, x - start, 1, palette[char]))
    return rects


def _shift(rects, dx, dy):
    return [(x + dx, y + dy, w, h, c) for x, y, w, h, c in rects]


def _flip(rects, width):
    """Mirror a sprite that is `width` pixels wide."""
    return [(width - x - w, y, w, h, c) for x, y, w, h, c in rects]


# ---- characters ---------------------------------------------------------------------

# Dark hair, light stubble, dark green waxed coat with the (corduroy) collar popped, jeans, black leather boots.
BENJAMIN_PALETTE = {
    "h": "#2a1a12", "H": "#43301f", "s": "#e8b894", "S": "#c99372", "e": "#1a1a1a", "b": "#8d7060",
    "m": "#8b3a3a", "g": "#33502f", "G": "#233a22", "c": "#4a3623", "C": "#35261a", "d": "#2f4f85",
    "k": "#111111",
}
BENJAMIN_ROWS = [
    "...hhhhhh...",
    "..hhhhhhhh..",
    "..hhHhhhhh..",
    "..hssssssh..",
    "..hsessesh..",
    "..ssssssss..",
    ".csbbmmbbsc.",
    ".ccCSSSSCcc.",
    ".gggggggggG.",
    ".gggggggggG.",
    ".gggggggggG.",
    ".sgggggggGs.",
    "..gggggggG..",
    "..gggggggG..",
    "..dddddddd..",
    "..ddd..ddd..",
    "..ddd..ddd..",
    "..kkk..kkk..",
    ".kkkk..kkkk.",
]

SOFIE_PALETTE = {
    "a": "#c4622d", "A": "#9b4a1f", "s": "#e8b894", "e": "#1a1a1a", "m": "#c0392b", "r": "#d6402f",
    "R": "#8f2a1f", "c": "#b9854d", "C": "#8f6538", "d": "#3a4f7a", "k": "#3b2a20",
}
SOFIE_ROWS = [
    "...aaaaaa...",
    "..aaaaaaaa..",
    "..aaaaaaaaa.",
    "..asessesaa.",
    "..assssssaaa",
    "..assmmssaa.",
    "...asssaaaa.",
    "..rrrrrrr.a.",
    ".ccrrRRrcc..",
    ".cccccrrcccc",
    ".cccccRccccc",
    ".sccccccccs.",
    "..cccccccc..",
    "..CCCCCCCC..",
    "..dddddddd..",
    "..ddd..ddd..",
    "..ddd..ddd..",
    "..ddd..ddd..",
    ".kkkk..kkkk.",
]
PERSON_W, PERSON_H = 12, 19

FUR, SHADE, GOLD, DARK_GOLD = "#f7f0dc", "#e6d6ab", "#e0b25a", "#c99a45"
NOSE, TONGUE, TEAL, TEAL_DARK = "#1b1b1b", "#e86f7a", "#19b7b0", "#0f8a85"

OTTO_RUN_W, OTTO_RUN_H = 26, 13
OTTO_RUN = [
    # tail plume
    (0, 2, 2, 2, GOLD), (1, 3, 3, 2, FUR), (2, 4, 2, 1, SHADE),
    # body and chest
    (4, 4, 11, 5, FUR), (6, 4, 8, 1, SHADE), (5, 8, 9, 1, SHADE),
    (14, 3, 4, 6, FUR), (15, 8, 3, 2, GOLD),
    # head, snout, ear, eye, nose, tongue
    (17, 1, 6, 6, FUR), (22, 4, 3, 2, FUR), (22, 6, 3, 1, SHADE),
    (16, 1, 2, 5, DARK_GOLD), (16, 2, 1, 3, GOLD),
    (21, 3, 1, 1, NOSE), (24, 4, 1, 1, NOSE), (23, 6, 1, 2, TONGUE),
    # collar
    (15, 4, 2, 3, TEAL),
    # galloping legs
    (15, 9, 2, 1, FUR), (17, 10, 2, 1, FUR), (19, 11, 2, 1, SHADE),
    (13, 9, 2, 2, FUR), (13, 11, 2, 1, SHADE),
    (5, 9, 2, 1, FUR), (3, 10, 2, 1, FUR), (1, 11, 2, 1, SHADE),
    (7, 9, 2, 2, FUR), (7, 11, 2, 1, SHADE),
    # teal leash flying behind in the wind
    (15, 3, 1, 1, TEAL), (14, 2, 1, 1, TEAL), (13, 2, 1, 1, TEAL), (12, 1, 1, 1, TEAL), (11, 1, 1, 1, TEAL),
    (10, 2, 1, 1, TEAL), (9, 2, 1, 1, TEAL), (8, 1, 1, 1, TEAL), (7, 1, 1, 1, TEAL), (6, 0, 1, 1, TEAL),
    (5, 0, 1, 1, TEAL), (3, 0, 2, 1, TEAL_DARK), (3, 1, 1, 1, TEAL_DARK),
]

OTTO_SIT_W, OTTO_SIT_H = 17, 15
OTTO_SIT = [
    (0, 10, 2, 2, GOLD), (0, 9, 1, 1, GOLD),
    (1, 7, 8, 7, FUR), (1, 12, 8, 2, SHADE),
    (7, 5, 4, 9, FUR), (8, 10, 3, 3, SHADE),
    (9, 10, 2, 5, FUR), (9, 14, 3, 1, SHADE),
    (8, 1, 6, 5, FUR), (13, 3, 3, 2, FUR), (13, 5, 3, 1, SHADE),
    (8, 1, 2, 5, DARK_GOLD), (8, 2, 1, 3, GOLD),
    (12, 2, 1, 1, NOSE), (15, 3, 1, 1, NOSE), (14, 5, 1, 2, TONGUE),
    (8, 6, 3, 1, TEAL), (11, 7, 1, 3, TEAL), (11, 10, 2, 1, TEAL_DARK),
]

HEART = [".rr.rr.", "rrrrrrr", "rrrrrrr", ".rrrrr.", "..rrr..", "...r..."]


def _heart(x, y):
    return _grid(HEART, {"r": "#e0405a"}, x, y) + [(x + 1, y + 1, 1, 1, "#ff93a4")]


def _person(rows, palette, x, y, flip=False):
    rects = _grid(rows, palette)
    if flip:
        rects = _flip(rects, PERSON_W)
    return _shift(rects, x, y)


def _otto_running(x, y):
    return _shift(OTTO_RUN, x, y)


def _otto_sitting(x, y):
    return _shift(OTTO_SIT, x, y)


# ---- vehicles and props -------------------------------------------------------------


def _tram(x, y):
    rects = [
        (1, 1, 32, 1, "#8a8f98"), (14, 0, 6, 1, "#333a44"),
        (0, 2, 34, 9, "#2a5db0"), (0, 6, 34, 2, "#f2f2f2"), (0, 10, 34, 1, "#1d4585"),
        (33, 7, 1, 2, "#ffe27a"), (4, 11, 4, 2, "#222222"), (26, 11, 4, 2, "#222222"),
    ]
    rects += [(3 + 8 * i, 3, 5, 3, "#cfe6f5") for i in range(4)]
    return _shift(rects, x, y)


def _car(x, y):
    rects = [
        (0, 4, 24, 5, "#c0392b"), (5, 1, 13, 3, "#c0392b"), (7, 2, 4, 2, "#cfe6f5"), (12, 2, 4, 2, "#cfe6f5"),
        (3, 8, 4, 3, "#222222"), (17, 8, 4, 3, "#222222"), (23, 5, 1, 2, "#ffe27a"), (0, 5, 1, 2, "#ffb3a7"),
    ]
    return _shift(rects, x, y)


def _bench(x, y):
    wood, dark = "#8a5a32", "#5f3d20"
    return _shift(
        [(0, 0, 34, 2, wood), (0, 2, 34, 1, dark), (0, 4, 34, 2, wood), (0, 6, 34, 1, dark),
         (2, 7, 2, 5, dark), (30, 7, 2, 5, dark), (0, 8, 34, 2, wood), (0, 10, 34, 1, dark)],
        x, y,
    )


def _pond(x, y):
    rects = [(2, 2, 46, 6, "#4f8fb0"), (0, 3, 50, 4, "#4f8fb0"), (6, 2, 38, 1, "#7fb6cf"),
             (4, 5, 14, 1, "#7fb6cf"), (28, 4, 14, 1, "#7fb6cf"), (10, 7, 30, 1, "#3d7391"),
             (30, 0, 2, 1, "#fff6d6"), (29, 1, 4, 2, "#fff6d6"), (32, 1, 2, 1, "#f2a22c")]
    return _shift(rects, x, y)


def _kiosk(x, y):
    rects = [(0, 6, 28, 18, "#f1e2bd"), (0, 6, 28, 1, "#cdb88a"), (3, 12, 22, 6, "#5b3a22"),
             (3, 12, 22, 1, "#8a5a32"), (4, 14, 4, 3, "#d9531e"), (10, 14, 4, 3, "#f2a22c")]
    for i in range(7):
        rects.append((i * 4, 0, 4, 6, "#d6402f" if i % 2 == 0 else "#f7f0dc"))
    return _shift(rects, x, y)


def _swings(x, y):
    wood = "#7a5230"
    rects = [(0, 0, 34, 2, wood), (0, 0, 2, 26, wood), (32, 0, 2, 26, wood)]
    for sx in (8, 22):
        rects += [(sx, 2, 1, 16, "#444444"), (sx + 5, 2, 1, 16, "#444444"), (sx - 1, 18, 8, 2, "#d9531e")]
    return _shift(rects, x, y)


def _tracks(y):
    rects = [(0, y, 120, 1, "#aab0b8"), (0, y + 3, 120, 1, "#aab0b8")]
    rects += [(i, y - 1, 2, 6, "#5b4630") for i in range(0, 120, 6)]
    return rects


def _tree(cx, base_y, radius, trunk_h, rng):
    rects = [(cx - 1, base_y - trunk_h, 3, trunk_h, "#5b3a22")]
    cy = base_y - trunk_h - radius + 3
    for dy in range(-radius, radius + 1):
        half = round(math.sqrt(max(0, radius * radius - dy * dy)) * 1.15)
        x = cx - half
        while x <= cx + half:
            width = min(rng.randint(1, 3), cx + half - x + 1)
            fraction = (dy + radius) / (2 * radius)
            color = LEAF_COLORS[min(4, int(fraction * 3.2 + rng.random() * 1.8))]
            rects.append((x, cy + dy, width, 1, color))
            x += width
    return rects


# ---- the full-page background ---------------------------------------------------------

SKY = ["#8fb8cf", "#9cc2d6", "#a9cadc", "#b6d2e2", "#c3dae7", "#d0e2ec", "#dce9f1"]
GRASS = ["#b7a747", "#a69a3f", "#958a38", "#847b32", "#746c2c"]


def _bands(colors, top, bottom, width):
    """Horizontal bands of colour with a one-row dither where two bands meet."""
    rects = []
    step = (bottom - top) / len(colors)
    for i, color in enumerate(colors):
        y0 = round(top + i * step)
        y1 = round(top + (i + 1) * step)
        rects.append((0, y0, width, y1 - y0, color))
        if i > 0:
            rects += [(x, y0 - 1, 1, 1, color) for x in range(0, width, 2)]
    return rects


def _cloud(x, y):
    return [(x + 2, y, 9, 1, "#f6f9fb"), (x, y + 1, 15, 1, "#f6f9fb"), (x + 3, y + 2, 12, 1, "#e1ebf2"),
            (x + 15, y + 1, 12, 1, "#eef4f8"), (x + 21, y + 2, 9, 1, "#e8eff5"), (x + 28, y + 1, 5, 1, "#f1f6f9")]


def park_background():
    """The pixelated autumn park behind everything, 160 x 90 pixels stretched over the page."""
    rng = random.Random(7)
    width, horizon = 160, 54
    rects = _bands(SKY, 0, horizon, width)
    for x, y in [(8, 6), (62, 12), (112, 4), (36, 24), (96, 28), (140, 18)]:
        rects += _cloud(x, y)
    for _ in range(18):
        rects.append((rng.randint(0, 150), rng.randint(2, 40), rng.randint(5, 13), 1, "#f4f8fa"))
    skyline = "#8ea3b8"
    x = 0
    while x < width:
        w, h = rng.randint(4, 9), rng.randint(3, 8)
        rects.append((x, horizon - h, w, h, skyline if rng.random() < 0.6 else "#7f95ab"))
        x += w
    rects += [(100, 42, 7, 12, "#7f95ab"), (101, 38, 5, 4, "#6f869e"), (103, 33, 1, 5, "#6f869e")]
    rects += _bands(GRASS, horizon, 90, width)
    for y in range(horizon + 2, 90):
        t = (y - horizon) / 36
        centre = 80 + 16 * math.sin(y * 0.16) * (0.3 + t)
        w = int(3 + 15 * t)
        rects.append((int(centre - w / 2) - 1, y, w + 2, 1, "#c9b27c"))
        rects.append((int(centre - w / 2), y, w, 1, "#e6d3a3"))
    for cx, base, radius, trunk in [(64, 58, 5, 4), (96, 57, 5, 4), (132, 58, 6, 5), (40, 59, 6, 5)]:
        rects += _tree(cx, base, radius, trunk, rng)
    for cx, base, radius, trunk in [(14, 80, 15, 16), (148, 84, 17, 18), (46, 74, 9, 9), (118, 72, 10, 10)]:
        rects += _tree(cx, base, radius, trunk, rng)
    for _ in range(170):
        rects.append((rng.randint(0, 158), rng.randint(horizon + 3, 89), rng.randint(1, 2), 1, rng.choice(LEAF_COLORS)))
    return _svg(width, 90, _paths(rects), "park-bg-svg", "xMidYMax slice")


# ---- the small picture above each scene --------------------------------------------------

STRIP_W, STRIP_H, GROUND = 120, 44, 38


def _strip_background(scene):
    rng = random.Random(11)
    rects = _bands(SKY, 0, 30, STRIP_W)
    rects += _cloud(8, 4) + _cloud(70, 9)
    for cx, base, radius, trunk in [(10, 34, 8, 6), (116, 34, 7, 6), (62, 33, 4, 3)]:
        rects += _tree(cx, base, radius, trunk, rng)
    rects += _bands(GRASS, 30, STRIP_H, STRIP_W)
    rects += [(rng.randint(0, 118), rng.randint(32, 43), rng.randint(1, 2), 1, rng.choice(LEAF_COLORS)) for _ in range(34)]
    if scene in ("carstreet",):
        rects += [(0, 34, STRIP_W, 10, "#3b3f49"), (0, 34, STRIP_W, 1, "#8d939c")]
        rects += [(i, 39, 6, 1, "#f1e2bd") for i in range(0, STRIP_W, 12)]
    if scene in ("tramstreet",):
        rects += [(0, 33, STRIP_W, 11, "#6a6f78")] + _tracks(35)
    return rects


def _strip_props(scene, decisions):
    if scene == "bench":
        return _bench(10, GROUND - 11)
    if scene == "pond":
        return _pond(60, GROUND - 8)
    if scene == "kiosk":
        return _kiosk(78, GROUND - 24)
    if scene == "playground":
        return _swings(74, GROUND - 26)
    if scene == "hill":
        return _tree(100, GROUND, 8, 9, random.Random(3))
    return []


def scene_art(scene, decisions, ending=None, lost=False):
    """The picture shown above the story text. It changes with the decisions made so far."""
    parts = _strip_background("carstreet" if ending == "car" else scene) + _strip_props(scene, decisions)
    rescue = decisions.get("rescue") == "treat"
    top = GROUND - PERSON_H
    people = _person(BENJAMIN_ROWS, BENJAMIN_PALETTE, 26, top)
    sofie_x = 42 if decisions.get("sofie") != "flirt" else 48
    sofie = _person(SOFIE_ROWS, SOFIE_PALETTE, sofie_x, top)
    otto = []
    extra = []

    if ending == "love":
        sofie = _person(SOFIE_ROWS, SOFIE_PALETTE, 42, top)
        otto = _otto_sitting(60, GROUND - OTTO_SIT_H)
        extra = _heart(44, 8) + _heart(36, 14) + _heart(52, 13)
    elif ending == "nonumber":
        otto = _otto_sitting(44, GROUND - OTTO_SIT_H)
        sofie = _person(SOFIE_ROWS, SOFIE_PALETTE, 100, top, flip=False)
    elif ending == "tram":
        otto = []
        extra = _tram(54, 25) + [(44, GROUND, 12, 1, TEAL), (40, GROUND - 1, 4, 1, TEAL_DARK)]
        sofie = _person(SOFIE_ROWS, SOFIE_PALETTE, 40, top)
        people = _person(BENJAMIN_ROWS, BENJAMIN_PALETTE, 20, top)
    elif ending == "car":
        extra = _car(72, 25) + [(54, GROUND, 14, 1, TEAL), (50, GROUND - 1, 4, 1, TEAL_DARK)]
        sofie = _person(SOFIE_ROWS, SOFIE_PALETTE, 40, top)
        people = _person(BENJAMIN_ROWS, BENJAMIN_PALETTE, 20, top)
    elif rescue:
        otto = _otto_sitting(62, GROUND - OTTO_SIT_H)
    else:
        otto_x = {"tramstreet": 60, "hill": 72}.get(scene, 74)
        otto = _otto_running(otto_x, GROUND - OTTO_RUN_H)
        extra = [(otto_x - 6, GROUND - 2, 4, 1, "#ffffff"), (otto_x - 10, GROUND - 5, 3, 1, "#ffffff")]

    if scene == "tramstreet" and not ending:
        extra += _tram(88, 25) if not rescue else _tram(96, 25)
    if scene == "carstreet" and not ending:
        extra += _car(80, 26)

    parts += people + sofie + otto + extra
    if ending in ("tram", "car"):
        parts.append((0, 0, STRIP_W, STRIP_H, "#7a0f1f"))
    body = _paths(parts)
    if ending in ("tram", "car"):
        body = body.replace('<path fill="#7a0f1f"', '<path opacity="0.28" fill="#7a0f1f"')
    return _svg(STRIP_W, STRIP_H, body, "strip-svg")


def export_for_web():
    """Everything the single-file web version needs to draw exactly the same pictures in JavaScript."""
    base = _strip_background("bench")
    return {
        "parkBackground": park_background(),
        "stripW": STRIP_W, "stripH": STRIP_H, "ground": GROUND,
        "personW": PERSON_W, "personH": PERSON_H, "ottoRunH": OTTO_RUN_H, "ottoSitH": OTTO_SIT_H,
        "teal": TEAL, "tealDark": TEAL_DARK,
        "benjamin": _grid(BENJAMIN_ROWS, BENJAMIN_PALETTE), "sofie": _grid(SOFIE_ROWS, SOFIE_PALETTE),
        "ottoRun": OTTO_RUN, "ottoSit": OTTO_SIT, "heart": _heart(0, 0), "tram": _tram(0, 0), "car": _car(0, 0),
        "base": _paths(base),
        "extras": {
            "carstreet": _paths(_strip_background("carstreet")[len(base):]),
            "tramstreet": _paths(_strip_background("tramstreet")[len(base):]),
        },
        "props": {scene: _paths(_strip_props(scene, {})) for scene in ("bench", "pond", "kiosk", "playground", "hill")},
    }

"""Where's Otto?: the Streamlit screens. Start the app with:  uv run streamlit run app.py"""

import html
import random

import streamlit as st

import db
import logic
import sprites

DB_PATH = db.DEFAULT_PATH

st.set_page_config(page_title="Where's Otto?", page_icon="🐾", layout="centered")


def toe(fill, light):
    """One pixel toe bean, as a CSS image."""
    return (
        "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 7 5' "
        "shape-rendering='crispEdges'%3E%3Cpath fill='" + fill.replace("#", "%23")
        + "' d='M1 0h5v1h1v3h-1v1h-5v-1h-1v-3h1z'/%3E%3Cpath fill='" + light.replace("#", "%23")
        + "' d='M2 1h2v1h-2z'/%3E%3C/svg%3E\")"
    )


def wind_leaves():
    """Orange and yellow leaves that blow across the whole page."""
    rng = random.Random(5)
    leaves = []
    for _ in range(22):
        leaves.append(
            '<span class="leaf" style="--top:%dvh;--size:%dpx;--dur:%.1fs;--delay:-%.1fs;--drop:%dvh;--c:%s"><span></span></span>'
            % (rng.randint(2, 92), rng.choice([6, 8, 10]), rng.uniform(9, 18), rng.uniform(0, 18),
               rng.randint(-20, 30), rng.choice(sprites.LEAF_COLORS))
        )
    return '<div class="wind">' + "".join(leaves) + "</div>"


BROWN_TOE = toe("#6d4527", "#b07a4d")
TEAL_TOE = toe("#0f8a85", "#5fd6cf")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');
:root { --gold: #ffd24a; --cream: #fbf1da; --ink: #181422; --teal: #19b7b0; --pad: #8a5a35; --pad-dark: #5a371d; }
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stHeader"] { background: transparent !important; }
html, body { background: #847b32; }
footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
.park-bg { position: fixed; inset: 0; z-index: -1; pointer-events: none; }
.park-bg svg { width: 100%; height: 100%; display: block; }
.block-container, [data-testid="stMainBlockContainer"] {
    max-width: 800px; margin-top: 1.5rem; padding: 1.6rem 1.8rem 2rem 1.8rem !important;
    background: rgba(24, 20, 34, 0.88);
    box-shadow: 0 -6px 0 0 #0e0b14, 0 6px 0 0 #0e0b14, -6px 0 0 0 #0e0b14, 6px 0 0 0 #0e0b14,
                0 -6px 0 -2px #ffd24a, 0 6px 0 -2px #ffd24a, -6px 0 0 -2px #ffd24a, 6px 0 0 -2px #ffd24a;
}
html, body, .stApp, .stMarkdown, p, li, label { font-family: 'VT323', 'Courier New', monospace !important; color: var(--cream); }
.stApp p { font-size: 1.35rem; }

.logo { font-family: 'Press Start 2P', monospace; text-align: center; font-size: 2.3rem; line-height: 1.4; color: var(--gold);
    text-shadow: 4px 4px 0 #8a3b12, -2px -2px 0 #3b1f0a, 2px -2px 0 #3b1f0a, -2px 2px 0 #3b1f0a; margin: 0.4rem 0 0.2rem 0; }
.tagline { text-align: center; font-size: 1.5rem; color: #cfe9e6; margin-bottom: 1rem; }
.place { font-family: 'Press Start 2P', monospace; font-size: 0.6rem; letter-spacing: 0.12em; color: #ff8c5a; margin-bottom: 0.7rem; }
.strip-svg { width: 100%; height: auto; display: block; image-rendering: pixelated;
    box-shadow: 0 -4px 0 0 #0e0b14, 0 4px 0 0 #0e0b14, -4px 0 0 0 #0e0b14, 4px 0 0 0 #0e0b14; margin: 0.4rem 0 1.2rem 0; }
.scene-title { font-family: 'Press Start 2P', monospace; font-size: 1.15rem; line-height: 1.5; color: var(--gold);
    border-bottom: 4px solid #6d4527; padding-bottom: 0.7rem; margin-bottom: 1rem; }
.scene-text { font-size: 1.55rem; line-height: 1.3; margin-bottom: 1.2rem; }
.whisper { border-left: 8px solid var(--teal); background: rgba(25, 183, 176, 0.14); padding: 0.6rem 1rem; margin: 0 0 1.1rem 0; font-size: 1.4rem; line-height: 1.25; }
.whisper.blocked { border-left-color: #ff5a4d; background: rgba(255, 90, 77, 0.16); }
.section { font-family: 'Press Start 2P', monospace; font-size: 0.6rem; letter-spacing: 0.15em; color: #8fd3cf; margin: 1.6rem 0 0.3rem 0; }
.ending { text-align: center; background: rgba(10, 8, 16, 0.85); padding: 1.4rem 1.2rem; margin: 1rem 0 1.5rem 0;
    box-shadow: 0 -4px 0 0 var(--gold), 0 4px 0 0 var(--gold), -4px 0 0 0 var(--gold), 4px 0 0 0 var(--gold); }
.ending.lost { box-shadow: 0 -4px 0 0 #ff5a4d, 0 4px 0 0 #ff5a4d, -4px 0 0 0 #ff5a4d, 4px 0 0 0 #ff5a4d; }
.ending .kicker { font-family: 'Press Start 2P', monospace; font-size: 0.6rem; line-height: 1.6; color: #8fd3cf; }
.ending.lost .kicker { color: #ff8a80; }
.ending .ending-title { font-family: 'Press Start 2P', monospace; font-size: 1.3rem; line-height: 1.5; color: var(--gold); margin: 0.8rem 0 1rem 0; }
.ending.lost .ending-title { color: #ff8a80; }
.ending p { font-size: 1.5rem; line-height: 1.3; }
.item { margin: 0.2rem 0 0.7rem 0; font-size: 1.4rem; line-height: 1.2; }
.item b { color: var(--gold); font-weight: normal; font-family: 'Press Start 2P', monospace; font-size: 0.7rem; }
.item span { color: #d8cbb0; }
.empty { color: #9a8f7c; font-size: 1.4rem; }

div[data-testid="stButton"] { margin-top: 32px; }
div[data-testid="stButton"] > button {
    position: relative; overflow: visible; width: 100%; justify-content: flex-start; text-align: left; border: 0; border-radius: 0;
    background: var(--pad); color: #fff4dc; padding: 0.9rem 1.1rem; min-height: 3rem;
    box-shadow: 0 -4px 0 0 var(--pad-dark), 0 4px 0 0 var(--pad-dark), -4px 0 0 0 var(--pad-dark), 4px 0 0 0 var(--pad-dark),
                inset 0 -6px 0 0 #6d4527, inset 0 6px 0 0 #a97b4f;
    transition: none;
}
div[data-testid="stButton"] > button::before {
    content: ""; position: absolute; left: 18px; top: -31px; width: 128px; height: 29px; pointer-events: none;
    background: BROWN_TOE 0% 9px / 28px 20px no-repeat, BROWN_TOE 34% 0 / 28px 20px no-repeat,
                BROWN_TOE 66% 0 / 28px 20px no-repeat, BROWN_TOE 100% 9px / 28px 20px no-repeat;
}
div[data-testid="stButton"] > button p { font-family: 'Press Start 2P', monospace !important; font-size: 0.62rem !important; line-height: 1.8; color: #fff4dc; margin: 0; }
div[data-testid="stButton"] > button:hover { background: #a97b4f; color: #fff; transform: translateY(-2px); }
div[data-testid="stButton"] > button:active { transform: translateY(3px); background: #6d4527; }
div[data-testid="stButton"] > button:focus:not(:active) { color: #fff; border: 0; outline: 4px solid #ffd24a; }
[class*="st-key-decide-"] div[data-testid="stButton"] > button, [class*="st-key-confirm-"] div[data-testid="stButton"] > button {
    background: #17908b;
    box-shadow: 0 -4px 0 0 #0a4f4c, 0 4px 0 0 #0a4f4c, -4px 0 0 0 #0a4f4c, 4px 0 0 0 #0a4f4c, inset 0 -6px 0 0 #0f6f6b, inset 0 6px 0 0 #3fc7c0;
}
[class*="st-key-decide-"] div[data-testid="stButton"] > button::before, [class*="st-key-confirm-"] div[data-testid="stButton"] > button::before {
    background: TEAL_TOE 0% 9px / 28px 20px no-repeat, TEAL_TOE 34% 0 / 28px 20px no-repeat,
                TEAL_TOE 66% 0 / 28px 20px no-repeat, TEAL_TOE 100% 9px / 28px 20px no-repeat;
}
[class*="st-key-decide-"] div[data-testid="stButton"] > button:hover, [class*="st-key-confirm-"] div[data-testid="stButton"] > button:hover { background: #2fb5ae; }
[class*="st-key-locked-"] div[data-testid="stButton"] > button { background: #5d5a62; filter: grayscale(0.6); box-shadow: 0 -4px 0 0 #36343b, 0 4px 0 0 #36343b, -4px 0 0 0 #36343b, 4px 0 0 0 #36343b, inset 0 -6px 0 0 #49464e, inset 0 6px 0 0 #77737c; }
[class*="st-key-menu-"] div[data-testid="stButton"] > button { background: #3b3550; box-shadow: 0 -4px 0 0 #1f1b2c, 0 4px 0 0 #1f1b2c, -4px 0 0 0 #1f1b2c, 4px 0 0 0 #1f1b2c, inset 0 -6px 0 0 #2b2640, inset 0 6px 0 0 #54496f; }

.wind { position: fixed; inset: 0; pointer-events: none; z-index: 60; overflow: hidden; }
.leaf { position: absolute; left: 0; top: var(--top); width: var(--size); height: var(--size); animation: blow var(--dur) steps(90) var(--delay) infinite; }
.leaf span { display: block; width: 100%; height: 100%; background: var(--c); clip-path: polygon(0 35%, 35% 0, 100% 0, 100% 65%, 65% 100%, 0 100%); animation: flutter 1.2s steps(6) infinite; }
@keyframes blow { from { transform: translate(-10vw, 0); } to { transform: translate(110vw, var(--drop)); } }
@keyframes flutter { 0% { transform: rotate(0) translateY(0); } 25% { transform: rotate(90deg) translateY(-6px); } 50% { transform: rotate(180deg) translateY(0); } 75% { transform: rotate(270deg) translateY(6px); } 100% { transform: rotate(360deg) translateY(0); } }
@media (prefers-reduced-motion: reduce) { .leaf, .leaf span { animation: none; } }
@media (max-width: 640px) { .logo { font-size: 1.4rem; } .block-container, [data-testid="stMainBlockContainer"] { padding: 1rem !important; } }
</style>
""".replace("BROWN_TOE", BROWN_TOE).replace("TEAL_TOE", TEAL_TOE),
    unsafe_allow_html=True,
)
st.markdown('<div class="park-bg">' + sprites.park_background() + "</div>" + wind_leaves(), unsafe_allow_html=True)


def say(text, kind=""):
    """Show a short message from the story, escaped so it can never inject markup."""
    st.markdown('<div class="whisper ' + kind + '">' + html.escape(text) + "</div>", unsafe_allow_html=True)


def act(action, *args):
    """Run one game action, remember its message for the next redraw, and redraw."""
    st.session_state["last"] = action(DB_PATH, *args)
    st.rerun()


def go_to_screen(screen):
    st.session_state["screen"] = screen
    st.session_state["last"] = None
    st.session_state["confirm_restart"] = False
    st.rerun()


def confirm_restart_box():
    """Ask before replacing existing progress; returns True while the question is open."""
    if not st.session_state.get("confirm_restart"):
        return False
    say("Starting over will erase your saved progress. This cannot be undone.", "blocked")
    yes, no = st.columns(2)
    if yes.button("Yes, start a new walk", key="confirm-yes"):
        logic.start_over(DB_PATH, confirmed=True)
        go_to_screen("game")
    if no.button("No, keep my progress", key="confirm-no"):
        st.session_state["confirm_restart"] = False
        st.rerun()
    return True


def ask_to_restart():
    """The 'new game' button: starts straight away on a first game, otherwise asks first."""
    if logic.load_game(DB_PATH) is None:
        logic.start_over(DB_PATH)
        go_to_screen("game")
    st.session_state["confirm_restart"] = True
    st.rerun()


def show_title():
    st.markdown('<div class="logo">WHERE\'S<br>OTTO?</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tagline">A windy autumn day in Oslo. One lost dog. One very confident detective.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(sprites.scene_art("bench", {"sofie": "help"}), unsafe_allow_html=True)
    save = logic.load_game(DB_PATH)
    if confirm_restart_box():
        return
    if save is not None:
        label = "See how your last walk ended" if save["ending"] else "Resume where you left off"
        if st.button(label, key="start-resume"):
            go_to_screen("game")
        if st.button("Start a new walk", key="start-new"):
            ask_to_restart()
    elif st.button("Start the walk", key="start-begin"):
        ask_to_restart()


def show_ending(view):
    lost = view["ending"]["result"] == "lost"
    st.markdown(
        '<div class="ending ' + ("lost" if lost else "") + '"><div class="kicker">' + html.escape(view["ending"]["kicker"])
        + '</div><div class="ending-title">' + html.escape(view["ending"]["title"]) + "</div><p>"
        + html.escape(view["ending"]["text"]) + "</p></div>",
        unsafe_allow_html=True,
    )


def show_actions(view):
    if view["takeable"] or view["choices"]:
        st.markdown('<div class="section">WHAT BENJAMIN DOES</div>', unsafe_allow_html=True)
    for item in view["takeable"]:
        if st.button(item["label"], key="take-" + item["id"]):
            act(logic.take_item, item["id"])
    for choice in view["choices"]:
        if st.button(choice["label"], key="decide-" + choice["decision"] + "-" + choice["value"]):
            act(logic.decide, choice["decision"], choice["value"])
    st.markdown('<div class="section">WHERE TO</div>', unsafe_allow_html=True)
    for move in view["moves"]:
        locked = bool(move["blocked"])
        label = ("🔒 " if locked else "") + move["label"]
        if st.button(label, key=("locked-" if locked else "go-") + move["to"]):
            act(logic.go_to, move["to"])


def show_inventory(view):
    st.markdown('<div class="section">POCKETS</div>', unsafe_allow_html=True)
    if not view["inventory"]:
        st.markdown('<div class="empty">Just keys, a phone and an empty leash loop.</div>', unsafe_allow_html=True)
    for item in view["inventory"]:
        st.markdown(
            '<div class="item"><b>' + html.escape(item["name"]) + "</b><br><span>" + html.escape(item["description"]) + "</span></div>",
            unsafe_allow_html=True,
        )


def show_game():
    view = logic.scene_view(DB_PATH)
    if view is None:
        go_to_screen("title")
    ending = view["ending"]["id"] if view["ending"] else None
    st.markdown('<div class="place">ST. HANSHAUGEN · OSLO</div>', unsafe_allow_html=True)
    st.markdown(sprites.scene_art(view["scene"], logic.get_decisions(DB_PATH), ending), unsafe_allow_html=True)
    st.markdown('<div class="scene-title">' + html.escape(view["title"]) + "</div>", unsafe_allow_html=True)
    last = st.session_state.get("last")
    if last:
        say(last["message"], "" if last["ok"] else "blocked")
    if view["ending"] is None:
        st.markdown('<div class="scene-text">' + html.escape(view["text"]) + "</div>", unsafe_allow_html=True)
    else:
        show_ending(view)
    if confirm_restart_box():
        return
    if view["ending"] is None:
        show_actions(view)
    show_inventory(view)
    st.markdown('<div class="section">THE WALK</div>', unsafe_allow_html=True)
    left, right = st.columns(2)
    if left.button("Start a new walk", key="menu-restart"):
        st.session_state["confirm_restart"] = True
        st.rerun()
    if right.button("Back to the title", key="menu-title"):
        go_to_screen("title")


def main():
    if st.session_state.get("screen", "title") == "game":
        show_game()
    else:
        show_title()


main()

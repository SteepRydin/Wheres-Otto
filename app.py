"""Last Curtain: the Streamlit screens. Start the app with:  uv run streamlit run app.py"""

import html

import streamlit as st

import db
import logic

DB_PATH = db.DEFAULT_PATH

st.set_page_config(page_title="Last Curtain", page_icon="🎭", layout="centered")

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=IM+Fell+English:ital@0;1&display=swap');

        :root { --gold: #c9a24b; --blood: #9b1c31; --bone: #e9e0d0; --ink: #0a060c; }

        .stApp {
            background:
                radial-gradient(ellipse at 50% -10%, rgba(155, 28, 49, 0.28), transparent 55%),
                radial-gradient(ellipse at 50% 120%, rgba(201, 162, 75, 0.10), transparent 50%),
                var(--ink);
            color: var(--bone);
        }
        [data-testid="stHeader"] { background: transparent; }
        footer, #MainMenu { visibility: hidden; }
        .block-container { max-width: 760px; padding-top: 2.5rem; }

        html, body, p, li, label, .stMarkdown { font-family: 'IM Fell English', Georgia, serif; }

        .title-mask { text-align: center; font-size: 4rem; margin: 0; filter: drop-shadow(0 0 18px rgba(155, 28, 49, 0.8)); animation: flicker 6s infinite; }
        .title { font-family: 'Cinzel', Georgia, serif; font-weight: 700; letter-spacing: 0.35em; text-align: center; font-size: 2.6rem; color: var(--gold); margin: 0.2rem 0; text-shadow: 0 0 24px rgba(201, 162, 75, 0.35); animation: flicker 6s infinite; }
        .tagline { text-align: center; font-style: italic; color: #9d8f80; letter-spacing: 0.08em; margin-bottom: 2rem; }
        .place { font-family: 'Cinzel', Georgia, serif; font-size: 0.75rem; letter-spacing: 0.3em; text-transform: uppercase; color: var(--blood); margin-bottom: 0.2rem; }
        .scene-title { font-family: 'Cinzel', Georgia, serif; font-size: 1.9rem; color: var(--gold); border-bottom: 1px solid rgba(201, 162, 75, 0.35); padding-bottom: 0.4rem; margin-bottom: 1rem; }
        .scene-text { font-size: 1.2rem; line-height: 1.75; font-style: italic; margin-bottom: 1.2rem; }
        .whisper { border-left: 3px solid var(--gold); background: rgba(201, 162, 75, 0.07); padding: 0.7rem 1rem; margin: 0 0 1.2rem 0; font-size: 1.05rem; }
        .whisper.blocked { border-left-color: var(--blood); background: rgba(155, 28, 49, 0.12); }
        .ending { text-align: center; border: 1px solid var(--gold); background: rgba(10, 6, 12, 0.7); padding: 1.6rem 1.4rem; margin: 1rem 0 1.5rem 0; box-shadow: 0 0 40px rgba(155, 28, 49, 0.35); }
        .ending.lost { border-color: var(--blood); box-shadow: 0 0 50px rgba(155, 28, 49, 0.6); }
        .ending.lost .ending-title { color: #d8556a; }
        .ending .kicker { font-family: 'Cinzel', Georgia, serif; letter-spacing: 0.4em; font-size: 0.75rem; color: var(--blood); }
        .ending .ending-title { font-family: 'Cinzel', Georgia, serif; font-size: 2.2rem; color: var(--gold); margin: 0.4rem 0 1rem 0; }
        .ending p { font-size: 1.15rem; line-height: 1.75; font-style: italic; }
        .section { font-family: 'Cinzel', Georgia, serif; letter-spacing: 0.25em; text-transform: uppercase; font-size: 0.8rem; color: #9d8f80; margin: 1.4rem 0 0.4rem 0; }
        .item { margin: 0.2rem 0 0.6rem 0; }
        .item b { color: var(--gold); font-family: 'Cinzel', Georgia, serif; font-weight: 500; }
        .item span { color: #b3a595; font-style: italic; }
        .empty { color: #6f6458; font-style: italic; }

        .stButton > button {
            width: 100%; text-align: left; justify-content: flex-start;
            background: rgba(20, 12, 16, 0.9); color: var(--bone);
            border: 1px solid rgba(201, 162, 75, 0.35); border-radius: 2px;
            font-family: 'IM Fell English', Georgia, serif; font-size: 1.1rem; padding: 0.55rem 1rem;
        }
        .stButton > button:hover { border-color: var(--gold); color: var(--gold); box-shadow: 0 0 14px rgba(155, 28, 49, 0.55); background: rgba(40, 14, 22, 0.95); }
        .stButton > button:focus:not(:active) { border-color: var(--gold); color: var(--gold); }

        @keyframes flicker { 0%, 92%, 100% { opacity: 1; } 93% { opacity: 0.55; } 95% { opacity: 1; } 96% { opacity: 0.7; } }
    </style>
    """,
    unsafe_allow_html=True,
)


def say(text, kind=""):
    """Show a short message from the house, escaped so it can never inject markup."""
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
    if yes.button("Yes, begin a new night", key="confirm-yes"):
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
    st.markdown('<p class="title-mask">🎭</p><p class="title">LAST CURTAIN</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="tagline">Operahuset, Oslo. After the masquerade. Something is still singing.</p>',
        unsafe_allow_html=True,
    )
    save = logic.load_game(DB_PATH)
    if confirm_restart_box():
        return
    if save is not None:
        label = "Return to the outcome of your last night" if save["ending"] else "Resume where you left off"
        if st.button(label, key="resume"):
            go_to_screen("game")
        if st.button("Begin a new night", key="new"):
            ask_to_restart()
    elif st.button("Begin the night", key="begin"):
        ask_to_restart()


def show_ending(view):
    lost = view["ending"]["result"] == "lost"
    kicker = "THE END · YOU DID NOT SURVIVE" if lost else "THE END · YOU SURVIVED"
    st.markdown(
        '<div class="ending ' + ("lost" if lost else "") + '"><div class="kicker">' + kicker + '</div><div class="ending-title">'
        + html.escape(view["ending"]["title"])
        + "</div><p>"
        + html.escape(view["ending"]["text"])
        + "</p></div>",
        unsafe_allow_html=True,
    )


def show_actions(view):
    if view["takeable"] or view["choices"]:
        st.markdown('<div class="section">Here</div>', unsafe_allow_html=True)
    for item in view["takeable"]:
        if st.button("✋ " + item["label"], key="take-" + item["id"]):
            act(logic.take_item, item["id"])
    for choice in view["choices"]:
        if st.button("🎭 " + choice["label"], key="decide-" + choice["decision"] + "-" + choice["value"]):
            act(logic.decide, choice["decision"], choice["value"])
    st.markdown('<div class="section">Where to</div>', unsafe_allow_html=True)
    for move in view["moves"]:
        prefix = "🔒 " if move["blocked"] else "→ "
        if st.button(prefix + move["label"], key="go-" + move["to"]):
            act(logic.go_to, move["to"])


def show_inventory(view):
    st.markdown('<div class="section">Inventory</div>', unsafe_allow_html=True)
    if not view["inventory"]:
        st.markdown('<div class="empty">Your pockets hold only a rag and a bottle of cleaner.</div>', unsafe_allow_html=True)
    for item in view["inventory"]:
        st.markdown(
            '<div class="item"><b>' + html.escape(item["name"]) + "</b><br><span>" + html.escape(item["description"]) + "</span></div>",
            unsafe_allow_html=True,
        )


def show_game():
    view = logic.scene_view(DB_PATH)
    if view is None:
        go_to_screen("title")
    st.markdown(
        '<div class="place">Operahuset · Bjørvika</div><div class="scene-title">' + html.escape(view["title"]) + "</div>",
        unsafe_allow_html=True,
    )
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
    st.markdown('<div class="section">The night</div>', unsafe_allow_html=True)
    left, right = st.columns(2)
    if left.button("Begin a new night", key="restart"):
        st.session_state["confirm_restart"] = True
        st.rerun()
    if right.button("Back to the title", key="title"):
        go_to_screen("title")


def main():
    if st.session_state.get("screen", "title") == "game":
        show_game()
    else:
        show_title()


main()

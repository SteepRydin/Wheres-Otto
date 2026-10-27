# Plot Twist — notes for the agent

A text mystery game for a university course (Introduction to Programming, Nova SBE). The person asking is a **beginner**. Teach, don't just do.

## Commands

- Run the app: `uv run streamlit run app.py`. Never use `pip` or `python -m venv`.
- Tests: `uv run pytest`.

## Structure

- `app.py` — Streamlit screens only.
- `logic.py` — the rules: which actions are allowed, what they change.
- `db.py` — SQLite storage (`plottwist.db`, never committed).
- `story.py` — the story content (scenes, items, conditions, endings), separate from player progress.
- `sprites.py` — the pixel art (background, characters, scene pictures) drawn as SVG. No game rules in here.
- `tests/` — pytest tests. `docs/product-brief.md` — the business requirements. `specs/` — one spec per task.

## Rules

- Read `docs/product-brief.md` and the spec before changing anything. If a requirement cannot be determined from them, say so instead of guessing.
- Build each task on a branch named after it (e.g. `first-feature`). Never commit to main directly.
- Tests come first and are reviewed by the student. Never edit, delete, weaken or skip a test to get green; if a test looks wrong against the brief, say so and stop.
- After every change, run the tests and paste the final output. The output is the proof, not a sentence.
- A rejected action must leave the saved data unchanged.
- Never commit the database file or secrets.
- Before deleting or overwriting the database or any saved data, say what will be lost and wait for a yes.
- Change code only for the task at hand; don't build other features you notice.

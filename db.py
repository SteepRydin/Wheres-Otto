"""SQLite storage for the one saved game. Every function takes the path of the database file."""

import os
import sqlite3
from contextlib import closing

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plottwist.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS game (id INTEGER PRIMARY KEY CHECK (id = 1), scene TEXT NOT NULL, ending TEXT);
CREATE TABLE IF NOT EXISTS inventory (item_id TEXT PRIMARY KEY);
CREATE TABLE IF NOT EXISTS decisions (decision TEXT PRIMARY KEY, value TEXT NOT NULL);
"""


def connect(db_path):
    """Open the database and make sure the tables exist."""
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA)
    return conn


def new_game(db_path, scene):
    """Replace any saved progress with a fresh game starting in this scene."""
    with closing(connect(db_path)) as conn, conn:
        conn.execute("DELETE FROM game")
        conn.execute("DELETE FROM inventory")
        conn.execute("DELETE FROM decisions")
        conn.execute("INSERT INTO game (id, scene, ending) VALUES (1, ?, NULL)", (scene,))


def load_state(db_path):
    """Return {"scene", "inventory", "ending"} for the saved game, or None if there is none."""
    with closing(connect(db_path)) as conn:
        row = conn.execute("SELECT scene, ending FROM game WHERE id = 1").fetchone()
        if row is None:
            return None
        items = conn.execute("SELECT item_id FROM inventory ORDER BY rowid").fetchall()
    return {"scene": row[0], "inventory": [item[0] for item in items], "ending": row[1]}


def load_decisions(db_path):
    """Return the remembered decisions as {decision: value}."""
    with closing(connect(db_path)) as conn:
        rows = conn.execute("SELECT decision, value FROM decisions ORDER BY rowid").fetchall()
    return {decision: value for decision, value in rows}


def save(db_path, scene=None, ending=None, add_item=None, decision=None):
    """Write the result of one accepted action in a single transaction."""
    with closing(connect(db_path)) as conn, conn:
        if scene is not None:
            conn.execute("UPDATE game SET scene = ? WHERE id = 1", (scene,))
        if ending is not None:
            conn.execute("UPDATE game SET ending = ? WHERE id = 1", (ending,))
        if add_item is not None:
            conn.execute("INSERT OR IGNORE INTO inventory (item_id) VALUES (?)", (add_item,))
        if decision is not None:
            conn.execute("INSERT INTO decisions (decision, value) VALUES (?, ?)", decision)

"""Tests for specs/first-feature.md. RED until the feature is built.

Each test gets its own throwaway database file, so tests never touch real saves.
Reopening the same file with load_game() is how these tests simulate restarting the app.
"""

import pytest

import logic


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "game.db")


def get_key(db_path):
    """Helper: new game, walk to the box office and take the key."""
    logic.new_game(db_path)
    assert logic.go_to(db_path, "box_office")["ok"]
    assert logic.take_item(db_path, "stage_door_key")["ok"]


def test_no_save_exists_before_a_new_game(db_path):
    assert logic.load_game(db_path) is None


def test_new_game_starts_in_the_foyer_with_an_empty_inventory(db_path):
    state = logic.new_game(db_path)
    assert state["scene"] == "foyer"
    assert state["inventory"] == []
    assert state["ending"] is None


def test_locked_route_is_rejected_without_the_key(db_path):
    """A1 / R1: backstage is locked; scene and inventory stay as they were."""
    logic.new_game(db_path)
    before = logic.load_game(db_path)
    result = logic.go_to(db_path, "backstage")
    assert result["ok"] is False
    assert result["message"] != ""
    assert logic.load_game(db_path) == before


def test_taking_the_key_puts_one_key_in_the_inventory(db_path):
    logic.new_game(db_path)
    logic.go_to(db_path, "box_office")
    assert logic.takeable_items(db_path) == ["stage_door_key"]
    result = logic.take_item(db_path, "stage_door_key")
    assert result["ok"] is True
    assert result["message"] != ""
    assert logic.load_game(db_path)["inventory"] == ["stage_door_key"]


def test_the_key_cannot_be_taken_twice(db_path):
    """A3 / R3: the drawer is empty afterwards and there is still only one key."""
    get_key(db_path)
    assert logic.takeable_items(db_path) == []
    before = logic.load_game(db_path)
    result = logic.take_item(db_path, "stage_door_key")
    assert result["ok"] is False
    assert logic.load_game(db_path) == before
    assert logic.load_game(db_path)["inventory"].count("stage_door_key") == 1


def test_the_key_cannot_be_taken_outside_the_box_office(db_path):
    """R2: items can only be collected where the story makes them available."""
    logic.new_game(db_path)
    result = logic.take_item(db_path, "stage_door_key")
    assert result["ok"] is False
    assert logic.load_game(db_path)["inventory"] == []


def test_the_box_office_has_no_direct_route_to_backstage(db_path):
    """R1: an action is only allowed from the scene that offers it, even with the key."""
    get_key(db_path)
    before = logic.load_game(db_path)
    result = logic.go_to(db_path, "backstage")
    assert result["ok"] is False
    assert logic.load_game(db_path) == before


def test_with_the_key_backstage_opens_and_the_key_is_kept(db_path):
    """A2: the key is reusable, not consumed."""
    get_key(db_path)
    assert logic.go_to(db_path, "foyer")["ok"]
    result = logic.go_to(db_path, "backstage")
    assert result["ok"] is True
    assert result["message"] != ""
    state = logic.load_game(db_path)
    assert state["scene"] == "backstage"
    assert state["inventory"] == ["stage_door_key"]


def test_resume_restores_scene_and_inventory(db_path):
    """A4: reopening the database file gives back the same game, and the same routes work."""
    get_key(db_path)
    logic.go_to(db_path, "foyer")
    saved = logic.load_game(db_path)
    assert saved == {"scene": "foyer", "inventory": ["stage_door_key"], "ending": None}
    assert logic.go_to(db_path, "backstage")["ok"] is True


def test_a_rejected_action_leaves_the_saved_game_unchanged(db_path):
    logic.new_game(db_path)
    logic.go_to(db_path, "box_office")
    before = logic.load_game(db_path)
    assert logic.go_to(db_path, "nowhere")["ok"] is False
    assert logic.take_item(db_path, "chainsaw")["ok"] is False
    assert logic.load_game(db_path) == before

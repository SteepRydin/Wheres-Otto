"""Tests for specs/full-game.md: endings, the remembered decision, restart and reset.

RED until the full game is built. tests/test_first_feature.py stays as written.
"""

import pytest

import logic
import story


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "game.db")


def ok(result):
    """Assert an action was accepted and told the player something."""
    assert result["ok"] is True, result["message"]
    assert result["message"] != ""
    return result


def with_key(db_path):
    logic.new_game(db_path)
    ok(logic.go_to(db_path, "box_office"))
    ok(logic.take_item(db_path, "stage_door_key"))
    ok(logic.go_to(db_path, "foyer"))
    ok(logic.go_to(db_path, "backstage"))


def fetch_mask(db_path):
    """From backstage: take the mask in the wardrobe and come back."""
    ok(logic.go_to(db_path, "wardrobe"))
    ok(logic.take_item(db_path, "porcelain_mask"))
    ok(logic.go_to(db_path, "backstage"))


def play_escape(db_path):
    with_key(db_path)
    fetch_mask(db_path)
    ok(logic.go_to(db_path, "stage"))
    ok(logic.decide(db_path, "singer", "silent"))
    ok(logic.go_to(db_path, "roof"))


def play_encore(db_path):
    with_key(db_path)
    ok(logic.go_to(db_path, "stage"))
    ok(logic.decide(db_path, "singer", "answer"))


# ---- the content the brief requires -------------------------------------------------


def test_the_story_has_the_content_the_brief_requires():
    assert len(story.SCENES) >= 5
    assert len(story.ITEMS) >= 2
    assert len(story.ENDINGS) >= 2
    assert story.START_SCENE in story.SCENES
    for scene in story.SCENES.values():
        assert scene["title"] != "" and scene["text"] != ""
        for target in scene.get("moves", {}):
            assert target in story.SCENES
    for item in story.ITEMS.values():
        assert item["location"] in story.SCENES
    for ending in story.ENDINGS.values():
        assert ending["title"] != "" and ending["text"] != ""


# ---- A5: two outcomes, then the game is over ----------------------------------------


def test_two_valid_paths_reach_two_different_endings(db_path):
    play_escape(db_path)
    first = logic.load_game(db_path)["ending"]
    ok(logic.start_over(db_path, confirmed=True))
    play_encore(db_path)
    second = logic.load_game(db_path)["ending"]
    assert first == "escape"
    assert second == "encore"


@pytest.mark.parametrize("play", [play_escape, play_encore])
def test_after_an_ending_story_actions_cannot_change_the_game(db_path, play):
    play(db_path)
    before = logic.load_game(db_path)
    decisions_before = logic.get_decisions(db_path)
    for scene_id in story.SCENES:
        assert logic.go_to(db_path, scene_id)["ok"] is False
    for item_id in story.ITEMS:
        assert logic.take_item(db_path, item_id)["ok"] is False
    assert logic.decide(db_path, "singer", "answer")["ok"] is False
    assert logic.decide(db_path, "singer", "silent")["ok"] is False
    assert logic.load_game(db_path) == before
    assert logic.get_decisions(db_path) == decisions_before
    assert logic.takeable_items(db_path) == []


@pytest.mark.parametrize("play,ending", [(play_escape, "escape"), (play_encore, "encore")])
def test_the_ending_can_be_reviewed_and_survives_a_restart(db_path, play, ending):
    play(db_path)
    view = logic.scene_view(db_path)
    assert view["ending"]["id"] == ending
    assert view["ending"]["title"] != "" and view["ending"]["text"] != ""
    assert view["moves"] == [] and view["takeable"] == [] and view["choices"] == []
    assert logic.load_game(db_path)["ending"] == ending


# ---- PT04: a remembered decision with consequences ----------------------------------


def test_answering_the_singer_ends_the_game_and_is_remembered(db_path):
    play_encore(db_path)
    assert logic.get_decisions(db_path) == {"singer": "answer"}
    assert logic.load_game(db_path)["scene"] == "stage"


def test_the_roof_is_closed_until_the_singer_is_dealt_with(db_path):
    with_key(db_path)
    fetch_mask(db_path)
    ok(logic.go_to(db_path, "stage"))
    before = logic.load_game(db_path)
    result = logic.go_to(db_path, "roof")
    assert result["ok"] is False and result["message"] != ""
    assert logic.load_game(db_path) == before


def test_staying_silent_without_a_mask_is_blocked_then_fixed_with_the_mask(db_path):
    with_key(db_path)
    ok(logic.go_to(db_path, "stage"))
    ok(logic.decide(db_path, "singer", "silent"))
    before = logic.load_game(db_path)
    result = logic.go_to(db_path, "roof")
    assert result["ok"] is False and result["message"] != ""
    assert logic.load_game(db_path) == before
    assert logic.get_decisions(db_path) == {"singer": "silent"}
    ok(logic.go_to(db_path, "backstage"))
    fetch_mask(db_path)
    ok(logic.go_to(db_path, "stage"))
    ok(logic.go_to(db_path, "roof"))
    assert logic.load_game(db_path)["ending"] == "escape"


def test_the_decision_is_made_once_and_only_on_the_stage(db_path):
    with_key(db_path)
    assert logic.decide(db_path, "singer", "silent")["ok"] is False
    assert logic.get_decisions(db_path) == {}
    ok(logic.go_to(db_path, "stage"))
    assert logic.decide(db_path, "singer", "scream")["ok"] is False
    ok(logic.decide(db_path, "singer", "silent"))
    assert logic.decide(db_path, "singer", "answer")["ok"] is False
    assert logic.get_decisions(db_path) == {"singer": "silent"}
    assert logic.load_game(db_path)["ending"] is None


# ---- PT03 / R2: items ----------------------------------------------------------------


def test_the_mask_is_taken_once_and_only_in_the_wardrobe(db_path):
    with_key(db_path)
    assert logic.take_item(db_path, "porcelain_mask")["ok"] is False
    ok(logic.go_to(db_path, "wardrobe"))
    assert logic.takeable_items(db_path) == ["porcelain_mask"]
    ok(logic.take_item(db_path, "porcelain_mask"))
    assert logic.take_item(db_path, "porcelain_mask")["ok"] is False
    assert logic.takeable_items(db_path) == []
    assert logic.load_game(db_path)["inventory"].count("porcelain_mask") == 1


def test_items_are_reusable_and_never_consumed(db_path):
    play_escape(db_path)
    assert logic.load_game(db_path)["inventory"] == ["stage_door_key", "porcelain_mask"]


def test_the_inventory_can_be_inspected(db_path):
    with_key(db_path)
    fetch_mask(db_path)
    inventory = logic.scene_view(db_path)["inventory"]
    assert [item["id"] for item in inventory] == ["stage_door_key", "porcelain_mask"]
    for item in inventory:
        assert item["name"] != "" and item["description"] != ""


# ---- PT02 / PT04 / R3: what the player sees -----------------------------------------


def test_blocked_routes_are_explained_and_open_ones_are_not(db_path):
    logic.new_game(db_path)
    moves = {move["to"]: move for move in logic.scene_view(db_path)["moves"]}
    assert moves["box_office"]["blocked"] is None
    assert isinstance(moves["backstage"]["blocked"], str) and moves["backstage"]["blocked"] != ""
    ok(logic.go_to(db_path, "box_office"))
    ok(logic.take_item(db_path, "stage_door_key"))
    ok(logic.go_to(db_path, "foyer"))
    moves = {move["to"]: move for move in logic.scene_view(db_path)["moves"]}
    assert moves["backstage"]["blocked"] is None


def test_revisited_scenes_remember_what_changed(db_path):
    logic.new_game(db_path)
    ok(logic.go_to(db_path, "box_office"))
    before = logic.scene_view(db_path)
    assert [item["id"] for item in before["takeable"]] == ["stage_door_key"]
    ok(logic.take_item(db_path, "stage_door_key"))
    after = logic.scene_view(db_path)
    assert after["text"] != before["text"]
    assert after["takeable"] == []


def test_the_wardrobe_changes_after_the_mask_is_taken(db_path):
    with_key(db_path)
    ok(logic.go_to(db_path, "wardrobe"))
    before = logic.scene_view(db_path)["text"]
    ok(logic.take_item(db_path, "porcelain_mask"))
    assert logic.scene_view(db_path)["text"] != before


def test_the_stage_remembers_the_decision(db_path):
    with_key(db_path)
    ok(logic.go_to(db_path, "stage"))
    view = logic.scene_view(db_path)
    assert {(c["decision"], c["value"]) for c in view["choices"]} == {("singer", "answer"), ("singer", "silent")}
    ok(logic.decide(db_path, "singer", "silent"))
    after = logic.scene_view(db_path)
    assert after["text"] != view["text"]
    assert after["choices"] == []


def test_there_is_no_view_without_a_game(db_path):
    assert logic.scene_view(db_path) is None


# ---- A4: resume ----------------------------------------------------------------------


def test_resume_restores_scene_items_and_the_decision(db_path):
    with_key(db_path)
    fetch_mask(db_path)
    ok(logic.go_to(db_path, "stage"))
    ok(logic.decide(db_path, "singer", "silent"))
    state = logic.load_game(db_path)
    decisions = logic.get_decisions(db_path)
    assert state == {"scene": "stage", "inventory": ["stage_door_key", "porcelain_mask"], "ending": None}
    assert decisions == {"singer": "silent"}
    # "Restart": nothing is kept in memory, everything is read back from the file.
    assert logic.load_game(db_path) == state
    assert logic.get_decisions(db_path) == decisions
    ok(logic.go_to(db_path, "roof"))


# ---- PT01 / A6 / R4: starting over ---------------------------------------------------


def test_cancelling_a_restart_keeps_the_progress(db_path):
    with_key(db_path)
    before = logic.load_game(db_path)
    result = logic.start_over(db_path, confirmed=False)
    assert result["ok"] is False and result["message"] != ""
    assert logic.load_game(db_path) == before


def test_confirming_a_restart_resets_progress_but_keeps_the_story(db_path):
    play_escape(db_path)
    ok(logic.start_over(db_path, confirmed=True))
    assert logic.load_game(db_path) == {"scene": "foyer", "inventory": [], "ending": None}
    assert logic.get_decisions(db_path) == {}
    ok(logic.go_to(db_path, "box_office"))
    assert logic.takeable_items(db_path) == ["stage_door_key"]


def test_starting_the_first_game_needs_no_confirmation(db_path):
    ok(logic.start_over(db_path, confirmed=False))
    assert logic.load_game(db_path)["scene"] == "foyer"

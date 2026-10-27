"""Tests for specs/more-consequences.md: the lights decision, the music box, and four endings (two lost).

RED until built. Existing tests are not changed.
"""

import pytest

import logic
import story


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "game.db")


def ok(result):
    assert result["ok"] is True, result["message"]
    assert result["message"] != ""
    return result


def rejected(result):
    assert result["ok"] is False
    assert result["message"] != ""


def start(db_path, lights=None):
    """New game, optionally flip the lights decision, then take the key and open backstage."""
    logic.new_game(db_path)
    if lights:
        ok(logic.decide(db_path, "lights", lights))
    ok(logic.go_to(db_path, "box_office"))
    ok(logic.take_item(db_path, "stage_door_key"))
    ok(logic.go_to(db_path, "foyer"))
    ok(logic.go_to(db_path, "backstage"))


def get_box(db_path):
    ok(logic.take_item(db_path, "music_box"))


def choice_set(db_path):
    return {(c["decision"], c["value"]) for c in logic.scene_view(db_path)["choices"]}


def play_lullaby(db_path):
    start(db_path, "on")
    get_box(db_path)
    ok(logic.go_to(db_path, "stage"))
    ok(logic.decide(db_path, "singer", "offer"))


def play_caught(db_path):
    start(db_path, "on")
    ok(logic.go_to(db_path, "stage"))
    ok(logic.decide(db_path, "singer", "rush"))


def play_escape(db_path):
    start(db_path, "off")
    ok(logic.go_to(db_path, "wardrobe"))
    ok(logic.take_item(db_path, "porcelain_mask"))
    ok(logic.go_to(db_path, "backstage"))
    ok(logic.go_to(db_path, "stage"))
    ok(logic.decide(db_path, "singer", "silent"))
    ok(logic.go_to(db_path, "roof"))


def play_encore(db_path):
    start(db_path)
    ok(logic.go_to(db_path, "stage"))
    ok(logic.decide(db_path, "singer", "answer"))


# ---- the lights decision ------------------------------------------------------------


def test_the_lights_decision_is_offered_once_in_the_foyer(db_path):
    logic.new_game(db_path)
    assert choice_set(db_path) == {("lights", "on"), ("lights", "off")}
    ok(logic.decide(db_path, "lights", "on"))
    assert logic.get_decisions(db_path) == {"lights": "on"}
    assert choice_set(db_path) == set()
    rejected(logic.decide(db_path, "lights", "off"))
    assert logic.get_decisions(db_path) == {"lights": "on"}


def test_the_lights_can_only_be_changed_in_the_foyer(db_path):
    logic.new_game(db_path)
    ok(logic.go_to(db_path, "box_office"))
    rejected(logic.decide(db_path, "lights", "on"))
    assert logic.get_decisions(db_path) == {}


def test_the_foyer_reacts_to_the_lights(db_path, tmp_path):
    logic.new_game(db_path)
    before = logic.scene_view(db_path)["text"]
    ok(logic.decide(db_path, "lights", "on"))
    lit = logic.scene_view(db_path)["text"]
    other = str(tmp_path / "other.db")
    logic.new_game(other)
    ok(logic.decide(other, "lights", "off"))
    dark = logic.scene_view(other)["text"]
    assert len({before, lit, dark}) == 3


# ---- the music box -------------------------------------------------------------------


def test_in_the_dark_the_music_box_cannot_be_found(db_path):
    start(db_path)
    assert logic.takeable_items(db_path) == []
    before = logic.load_game(db_path)
    rejected(logic.take_item(db_path, "music_box"))
    assert logic.load_game(db_path) == before


def test_with_the_lights_on_the_music_box_can_be_taken_once(db_path):
    start(db_path, "on")
    assert logic.takeable_items(db_path) == ["music_box"]
    get_box(db_path)
    assert logic.takeable_items(db_path) == []
    rejected(logic.take_item(db_path, "music_box"))
    assert logic.load_game(db_path)["inventory"].count("music_box") == 1


def test_the_music_box_cannot_be_taken_elsewhere(db_path):
    logic.new_game(db_path)
    ok(logic.decide(db_path, "lights", "on"))
    rejected(logic.take_item(db_path, "music_box"))
    assert logic.load_game(db_path)["inventory"] == []


# ---- what the singer lets you do depends on what you did ----------------------------


def test_with_the_lights_off_you_may_answer_or_stay_silent(db_path):
    start(db_path, "off")
    ok(logic.go_to(db_path, "stage"))
    assert choice_set(db_path) == {("singer", "answer"), ("singer", "silent")}


def test_with_the_lights_on_standing_still_is_not_an_option(db_path):
    start(db_path, "on")
    ok(logic.go_to(db_path, "stage"))
    assert choice_set(db_path) == {("singer", "answer"), ("singer", "rush")}
    before = logic.load_game(db_path)
    rejected(logic.decide(db_path, "singer", "silent"))
    assert logic.load_game(db_path) == before
    assert logic.get_decisions(db_path) == {"lights": "on"}


def test_the_music_box_adds_a_third_choice_only_when_you_hold_it(db_path):
    start(db_path, "on")
    get_box(db_path)
    ok(logic.go_to(db_path, "stage"))
    assert choice_set(db_path) == {("singer", "answer"), ("singer", "rush"), ("singer", "offer")}


def test_offering_the_music_box_without_having_it_is_rejected(db_path):
    start(db_path, "on")
    ok(logic.go_to(db_path, "stage"))
    before = logic.load_game(db_path)
    rejected(logic.decide(db_path, "singer", "offer"))
    assert logic.load_game(db_path) == before


def test_with_the_lights_on_the_roof_stays_out_of_reach(db_path):
    start(db_path, "on")
    ok(logic.go_to(db_path, "wardrobe"))
    ok(logic.take_item(db_path, "porcelain_mask"))
    ok(logic.go_to(db_path, "backstage"))
    ok(logic.go_to(db_path, "stage"))
    before = logic.load_game(db_path)
    rejected(logic.go_to(db_path, "roof"))
    assert logic.load_game(db_path) == before


# ---- four endings, two of them lost -------------------------------------------------


def test_every_ending_says_whether_you_survived_or_lost():
    results = {ending_id: ending["result"] for ending_id, ending in story.ENDINGS.items()}
    assert results == {"escape": "survived", "lullaby": "survived", "encore": "lost", "caught": "lost"}


@pytest.mark.parametrize(
    "play,ending,result",
    [
        (play_escape, "escape", "survived"),
        (play_lullaby, "lullaby", "survived"),
        (play_encore, "encore", "lost"),
        (play_caught, "caught", "lost"),
    ],
)
def test_each_ending_is_reachable_and_identified(db_path, play, ending, result):
    play(db_path)
    assert logic.load_game(db_path)["ending"] == ending
    shown = logic.scene_view(db_path)["ending"]
    assert shown["id"] == ending and shown["result"] == result
    assert shown["title"] != "" and shown["text"] != ""


@pytest.mark.parametrize("play", [play_lullaby, play_caught])
def test_the_new_endings_end_the_story(db_path, play):
    play(db_path)
    before = logic.load_game(db_path)
    decisions = logic.get_decisions(db_path)
    for scene_id in story.SCENES:
        rejected(logic.go_to(db_path, scene_id))
    for item_id in story.ITEMS:
        rejected(logic.take_item(db_path, item_id))
    rejected(logic.decide(db_path, "singer", "answer"))
    assert logic.load_game(db_path) == before
    assert logic.get_decisions(db_path) == decisions


def test_the_music_box_is_reusable(db_path):
    play_lullaby(db_path)
    assert logic.load_game(db_path)["inventory"] == ["stage_door_key", "music_box"]


# ---- A4 / A6 with the new state ------------------------------------------------------


def test_resume_keeps_the_lights_and_the_music_box(db_path):
    start(db_path, "on")
    get_box(db_path)
    state = logic.load_game(db_path)
    assert state["inventory"] == ["stage_door_key", "music_box"]
    assert logic.get_decisions(db_path) == {"lights": "on"}
    assert logic.load_game(db_path) == state
    ok(logic.go_to(db_path, "stage"))
    assert ("singer", "offer") in choice_set(db_path)


def test_starting_over_forgets_the_lights(db_path):
    start(db_path, "on")
    ok(logic.start_over(db_path, confirmed=True))
    assert logic.get_decisions(db_path) == {}
    assert choice_set(db_path) == {("lights", "on"), ("lights", "off")}

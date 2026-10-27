"""Tests for specs/otto-story.md: the whole of docs/product-brief.md, against the Where's Otto? story.

Each test gets its own throwaway database file. Reading the same file again with load_game() simulates
restarting the app. Brief requirements are named in the comments (PT01-PT05, R1-R4, A1-A6).
"""

import pytest

import logic
import story


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "game.db")


def ok(result):
    """Assert an action was accepted and told the player something (PT02)."""
    assert result["ok"] is True, result["message"]
    assert result["message"] != ""
    return result


def rejected(result):
    assert result["ok"] is False
    assert result["message"] != ""


def choice_set(db_path):
    return {(c["decision"], c["value"]) for c in logic.scene_view(db_path)["choices"]}


def begin(db_path, sofie="help"):
    logic.new_game(db_path)
    if sofie:
        ok(logic.decide(db_path, "sofie", sofie))


def fetch_sausage(db_path):
    ok(logic.go_to(db_path, "kiosk"))
    ok(logic.take_item(db_path, "sausage"))
    ok(logic.go_to(db_path, "bench"))


def climb_and_scan(db_path):
    """From the bench: playground (binoculars), hill, scan."""
    ok(logic.go_to(db_path, "playground"))
    ok(logic.take_item(db_path, "binoculars"))
    ok(logic.go_to(db_path, "hill"))
    ok(logic.decide(db_path, "scan", "tram"))


def to_tramstreet(db_path, sofie="help", sausage=True):
    begin(db_path, sofie)
    if sausage:
        fetch_sausage(db_path)
    climb_and_scan(db_path)
    ok(logic.go_to(db_path, "tramstreet"))


def play_love(db_path):
    to_tramstreet(db_path, "help")
    ok(logic.decide(db_path, "rescue", "treat"))
    ok(logic.decide(db_path, "finish", "thank"))


def play_nonumber(db_path):
    to_tramstreet(db_path, "flirt")
    ok(logic.decide(db_path, "rescue", "treat"))
    ok(logic.decide(db_path, "finish", "apologize"))


def play_tram(db_path):
    to_tramstreet(db_path, "help")
    ok(logic.decide(db_path, "rescue", "grab"))


def play_car(db_path):
    to_tramstreet(db_path, "help")
    ok(logic.decide(db_path, "rescue", "shout"))


ALL_PLAYS = [play_love, play_nonumber, play_tram, play_car]


# ---- the content the brief requires --------------------------------------------------


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
        assert ending["title"] != "" and ending["text"] != "" and ending["kicker"] != ""


def test_there_are_four_endings_two_won_and_two_lost():
    results = {ending_id: ending["result"] for ending_id, ending in story.ENDINGS.items()}
    assert results == {"love": "won", "nonumber": "won", "tram": "lost", "car": "lost"}


# ---- PT01 start and resume; A1 a locked route ----------------------------------------


def test_no_save_exists_before_a_new_game(db_path):
    assert logic.load_game(db_path) is None
    assert logic.scene_view(db_path) is None


def test_a_new_game_starts_on_the_bench_with_an_empty_inventory(db_path):
    state = logic.new_game(db_path)
    assert state == {"scene": "bench", "inventory": [], "ending": None}
    assert logic.get_decisions(db_path) == {}


def test_the_park_is_closed_until_you_have_said_something_to_sofie(db_path):
    """A1 / R1: a blocked action does not move the player or change the save."""
    logic.new_game(db_path)
    before = logic.load_game(db_path)
    for scene_id in ("pond", "kiosk", "playground"):
        rejected(logic.go_to(db_path, scene_id))
    assert logic.load_game(db_path) == before
    moves = {m["to"]: m for m in logic.scene_view(db_path)["moves"]}
    assert all(isinstance(m["blocked"], str) and m["blocked"] != "" for m in moves.values())


@pytest.mark.parametrize("sofie", ["help", "flirt"])
def test_either_answer_to_sofie_opens_the_park(db_path, sofie):
    begin(db_path, sofie)
    assert logic.get_decisions(db_path) == {"sofie": sofie}
    ok(logic.go_to(db_path, "pond"))


def test_the_sofie_decision_is_made_once_and_only_on_the_bench(db_path):
    logic.new_game(db_path)
    assert choice_set(db_path) == {("sofie", "help"), ("sofie", "flirt")}
    ok(logic.decide(db_path, "sofie", "help"))
    assert choice_set(db_path) == set()
    rejected(logic.decide(db_path, "sofie", "flirt"))
    assert logic.get_decisions(db_path) == {"sofie": "help"}
    ok(logic.go_to(db_path, "pond"))
    rejected(logic.decide(db_path, "sofie", "flirt"))


# ---- PT02 explore, PT04 remembered decisions change the story ------------------------


def test_the_pond_gives_a_clue_only_if_sofie_is_helping(db_path, tmp_path):
    begin(db_path, "help")
    ok(logic.go_to(db_path, "pond"))
    helped = logic.scene_view(db_path)["text"]
    other = str(tmp_path / "other.db")
    begin(other, "flirt")
    ok(logic.go_to(other, "pond"))
    flirted = logic.scene_view(other)["text"]
    assert helped != flirted
    assert "paw" in helped.lower()


def test_the_bench_reacts_to_the_decision(db_path, tmp_path):
    logic.new_game(db_path)
    start = logic.scene_view(db_path)["text"]
    ok(logic.decide(db_path, "sofie", "help"))
    helping = logic.scene_view(db_path)["text"]
    other = str(tmp_path / "other.db")
    begin(other, "flirt")
    flirting = logic.scene_view(other)["text"]
    assert len({start, helping, flirting}) == 3


def test_every_scene_can_be_reached_and_left(db_path):
    begin(db_path)
    ok(logic.go_to(db_path, "pond"))
    ok(logic.go_to(db_path, "bench"))
    ok(logic.go_to(db_path, "kiosk"))
    ok(logic.go_to(db_path, "bench"))
    ok(logic.go_to(db_path, "playground"))
    ok(logic.go_to(db_path, "hill"))
    ok(logic.go_to(db_path, "carstreet"))
    ok(logic.go_to(db_path, "hill"))


# ---- PT03 / R2 / A3: collecting and using items --------------------------------------


def test_the_sausage_is_taken_once_and_only_at_the_kiosk(db_path):
    begin(db_path)
    rejected(logic.take_item(db_path, "sausage"))
    ok(logic.go_to(db_path, "kiosk"))
    assert logic.takeable_items(db_path) == ["sausage"]
    ok(logic.take_item(db_path, "sausage"))
    assert logic.takeable_items(db_path) == []
    before = logic.load_game(db_path)
    rejected(logic.take_item(db_path, "sausage"))
    assert logic.load_game(db_path) == before
    assert logic.load_game(db_path)["inventory"].count("sausage") == 1


def test_the_binoculars_are_taken_once_and_only_at_the_playground(db_path):
    begin(db_path)
    ok(logic.go_to(db_path, "kiosk"))
    rejected(logic.take_item(db_path, "binoculars"))
    ok(logic.go_to(db_path, "bench"))
    ok(logic.go_to(db_path, "playground"))
    assert logic.takeable_items(db_path) == ["binoculars"]
    ok(logic.take_item(db_path, "binoculars"))
    rejected(logic.take_item(db_path, "binoculars"))
    assert logic.load_game(db_path)["inventory"] == ["binoculars"]


def test_unknown_things_cannot_be_taken_or_visited(db_path):
    begin(db_path)
    before = logic.load_game(db_path)
    rejected(logic.take_item(db_path, "chainsaw"))
    rejected(logic.go_to(db_path, "nowhere"))
    rejected(logic.decide(db_path, "sofie", "kiss"))
    assert logic.load_game(db_path) == before


def test_revisited_scenes_remember_what_was_taken(db_path):
    """R3: the kiosk and the playground change once their item is gone."""
    begin(db_path)
    ok(logic.go_to(db_path, "kiosk"))
    kiosk_before = logic.scene_view(db_path)
    ok(logic.take_item(db_path, "sausage"))
    kiosk_after = logic.scene_view(db_path)
    assert kiosk_after["text"] != kiosk_before["text"] and kiosk_after["takeable"] == []
    ok(logic.go_to(db_path, "bench"))
    ok(logic.go_to(db_path, "playground"))
    play_before = logic.scene_view(db_path)
    ok(logic.take_item(db_path, "binoculars"))
    play_after = logic.scene_view(db_path)
    assert play_after["text"] != play_before["text"] and play_after["takeable"] == []


def test_the_inventory_can_be_inspected(db_path):
    begin(db_path)
    fetch_sausage(db_path)
    ok(logic.go_to(db_path, "playground"))
    ok(logic.take_item(db_path, "binoculars"))
    inventory = logic.scene_view(db_path)["inventory"]
    assert [item["id"] for item in inventory] == ["sausage", "binoculars"]
    for item in inventory:
        assert item["name"] != "" and item["description"] != ""


# ---- the detective work: the hill ----------------------------------------------------


def test_the_scan_needs_the_binoculars(db_path):
    begin(db_path)
    ok(logic.go_to(db_path, "playground"))
    ok(logic.go_to(db_path, "hill"))
    assert choice_set(db_path) == set()
    before = logic.load_game(db_path)
    rejected(logic.decide(db_path, "scan", "tram"))
    assert logic.load_game(db_path) == before
    assert logic.get_decisions(db_path) == {"sofie": "help"}


def test_the_tram_street_is_locked_until_the_scan_and_explained(db_path):
    """A1: without the clue the route is rejected, and nothing changes."""
    begin(db_path)
    ok(logic.go_to(db_path, "playground"))
    ok(logic.take_item(db_path, "binoculars"))
    ok(logic.go_to(db_path, "hill"))
    moves = {m["to"]: m for m in logic.scene_view(db_path)["moves"]}
    assert isinstance(moves["tramstreet"]["blocked"], str) and moves["tramstreet"]["blocked"] != ""
    assert moves["carstreet"]["blocked"] is None
    before = logic.load_game(db_path)
    rejected(logic.go_to(db_path, "tramstreet"))
    assert logic.load_game(db_path) == before


def test_after_the_scan_the_tram_street_opens_and_the_binoculars_are_kept(db_path):
    """A2: using an item unlocks the route and the item stays."""
    begin(db_path)
    climb_and_scan(db_path)
    assert logic.get_decisions(db_path)["scan"] == "tram"
    ok(logic.go_to(db_path, "tramstreet"))
    assert logic.load_game(db_path)["scene"] == "tramstreet"
    assert "binoculars" in logic.load_game(db_path)["inventory"]


def test_the_hill_changes_after_the_scan(db_path):
    begin(db_path)
    ok(logic.go_to(db_path, "playground"))
    ok(logic.take_item(db_path, "binoculars"))
    ok(logic.go_to(db_path, "hill"))
    before = logic.scene_view(db_path)["text"]
    ok(logic.decide(db_path, "scan", "tram"))
    assert logic.scene_view(db_path)["text"] != before
    assert choice_set(db_path) == set()


def test_the_car_road_is_a_safe_dead_end_with_a_hint(db_path):
    begin(db_path)
    ok(logic.go_to(db_path, "playground"))
    ok(logic.go_to(db_path, "hill"))
    ok(logic.go_to(db_path, "carstreet"))
    assert logic.load_game(db_path)["ending"] is None
    assert logic.scene_view(db_path)["text"] != ""
    ok(logic.go_to(db_path, "hill"))


# ---- the rescue and the ending -------------------------------------------------------


def test_at_the_tracks_the_sausage_adds_the_calm_option(db_path):
    to_tramstreet(db_path, "help", sausage=True)
    assert choice_set(db_path) == {("rescue", "treat"), ("rescue", "grab"), ("rescue", "shout")}


def test_without_the_sausage_only_the_reckless_options_remain(db_path):
    to_tramstreet(db_path, "help", sausage=False)
    assert choice_set(db_path) == {("rescue", "grab"), ("rescue", "shout")}
    before = logic.load_game(db_path)
    rejected(logic.decide(db_path, "rescue", "treat"))
    assert logic.load_game(db_path) == before


def test_without_the_sausage_you_can_retreat_and_fetch_it(db_path):
    to_tramstreet(db_path, "help", sausage=False)
    ok(logic.go_to(db_path, "hill"))
    ok(logic.go_to(db_path, "playground"))
    ok(logic.go_to(db_path, "bench"))
    fetch_sausage(db_path)
    ok(logic.go_to(db_path, "playground"))
    ok(logic.go_to(db_path, "hill"))
    ok(logic.go_to(db_path, "tramstreet"))
    assert ("rescue", "treat") in choice_set(db_path)


def test_the_rescue_is_made_once_and_only_at_the_tram_street(db_path):
    begin(db_path)
    fetch_sausage(db_path)
    rejected(logic.decide(db_path, "rescue", "treat"))
    climb_and_scan(db_path)
    rejected(logic.decide(db_path, "rescue", "treat"))
    ok(logic.go_to(db_path, "tramstreet"))
    ok(logic.decide(db_path, "rescue", "treat"))
    rejected(logic.decide(db_path, "rescue", "grab"))
    assert logic.get_decisions(db_path)["rescue"] == "treat"
    assert logic.load_game(db_path)["ending"] is None


def test_the_final_choice_only_appears_after_a_calm_rescue(db_path):
    to_tramstreet(db_path, "help")
    assert not any(decision == "finish" for decision, _ in choice_set(db_path))
    rejected(logic.decide(db_path, "finish", "brag"))
    ok(logic.decide(db_path, "rescue", "treat"))
    assert choice_set(db_path) == {("finish", "thank"), ("finish", "brag")}


def test_the_final_choices_depend_on_how_you_treated_sofie(db_path):
    to_tramstreet(db_path, "flirt")
    ok(logic.decide(db_path, "rescue", "treat"))
    assert choice_set(db_path) == {("finish", "apologize"), ("finish", "brag")}
    before = logic.load_game(db_path)
    rejected(logic.decide(db_path, "finish", "thank"))
    assert logic.load_game(db_path) == before


def test_apologizing_is_only_for_someone_who_kept_flirting(db_path):
    to_tramstreet(db_path, "help")
    ok(logic.decide(db_path, "rescue", "treat"))
    rejected(logic.decide(db_path, "finish", "apologize"))
    assert logic.load_game(db_path)["ending"] is None


def test_bragging_after_help_ends_without_a_number(db_path):
    to_tramstreet(db_path, "help")
    ok(logic.decide(db_path, "rescue", "treat"))
    ok(logic.decide(db_path, "finish", "brag"))
    assert logic.load_game(db_path)["ending"] == "nonumber"


# ---- PT05 / A5: endings --------------------------------------------------------------


@pytest.mark.parametrize(
    "play,ending,result",
    [
        (play_love, "love", "won"),
        (play_nonumber, "nonumber", "won"),
        (play_tram, "tram", "lost"),
        (play_car, "car", "lost"),
    ],
)
def test_each_ending_is_reachable_identified_and_reviewable(db_path, play, ending, result):
    """R4: every ending is reachable from a new game through valid play."""
    play(db_path)
    assert logic.load_game(db_path)["ending"] == ending
    shown = logic.scene_view(db_path)["ending"]
    assert shown["id"] == ending and shown["result"] == result
    assert shown["title"] != "" and shown["text"] != "" and shown["kicker"] != ""
    view = logic.scene_view(db_path)
    assert view["moves"] == [] and view["takeable"] == [] and view["choices"] == []


@pytest.mark.parametrize("play", ALL_PLAYS)
def test_after_an_ending_story_actions_cannot_change_the_game(db_path, play):
    play(db_path)
    before = logic.load_game(db_path)
    decisions = logic.get_decisions(db_path)
    for scene_id in story.SCENES:
        rejected(logic.go_to(db_path, scene_id))
    for item_id in story.ITEMS:
        rejected(logic.take_item(db_path, item_id))
    for decision, value in [("sofie", "help"), ("rescue", "treat"), ("finish", "thank"), ("finish", "brag")]:
        rejected(logic.decide(db_path, decision, value))
    assert logic.load_game(db_path) == before
    assert logic.get_decisions(db_path) == decisions
    assert logic.takeable_items(db_path) == []


def test_two_valid_paths_from_separate_new_games_reach_different_endings(db_path):
    play_love(db_path)
    first = logic.load_game(db_path)["ending"]
    ok(logic.start_over(db_path, confirmed=True))
    play_tram(db_path)
    assert (first, logic.load_game(db_path)["ending"]) == ("love", "tram")


def test_grabbing_and_shouting_lose_in_different_ways(db_path):
    play_tram(db_path)
    assert logic.load_game(db_path)["ending"] == "tram"
    ok(logic.start_over(db_path, confirmed=True))
    play_car(db_path)
    assert logic.load_game(db_path)["ending"] == "car"


def test_items_are_reusable_and_never_consumed(db_path):
    play_love(db_path)
    assert logic.load_game(db_path)["inventory"] == ["sausage", "binoculars"]


# ---- A4: resume ----------------------------------------------------------------------


def test_resume_restores_scene_items_and_decisions(db_path):
    to_tramstreet(db_path, "help")
    ok(logic.decide(db_path, "rescue", "treat"))
    state = logic.load_game(db_path)
    decisions = logic.get_decisions(db_path)
    assert state == {"scene": "tramstreet", "inventory": ["sausage", "binoculars"], "ending": None}
    assert decisions == {"sofie": "help", "scan": "tram", "rescue": "treat"}
    # "Restart": nothing is kept in memory, everything is read back from the file.
    assert logic.load_game(db_path) == state
    assert logic.get_decisions(db_path) == decisions
    assert choice_set(db_path) == {("finish", "thank"), ("finish", "brag")}
    ok(logic.go_to(db_path, "hill"))


def test_a_finished_game_is_still_finished_after_a_restart(db_path):
    play_car(db_path)
    assert logic.load_game(db_path)["ending"] == "car"
    assert logic.scene_view(db_path)["ending"]["id"] == "car"


# ---- PT01 / A6 / R4: starting over ---------------------------------------------------


def test_cancelling_a_restart_keeps_the_progress(db_path):
    to_tramstreet(db_path)
    before = logic.load_game(db_path)
    result = logic.start_over(db_path, confirmed=False)
    assert result["ok"] is False and result["message"] != ""
    assert logic.load_game(db_path) == before


def test_confirming_a_restart_resets_progress_but_keeps_the_story(db_path):
    play_love(db_path)
    ok(logic.start_over(db_path, confirmed=True))
    assert logic.load_game(db_path) == {"scene": "bench", "inventory": [], "ending": None}
    assert logic.get_decisions(db_path) == {}
    assert choice_set(db_path) == {("sofie", "help"), ("sofie", "flirt")}
    begin_after = ok(logic.decide(db_path, "sofie", "help"))
    assert begin_after["ok"]
    ok(logic.go_to(db_path, "kiosk"))
    assert logic.takeable_items(db_path) == ["sausage"]


def test_starting_the_first_game_needs_no_confirmation(db_path):
    ok(logic.start_over(db_path, confirmed=False))
    assert logic.load_game(db_path)["scene"] == "bench"

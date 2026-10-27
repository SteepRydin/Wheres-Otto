"""The rules of Last Curtain: which actions are allowed and what they change.

Every action either is rejected (nothing is saved) or is accepted (saved in one step).
Actions return {"ok": bool, "message": str}.
"""

import db
import story

GAME_OVER = "The story is over. Start a new game to play again."


def _accepted(message):
    return {"ok": True, "message": message}


def _rejected(message):
    return {"ok": False, "message": message}


def _holds(condition, state, decisions):
    """True when the condition is met. Forms: {"item": id}, {"decision": id, "value": v}, {"decision": id, "any": True}.
    "not": True flips the result."""
    if "item" in condition:
        met = condition["item"] in state["inventory"]
    elif condition.get("any"):
        met = condition["decision"] in decisions
    else:
        met = decisions.get(condition["decision"]) == condition["value"]
    return not met if condition.get("not") else met


def _first_unmet(requirements, state, decisions):
    """Return the explanation of the first unmet requirement, or None when all are met."""
    for requirement in requirements:
        if not _holds(requirement, state, decisions):
            return requirement["blocked"]
    return None


def new_game(db_path):
    """Start a fresh game (replacing any save) and return its state."""
    db.new_game(db_path, story.START_SCENE)
    return load_game(db_path)


def start_over(db_path, confirmed=False):
    """Start a new game. Replacing an existing save needs confirmed=True."""
    if db.load_state(db_path) is not None and not confirmed:
        return _rejected("Starting over erases your progress. Confirm to start a new game.")
    new_game(db_path)
    return _accepted("A new night begins. The doors are locked behind you.")


def load_game(db_path):
    """Return the saved state {"scene", "inventory", "ending"}, or None when no save exists."""
    return db.load_state(db_path)


def get_decisions(db_path):
    """Return the remembered decisions as {decision: value}."""
    return db.load_decisions(db_path)


def go_to(db_path, scene_id):
    """Move to another scene if the story offers that route and its conditions are met."""
    state = load_game(db_path)
    if state is None:
        return _rejected("There is no game in progress.")
    if state["ending"] is not None:
        return _rejected(GAME_OVER)
    move = story.SCENES[state["scene"]].get("moves", {}).get(scene_id)
    if move is None:
        return _rejected("You cannot get there from here.")
    blocked = _first_unmet(move.get("requires", []), state, get_decisions(db_path))
    if blocked is not None:
        return _rejected(blocked)
    db.save(db_path, scene=scene_id, ending=story.SCENES[scene_id].get("ending"))
    return _accepted(move["message"])


def takeable_items(db_path):
    """Return the ids of items that can still be taken in the current scene."""
    state = load_game(db_path)
    if state is None or state["ending"] is not None:
        return []
    decisions = get_decisions(db_path)
    return [
        item_id
        for item_id, item in story.ITEMS.items()
        if item["location"] == state["scene"]
        and item_id not in state["inventory"]
        and _first_unmet(item.get("requires", []), state, decisions) is None
    ]


def take_item(db_path, item_id):
    """Collect an item that lies in the current scene, once per game."""
    state = load_game(db_path)
    if state is None:
        return _rejected("There is no game in progress.")
    if state["ending"] is not None:
        return _rejected(GAME_OVER)
    item = story.ITEMS.get(item_id)
    if item is None:
        return _rejected("There is no such thing here.")
    if item_id in state["inventory"]:
        return _rejected("You already have the " + item["name"].lower() + ".")
    if item["location"] != state["scene"]:
        return _rejected("There is nothing like that to take here.")
    blocked = _first_unmet(item.get("requires", []), state, get_decisions(db_path))
    if blocked is not None:
        return _rejected(blocked)
    db.save(db_path, add_item=item_id)
    return _accepted(item["take_message"])


def decide(db_path, decision, value):
    """Make a one-time decision offered by the current scene. Some choices end the game."""
    state = load_game(db_path)
    if state is None:
        return _rejected("There is no game in progress.")
    if state["ending"] is not None:
        return _rejected(GAME_OVER)
    for choice in story.SCENES[state["scene"]].get("choices", []):
        if choice["decision"] == decision and choice["value"] == value:
            break
    else:
        return _rejected("That is not a choice you can make here.")
    decisions = get_decisions(db_path)
    if decision in decisions:
        return _rejected("You have already made that choice. It cannot be unmade.")
    blocked = _first_unmet(choice.get("requires", []), state, decisions)
    if blocked is not None:
        return _rejected(blocked)
    db.save(db_path, decision=(decision, value), ending=choice.get("ending"))
    return _accepted(choice["message"])


def scene_view(db_path):
    """Everything the screen needs to show the current moment, or None when there is no game."""
    state = load_game(db_path)
    if state is None:
        return None
    decisions = get_decisions(db_path)
    scene = story.SCENES[state["scene"]]
    inventory = [
        {"id": item_id, "name": story.ITEMS[item_id]["name"], "description": story.ITEMS[item_id]["description"]}
        for item_id in state["inventory"]
    ]
    view = {"scene": state["scene"], "title": scene["title"], "text": scene["text"],
            "moves": [], "takeable": [], "choices": [], "inventory": inventory, "ending": None}
    for change in scene.get("changes", []):
        if _holds(change["if"], state, decisions):
            view["text"] = change["text"]
            break
    if state["ending"] is not None:
        ending = story.ENDINGS[state["ending"]]
        view["ending"] = {
            "id": state["ending"],
            "title": ending["title"],
            "text": ending["text"],
            "result": ending["result"],
            "kicker": ending["kicker"],
        }
        return view
    for target, move in scene.get("moves", {}).items():
        blocked = _first_unmet(move.get("requires", []), state, decisions)
        view["moves"].append({"to": target, "label": move["label"], "blocked": blocked})
    for item_id in takeable_items(db_path):
        view["takeable"].append({"id": item_id, "label": "Take the " + story.ITEMS[item_id]["name"].lower()})
    for choice in scene.get("choices", []):
        if choice["decision"] in decisions:
            continue
        if _first_unmet(choice.get("requires", []), state, decisions) is not None:
            continue
        view["choices"].append({"decision": choice["decision"], "value": choice["value"], "label": choice["label"]})
    return view

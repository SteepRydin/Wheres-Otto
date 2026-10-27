"use strict";
/* The rules of Where's Otto?, ported from logic.py. Story content is passed in (it is story.py exported
   as JSON); the saved game lives in `storage`, which has get(), set(text) and clear().
   Every action either is rejected (nothing is saved) or accepted (saved in one step) and returns
   {ok: boolean, message: string}. */

function createEngine(story, storage) {
  var GAME_OVER = "The story is over. Start a new game to play again.";
  var memory = null; // the save kept in memory, used only if the browser refuses to store anything

  function has(object, key) {
    return Object.prototype.hasOwnProperty.call(object, key);
  }

  function accepted(message) {
    return { ok: true, message: message };
  }

  function rejected(message) {
    return { ok: false, message: message };
  }

  function valid(save) {
    if (!save || typeof save !== "object") return false;
    if (typeof save.scene !== "string" || !has(story.scenes, save.scene)) return false;
    if (!Array.isArray(save.inventory)) return false;
    for (var i = 0; i < save.inventory.length; i++) {
      if (typeof save.inventory[i] !== "string" || !has(story.items, save.inventory[i])) return false;
    }
    if (save.ending !== null && (typeof save.ending !== "string" || !has(story.endings, save.ending))) return false;
    if (!save.decisions || typeof save.decisions !== "object" || Array.isArray(save.decisions)) return false;
    for (var key in save.decisions) {
      if (has(save.decisions, key) && typeof save.decisions[key] !== "string") return false;
    }
    return true;
  }

  function load() {
    var raw;
    try {
      raw = storage.get();
    } catch (error) {
      return memory === null ? null : JSON.parse(JSON.stringify(memory));
    }
    if (raw === null || raw === undefined) return null;
    try {
      var save = JSON.parse(raw);
      return valid(save) ? save : null;
    } catch (error) {
      return null;
    }
  }

  function save(state) {
    memory = JSON.parse(JSON.stringify(state));
    try {
      storage.set(JSON.stringify(state));
    } catch (error) {
      /* storage is blocked: the game keeps working, it just cannot be resumed after a reload */
    }
  }

  function holds(condition, state) {
    var met;
    if (has(condition, "item")) {
      met = state.inventory.indexOf(condition.item) !== -1;
    } else if (condition.any) {
      met = has(state.decisions, condition.decision);
    } else {
      met = has(state.decisions, condition.decision) && state.decisions[condition.decision] === condition.value;
    }
    return condition.not ? !met : met;
  }

  function firstUnmet(requirements, state) {
    for (var i = 0; i < (requirements || []).length; i++) {
      if (!holds(requirements[i], state)) return requirements[i].blocked;
    }
    return null;
  }

  function newGame() {
    save({ scene: story.start, inventory: [], ending: null, decisions: {} });
  }

  function startOver(confirmed) {
    if (load() !== null && !confirmed) {
      return rejected("Starting over erases your progress. Confirm to start a new game.");
    }
    newGame();
    return accepted("A new walk begins in St. Hanshaugen.");
  }

  function loadGame() {
    var state = load();
    if (state === null) return null;
    return { scene: state.scene, inventory: state.inventory.slice(), ending: state.ending };
  }

  function getDecisions() {
    var state = load();
    return state === null ? {} : JSON.parse(JSON.stringify(state.decisions));
  }

  function goTo(sceneId) {
    var state = load();
    if (state === null) return rejected("There is no game in progress.");
    if (state.ending !== null) return rejected(GAME_OVER);
    var moves = story.scenes[state.scene].moves || {};
    if (!has(moves, sceneId)) return rejected("You cannot get there from here.");
    var move = moves[sceneId];
    var blocked = firstUnmet(move.requires, state);
    if (blocked !== null) return rejected(blocked);
    state.scene = sceneId;
    if (story.scenes[sceneId].ending) state.ending = story.scenes[sceneId].ending;
    save(state);
    return accepted(move.message);
  }

  function takeableIn(state) {
    if (state === null || state.ending !== null) return [];
    var found = [];
    for (var id in story.items) {
      if (!has(story.items, id)) continue;
      var item = story.items[id];
      if (item.location === state.scene && state.inventory.indexOf(id) === -1 && firstUnmet(item.requires, state) === null) {
        found.push(id);
      }
    }
    return found;
  }

  function takeableItems() {
    return takeableIn(load());
  }

  function takeItem(itemId) {
    var state = load();
    if (state === null) return rejected("There is no game in progress.");
    if (state.ending !== null) return rejected(GAME_OVER);
    if (!has(story.items, itemId)) return rejected("There is no such thing here.");
    var item = story.items[itemId];
    if (state.inventory.indexOf(itemId) !== -1) return rejected("You already have the " + item.name.toLowerCase() + ".");
    if (item.location !== state.scene) return rejected("There is nothing like that to take here.");
    var blocked = firstUnmet(item.requires, state);
    if (blocked !== null) return rejected(blocked);
    state.inventory.push(itemId);
    save(state);
    return accepted(item.take_message);
  }

  function decide(decision, value) {
    var state = load();
    if (state === null) return rejected("There is no game in progress.");
    if (state.ending !== null) return rejected(GAME_OVER);
    var choices = story.scenes[state.scene].choices || [];
    var choice = null;
    for (var i = 0; i < choices.length; i++) {
      if (choices[i].decision === decision && choices[i].value === value) {
        choice = choices[i];
        break;
      }
    }
    if (choice === null) return rejected("That is not a choice you can make here.");
    if (has(state.decisions, decision)) return rejected("You have already made that choice. It cannot be unmade.");
    var blocked = firstUnmet(choice.requires, state);
    if (blocked !== null) return rejected(blocked);
    state.decisions[decision] = value;
    if (choice.ending) state.ending = choice.ending;
    save(state);
    return accepted(choice.message);
  }

  function sceneView() {
    var state = load();
    if (state === null) return null;
    var scene = story.scenes[state.scene];
    var view = {
      scene: state.scene, title: scene.title, text: scene.text,
      moves: [], takeable: [], choices: [], inventory: [], ending: null
    };
    state.inventory.forEach(function (id) {
      view.inventory.push({ id: id, name: story.items[id].name, description: story.items[id].description });
    });
    var changes = scene.changes || [];
    for (var i = 0; i < changes.length; i++) {
      if (holds(changes[i]["if"], state)) {
        view.text = changes[i].text;
        break;
      }
    }
    if (state.ending !== null) {
      var ending = story.endings[state.ending];
      view.ending = { id: state.ending, title: ending.title, text: ending.text, result: ending.result, kicker: ending.kicker };
      return view;
    }
    var moves = scene.moves || {};
    for (var target in moves) {
      if (!has(moves, target)) continue;
      view.moves.push({ to: target, label: moves[target].label, blocked: firstUnmet(moves[target].requires, state) });
    }
    takeableIn(state).forEach(function (id) {
      view.takeable.push({ id: id, label: "Take the " + story.items[id].name.toLowerCase() });
    });
    (scene.choices || []).forEach(function (choice) {
      if (has(state.decisions, choice.decision)) return;
      if (firstUnmet(choice.requires, state) !== null) return;
      view.choices.push({ decision: choice.decision, value: choice.value, label: choice.label });
    });
    return view;
  }

  return {
    startOver: startOver, loadGame: loadGame, getDecisions: getDecisions, goTo: goTo,
    takeableItems: takeableItems, takeItem: takeItem, decide: decide, sceneView: sceneView
  };
}

if (typeof module !== "undefined" && module.exports) module.exports = { createEngine: createEngine };

"use strict";
/* The screens of Where's Otto? in the browser. All rules live in engine.js, all pictures in art.js. */

(function () {
  var SAVE_KEY = "wheres-otto-save-v1";
  var storage = {
    get: function () { return window.localStorage.getItem(SAVE_KEY); },
    set: function (text) { window.localStorage.setItem(SAVE_KEY, text); },
    clear: function () { window.localStorage.removeItem(SAVE_KEY); }
  };
  var engine = createEngine(STORY, storage);
  var art = createArt(ART_DATA);
  var app = document.getElementById("app");
  var live = document.getElementById("live");
  var ui = { screen: "title", last: null, confirm: false };

  function esc(text) {
    return String(text).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function paw(label, act, kind, a, b) {
    var attributes = ' type="button" class="paw ' + kind + '" data-act="' + act + '"';
    if (a !== undefined) attributes += ' data-a="' + esc(a) + '"';
    if (b !== undefined) attributes += ' data-b="' + esc(b) + '"';
    return "<button" + attributes + ">" + label + "</button>";
  }

  function picture(svg, description) {
    return '<div class="picture" role="img" aria-label="' + esc(description) + '">' + svg + "</div>";
  }

  function describe(view, decisions) {
    if (view.ending) return "Pixel picture of the ending: " + view.ending.title + ".";
    var otto = decisions.rescue === "treat" ? "Otto sits safely beside Benjamin." : "Otto, a white golden retriever with a teal leash, runs away.";
    return "Pixel picture of " + view.title + ". Benjamin and Sofie stand in the autumn wind. " + otto;
  }

  function whisper(result) {
    return '<div class="whisper ' + (result.ok ? "" : "blocked") + '">' + esc(result.message) + "</div>";
  }

  function confirmBox() {
    return (
      '<div class="whisper blocked" role="alert">Starting over will erase your saved progress. This cannot be undone.</div>' +
      '<div class="row">' + paw("Yes, start a new walk", "confirm-yes", "teal") + paw("No, keep my progress", "confirm-no", "teal") + "</div>"
    );
  }

  function titleHtml() {
    var saved = engine.loadGame();
    var html =
      '<h1 class="logo" tabindex="-1" data-focus>WHERE\'S<br>OTTO?</h1>' +
      '<p class="tagline">A windy autumn day in Oslo. One lost dog. One very confident detective.</p>' +
      picture(art.sceneArt("bench", { sofie: "help" }, null), "Pixel picture: Benjamin and Sofie by a bench, while Otto the white golden retriever runs away with his teal leash.");
    if (ui.confirm) return html + confirmBox();
    html += '<div class="actions">';
    if (saved !== null) {
      html += paw(saved.ending ? "See how your last walk ended" : "Resume where you left off", "resume", "");
      html += paw("Start a new walk", "new", "");
    } else {
      html += paw("Start the walk", "begin", "");
    }
    return html + "</div>";
  }

  function gameHtml() {
    var view = engine.sceneView();
    var decisions = engine.getDecisions();
    var html =
      '<div class="place">ST. HANSHAUGEN · OSLO</div>' +
      picture(art.sceneArt(view.scene, decisions, view.ending ? view.ending.id : null), describe(view, decisions)) +
      '<h1 class="scene-title" tabindex="-1" data-focus>' + esc(view.title) + "</h1>";
    if (ui.last) html += whisper(ui.last);
    if (view.ending) {
      var lost = view.ending.result === "lost";
      html +=
        '<div class="ending ' + (lost ? "lost" : "") + '"><div class="kicker">' + esc(view.ending.kicker) + '</div>' +
        '<div class="ending-title">' + esc(view.ending.title) + "</div><p>" + esc(view.ending.text) + "</p></div>";
    } else {
      html += '<p class="scene-text">' + esc(view.text) + "</p>";
    }
    if (ui.confirm) return html + confirmBox();
    if (!view.ending) {
      html += '<div class="actions">';
      if (view.takeable.length || view.choices.length) html += '<div class="section">WHAT BENJAMIN DOES</div>';
      view.takeable.forEach(function (item) { html += paw(esc(item.label), "take", "", item.id); });
      view.choices.forEach(function (choice) { html += paw(esc(choice.label), "decide", "teal", choice.decision, choice.value); });
      html += '<div class="section">WHERE TO</div>';
      view.moves.forEach(function (move) {
        var label = move.blocked
          ? '<span aria-hidden="true">🔒 </span><span class="sr-only">Locked. </span>' + esc(move.label)
          : esc(move.label);
        html += paw(label, "go", move.blocked ? "locked" : "", move.to);
      });
      html += "</div>";
    }
    html += '<div class="section">POCKETS</div>';
    if (!view.inventory.length) html += '<div class="empty">Just keys, a phone and an empty leash loop.</div>';
    view.inventory.forEach(function (item) {
      html += '<div class="item"><b>' + esc(item.name) + "</b><br><span>" + esc(item.description) + "</span></div>";
    });
    html += '<div class="section">THE WALK</div><div class="row">' + paw("Start a new walk", "restart", "menu") + paw("Back to the title", "title", "menu") + "</div>";
    return html;
  }

  function render() {
    if (ui.screen === "game" && engine.loadGame() === null) ui.screen = "title";
    app.innerHTML = ui.screen === "game" ? gameHtml() : titleHtml();
    var heading = app.querySelector("[data-focus]");
    if (heading) heading.focus({ preventScroll: true });
  }

  function handle(act, a, b) {
    if (act === "go") ui.last = engine.goTo(a);
    else if (act === "take") ui.last = engine.takeItem(a);
    else if (act === "decide") ui.last = engine.decide(a, b);
    else if (act === "resume") { ui.screen = "game"; ui.last = null; }
    else if (act === "begin" || act === "new") {
      if (engine.loadGame() === null) { engine.startOver(false); ui.screen = "game"; ui.last = null; }
      else ui.confirm = true;
    }
    else if (act === "restart") ui.confirm = true;
    else if (act === "confirm-yes") { engine.startOver(true); ui.screen = "game"; ui.last = null; ui.confirm = false; }
    else if (act === "confirm-no") ui.confirm = false;
    else if (act === "title") { ui.screen = "title"; ui.last = null; ui.confirm = false; }
    live.textContent = ui.last ? ui.last.message : "";
    render();
    window.scrollTo(0, 0);
  }

  app.addEventListener("click", function (event) {
    var button = event.target.closest("button[data-act]");
    if (button) handle(button.getAttribute("data-act"), button.getAttribute("data-a"), button.getAttribute("data-b"));
  });

  function windLeaves() {
    var seed = 5;
    function random() { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; }
    var colors = ["#f6c344", "#f2a22c", "#e8761f", "#d9531e", "#b8401a"];
    var html = "";
    for (var i = 0; i < 22; i++) {
      html +=
        '<span class="leaf" style="--top:' + Math.round(2 + random() * 90) + "vh;--size:" + [6, 8, 10][Math.floor(random() * 3)] +
        "px;--dur:" + (9 + random() * 9).toFixed(1) + "s;--delay:-" + (random() * 18).toFixed(1) + "s;--drop:" + Math.round(-20 + random() * 50) +
        "vh;--c:" + colors[Math.floor(random() * 5)] + '"><span></span></span>';
    }
    document.getElementById("wind").innerHTML = html;
  }

  document.getElementById("park-bg").innerHTML = art.parkBackground();
  windLeaves();
  render();
})();

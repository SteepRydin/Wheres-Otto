"use strict";
/* The pixel pictures of Where's Otto?, ported from sprites.py. The sprites, the park and the scene
   backgrounds are exported from Python (ART_DATA); this file only decides who stands where. */

function createArt(data) {
  var GROUND = data.ground;
  var OVERLAY = "#7a0f1f";

  function shift(rects, dx, dy) {
    return rects.map(function (r) {
      return [r[0] + dx, r[1] + dy, r[2], r[3], r[4]];
    });
  }

  function person(rects, x, y) {
    return shift(rects, x, y);
  }

  function rectsToSvg(rects) {
    return rects
      .map(function (r) {
        return '<rect x="' + r[0] + '" y="' + r[1] + '" width="' + r[2] + '" height="' + r[3] + '" fill="' + r[4] + '"/>';
      })
      .join("");
  }

  function sceneArt(scene, decisions, ending) {
    var rescue = decisions.rescue === "treat";
    var top = GROUND - data.personH;
    var benjamin = person(data.benjamin, 26, top);
    var sofie = person(data.sofie, decisions.sofie !== "flirt" ? 42 : 48, top);
    var otto = [];
    var extra = [];

    if (ending === "love") {
      sofie = person(data.sofie, 42, top);
      otto = shift(data.ottoSit, 60, GROUND - data.ottoSitH);
      extra = shift(data.heart, 44, 8).concat(shift(data.heart, 36, 14), shift(data.heart, 52, 13));
    } else if (ending === "nonumber") {
      otto = shift(data.ottoSit, 44, GROUND - data.ottoSitH);
      sofie = person(data.sofie, 100, top);
    } else if (ending === "tram") {
      extra = shift(data.tram, 54, 25).concat([[44, GROUND, 12, 1, data.teal], [40, GROUND - 1, 4, 1, data.tealDark]]);
      sofie = person(data.sofie, 40, top);
      benjamin = person(data.benjamin, 20, top);
    } else if (ending === "car") {
      extra = shift(data.car, 72, 25).concat([[54, GROUND, 14, 1, data.teal], [50, GROUND - 1, 4, 1, data.tealDark]]);
      sofie = person(data.sofie, 40, top);
      benjamin = person(data.benjamin, 20, top);
    } else if (rescue) {
      otto = shift(data.ottoSit, 62, GROUND - data.ottoSitH);
    } else {
      var ottoX = scene === "tramstreet" ? 60 : scene === "hill" ? 72 : 74;
      otto = shift(data.ottoRun, ottoX, GROUND - data.ottoRunH);
      extra = [[ottoX - 6, GROUND - 2, 4, 1, "#ffffff"], [ottoX - 10, GROUND - 5, 3, 1, "#ffffff"]];
    }

    if (scene === "tramstreet" && !ending) extra = extra.concat(shift(data.tram, rescue ? 96 : 88, 25));
    if (scene === "carstreet" && !ending) extra = extra.concat(shift(data.car, 80, 26));

    var backdrop = ending === "car" ? "carstreet" : scene;
    var body = data.base + (data.extras[backdrop] || "") + (data.props[scene] || "");
    body += rectsToSvg(benjamin.concat(sofie, otto, extra));
    if (ending === "tram" || ending === "car") {
      body += '<rect opacity="0.28" x="0" y="0" width="' + data.stripW + '" height="' + data.stripH + '" fill="' + OVERLAY + '"/>';
    }
    return (
      '<svg class="strip-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + data.stripW + " " + data.stripH +
      '" preserveAspectRatio="xMidYMid meet" shape-rendering="crispEdges">' + body + "</svg>"
    );
  }

  function parkBackground() {
    return data.parkBackground;
  }

  return { sceneArt: sceneArt, parkBackground: parkBackground };
}

if (typeof module !== "undefined" && module.exports) module.exports = { createArt: createArt };

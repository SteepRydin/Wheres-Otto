# Plot Twist — business requirements (v1.0, 29 September 2026)

Source: https://nova-sbe-introduction-to-programming.github.io/intro-to-programming-2026/weeks/week-05/01-plot-twist-brd.html

*A mystery shaped by the player's choices. 5 scenes · 2 items · 2 endings.*

## The opportunity

A player wants a short mystery they can explore through meaningful decisions. Finding a clue or making a choice changes what is possible, and a player can leave and return without losing progress.

## First release

One original mystery or escape room, roughly ten minutes of play. At least five scenes, two collectible items, two reachable endings. One ending must depend on an earlier choice or item. Text and simple controls; images and sound optional.

## User journey

The player starts a new game, reads the opening scene, explores available choices, and collects items. They use an item or prior decision to unlock a path, reach an ending, and can then start again. If they leave midway, they can resume the same game.

## Required capabilities

- **PT01 Start and resume** — Offer a new game and, when a save exists, a way to resume it. Starting over must ask for confirmation before replacing existing progress.
- **PT02 Explore** — Show the current scene and its available actions. Every accepted choice must produce a visible result (new scene, new information, or a changed condition).
- **PT03 Collect and use** — Let the player inspect their inventory. At least one item must unlock an action. Collecting the same item twice must not create duplicates.
- **PT04 Apply consequences** — At least one remembered decision affects a later action or ending. Explain blocked actions or hide them until their conditions are met.
- **PT05 Finish and replay** — Clearly identify each ending. Once an ending is reached, ordinary story actions stop; the player can review the outcome or start a new game.

## Business rules

- **PT R1** — An action is allowed only when its scene and prerequisite conditions are satisfied. A blocked action must not move the player or change their inventory.
- **PT R2** — An item may be collected only where the story makes it available. Each item can be collected once per game. Items are reusable; using an item does not consume it.
- **PT R3** — Previously visited scenes must reflect remembered changes. Returning to the drawer after taking its key must not offer a second key.
- **PT R4** — A new game resets all player progress while retaining the story content. Every ending must be reachable through valid play from a new game.

## What the product must remember

Story content and its choices, item locations, and conditions. For the active game: current scene, collected items, relevant decisions, and whether an ending has been reached. Save progress after each accepted action.

## Acceptance criteria

- **A1 A locked route** — New game without the key; attempting the locked route is unavailable or rejected. Location and inventory unchanged.
- **A2 An unlocked route** — With the key collected, using the locked route reaches the intended scene. The key remains in inventory.
- **A3 No duplicate collection** — After collecting an item, revisit its location and try again. Inventory still holds one copy.
- **A4 Resume correctly** — Collect an item and make a consequential choice, stop and reopen the app. Resume restores scene, item and choice, and the same routes remain available.
- **A5 Two outcomes** — Two valid paths from separate new games reach two different endings. At an ending, further story actions cannot change the completed game.
- **A6 Restart safely** — Cancel a restart: progress retained. Confirm a restart: opening scene, empty inventory, initial decisions restored.

## Scope boundaries

No visual story editor, procedural generation, multiplayer, combat, or live AI dialogue. Story is supplied content. Accepted changes must survive restarting the app. Rejected actions leave existing data unchanged. Works with supplied content, no paid service or live external integration.

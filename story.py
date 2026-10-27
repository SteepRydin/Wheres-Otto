"""Story content for Last Curtain: scenes, items, endings. Player progress lives in the database, never here."""

START_SCENE = "foyer"

# A condition is {"item": id} or {"decision": id, "value": v}. The first matching "changes" entry replaces a scene's text.

ITEMS = {
    "stage_door_key": {
        "name": "Stage door key",
        "description": "A heavy brass key, cold as a tombstone. The paper tag reads: STAGE - STAFF ONLY.",
        "location": "box_office",
        "take_message": "You ease the drawer open and lift out a brass key. The tag is damp, as if someone had been holding it a moment ago.",
    },
    "porcelain_mask": {
        "name": "Porcelain mask",
        "description": "A pale mask with one painted tear. Every guest wore one at the masquerade. Behind it, you are only a shape.",
        "location": "wardrobe",
        "take_message": "You lift the mask from the mannequin. It is warm. When you hold it up, the eyeholes feel like they are looking back.",
    },
}

SCENES = {
    "foyer": {
        "title": "The Foyer",
        "text": (
            "Operahuset is silent. The glass wall looks over the black fjord, and across the water the Barcode towers "
            "stand dark, like a row of missing teeth. Torn masquerade masks litter the oak of the Wave Wall, every one "
            "of them turned toward the same door: STAGE - STAFF ONLY. Somewhere deep in the building, a woman is humming. "
            "The box office light is still on."
        ),
        "changes": [
            {
                "if": {"item": "stage_door_key"},
                "text": (
                    "The foyer is exactly as you left it, except the masks on the floor have shifted. "
                    "They are all looking at your pocket now. The humming is louder behind the stage door."
                ),
            }
        ],
        "moves": {
            "box_office": {
                "label": "Walk to the box office",
                "message": "Your footsteps echo across the marble. The box office glows like a shrine.",
            },
            "backstage": {
                "label": "Open the stage door",
                "requires": [
                    {
                        "item": "stage_door_key",
                        "blocked": "The stage door is locked. The old brass lock does not give. Someone must have a key.",
                    }
                ],
                "message": "The key turns with a groan. Cold air breathes out of the dark corridor, carrying the humming.",
            },
        },
    },
    "box_office": {
        "title": "The Box Office",
        "text": (
            "Behind the glass, a lamp burns over a counter of unsold tickets, every one for tonight, every one stamped "
            "with a mask. A single drawer under the counter is not quite shut."
        ),
        "changes": [
            {
                "if": {"item": "stage_door_key"},
                "text": (
                    "The drawer hangs open, empty. The tickets on the counter have rearranged themselves into a "
                    "single line pointing toward the foyer."
                ),
            }
        ],
        "moves": {
            "foyer": {"label": "Back to the foyer", "message": "You step out of the lamplight. The foyer feels bigger than before."},
        },
    },
    "backstage": {
        "title": "Backstage Corridor",
        "text": (
            "A narrow corridor of black curtains and hanging ropes. Painted scenery leans in the dark, and on every "
            "peg along the wall hangs a face: masks of plaster, leather and lace. To the left is the wardrobe. "
            "Ahead, a slit of stage light and the humming, close now."
        ),
        "moves": {
            "foyer": {"label": "Back to the foyer", "message": "You pull the door shut behind you. It does not feel like it helps."},
            "wardrobe": {"label": "Enter the wardrobe", "message": "The wardrobe door sighs open."},
            "stage": {"label": "Walk onto the stage", "message": "You step through the curtain and the humming stops."},
        },
    },
    "wardrobe": {
        "title": "The Wardrobe",
        "text": (
            "Rails of gowns sway though there is no draught. Mannequins stand in a ring, each in a gala costume, each "
            "faceless except the last one, which wears a pale porcelain mask with a single painted tear."
        ),
        "changes": [
            {
                "if": {"item": "porcelain_mask"},
                "text": (
                    "The ring of mannequins is complete again, but the last one has no face now. "
                    "You are sure it has turned its head to follow you."
                ),
            }
        ],
        "moves": {
            "backstage": {"label": "Back to the corridor", "message": "The gowns whisper as you pass."},
        },
    },
    "stage": {
        "title": "The Main Stage",
        "text": (
            "The house lights are down and the great red curtain is drawn back on rows and rows of empty seats. "
            "At the center of the stage, in a single pale circle of light, stands a woman in a gown, a porcelain mask "
            "over her face. She stops humming. 'You are not one of us,' she says. 'Who are you under there?' "
            "Behind her, a narrow iron stair climbs into the fly tower, toward the roof."
        ),
        "changes": [
            {
                "if": {"decision": "singer", "value": "silent"},
                "text": (
                    "The singer tilts her head and waits. The seats creak as if the whole empty house is leaning in. "
                    "She has not forgotten you. She is only letting you pass, as long as no one looks too closely at "
                    "your face. The iron stair waits behind her."
                ),
            }
        ],
        "choices": [
            {
                "decision": "singer",
                "value": "answer",
                "label": "Answer her: 'I'm the cleaner.'",
                "message": "Your voice cracks in the huge dark. The singer smiles with a mouth that is not painted on.",
                "ending": "encore",
            },
            {
                "decision": "singer",
                "value": "silent",
                "label": "Say nothing. Stand perfectly still.",
                "message": "You hold your breath. After a long moment, the singer resumes her humming, a little louder, a little pleased.",
            },
        ],
        "moves": {
            "backstage": {"label": "Retreat backstage", "message": "You back into the curtain. She lets you."},
            "roof": {
                "label": "Climb the iron stair to the roof",
                "requires": [
                    {
                        "decision": "singer",
                        "value": "silent",
                        "blocked": "The stair is on the far side of the stage. You cannot cross the light while she is waiting for your answer.",
                    },
                    {
                        "item": "porcelain_mask",
                        "blocked": "She would see your bare face the moment you cross the light. Everyone here wears a mask. You would need one.",
                    },
                ],
                "message": "Mask on, eyes down, you cross the circle of light. The singer does not turn. The stair rings under your feet.",
            },
        },
    },
    "roof": {
        "title": "The Marble Roof",
        "text": "The white marble roof slopes down to the black water.",
        "ending": "escape",
    },
}

ENDINGS = {
    "escape": {
        "title": "The Last Curtain",
        "text": (
            "You step out onto the long white slope of the roof as the night wind hits your face. Across the fjord, "
            "the Barcode towers flicker back to life one window at a time. Behind you, deep in the building, the "
            "humming stops. Down in the water, the glass sculpture turns slowly, like a blade. You are alive. In the "
            "dark windows you see your reflection, and it is still wearing the mask. You do not dare take it off "
            "until sunrise."
        ),
    },
    "encore": {
        "title": "Encore",
        "text": (
            "The house lights blaze up. Every seat is full now, hundreds of masks turned toward you, and they begin "
            "to applaud. You take a bow you don't remember learning. The singer takes your hand and the curtain "
            "falls. Tomorrow the cleaners will find your work clothes folded neatly in the box office, and a new "
            "porcelain mask on the last mannequin, with a single painted tear."
        ),
    },
}

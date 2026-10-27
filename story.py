"""Story content for Where's Otto?: scenes, items, endings. Player progress lives in the database, never here.

A condition is {"item": id}, {"decision": id, "value": v} or {"decision": id, "any": True} (any value).
Add "not": True to flip it. The first matching "changes" entry replaces a scene's text.
"""

START_SCENE = "bench"

ITEMS = {
    "sausage": {
        "name": "Sausage",
        "description": "A warm hot-dog sausage wrapped in a napkin. Otto's greatest weakness.",
        "location": "kiosk",
        "take_message": "'Your dog stole my last sausage and ran toward the playground,' sighs the vendor. 'Here, take another. He will follow it anywhere.'",
    },
    "binoculars": {
        "name": "Toy binoculars",
        "description": "Plastic binoculars with a cracked left lens, tied with pink string. Surprisingly good.",
        "location": "playground",
        "take_message": "'A big white dog? I saw him!' says the girl in the yellow raincoat. 'He ran up the hill with a blue-green rope flying behind him. Take my binoculars. You need them more than me.'",
    },
}

SCENES = {
    "bench": {
        "title": "The Bench",
        "text": (
            "A windy October afternoon in St. Hanshaugen, Oslo. Orange and yellow leaves tumble across the lawn, "
            "and the whole city looks washed in cold gold. Benjamin Ernesto Aaron Hajdarpasic is minding his "
            "friend's golden retriever Otto for the weekend, and he is, by his own estimate, absolutely crushing it "
            "with Sofie, a woman in a red scarf with a laugh like a bicycle bell. Then he glances at the bench arm "
            "where Otto's teal leash was looped. The loop is empty. Otto has gone."
        ),
        "changes": [
            {
                "if": {"decision": "sofie", "value": "help"},
                "text": (
                    "Sofie is already on her feet, scarf flapping like a flag. 'Okay, detective,' she says. 'Where do "
                    "we start?' A path leads to the pond, another to the hot-dog kiosk, and a third across the lawn "
                    "to the playground."
                ),
            },
            {
                "if": {"decision": "sofie", "value": "flirt"},
                "text": (
                    "Sofie has folded her arms. She is following Benjamin mostly to watch him fail. 'So the dog is "
                    "more important than the conversation,' she says. Leaves hiss across the grass. A path leads to "
                    "the pond, another to the hot-dog kiosk, and a third across the lawn to the playground."
                ),
            },
        ],
        "choices": [
            {
                "decision": "sofie",
                "value": "help",
                "label": "Tell Sofie the truth and ask her to help search",
                "message": "Sofie's face goes from amused to determined in one second. 'A missing dog? Come on, I am excellent in a crisis.' She grabs her scarf and stands up.",
            },
            {
                "decision": "sofie",
                "value": "flirt",
                "label": "Keep the charm going: Otto cannot have gone far",
                "message": "'Where was I?' says Benjamin, smoothly ignoring the empty leash. Sofie's smile cools by several degrees. Two minutes later he finally admits the dog is gone, and she follows him anyway with her arms crossed.",
            },
        ],
        "moves": {
            "pond": {
                "label": "Walk to the pond",
                "requires": [
                    {
                        "decision": "sofie",
                        "any": True,
                        "blocked": "Sofie is looking at Benjamin expectantly, and the empty leash is still in his hand. He should say something to her first.",
                    }
                ],
                "message": "The wind pushes them down the path toward the pond.",
            },
            "kiosk": {
                "label": "Walk to the hot-dog kiosk",
                "requires": [
                    {
                        "decision": "sofie",
                        "any": True,
                        "blocked": "Sofie is looking at Benjamin expectantly, and the empty leash is still in his hand. He should say something to her first.",
                    }
                ],
                "message": "The smell of grilled sausage leads the way.",
            },
            "playground": {
                "label": "Cross the lawn to the playground",
                "requires": [
                    {
                        "decision": "sofie",
                        "any": True,
                        "blocked": "Sofie is looking at Benjamin expectantly, and the empty leash is still in his hand. He should say something to her first.",
                    }
                ],
                "message": "Leaves swirl around their ankles as they cross the lawn.",
            },
        },
    },
    "pond": {
        "title": "The Pond",
        "text": (
            "The pond by the fountain ripples in the wind, and the ducks bob like angry corks. Leaves skate across "
            "the water. The muddy bank is a confusing mess of footprints."
        ),
        "changes": [
            {
                "if": {"decision": "sofie", "value": "help"},
                "text": (
                    "Sofie crouches on the muddy bank. 'Look! Wet paw prints, big ones, heading uphill toward the "
                    "playground. And there is sausage grease in them.' She grins up at him. 'You are welcome.'"
                ),
            },
            {
                "if": {"decision": "sofie", "value": "flirt"},
                "text": (
                    "Sofie checks her phone while Benjamin stares at the mud. Prints? Ducks? A dog? The mud says "
                    "nothing useful, and a duck quacks at him in a very judgmental way."
                ),
            },
        ],
        "moves": {
            "bench": {"label": "Back to the bench", "message": "They trudge back up the path."},
        },
    },
    "kiosk": {
        "title": "The Hot-Dog Kiosk",
        "text": (
            "A small kiosk beside the path sells hot dogs and coffee, steam torn sideways by the wind. The vendor is "
            "glaring at a completely empty sausage tray."
        ),
        "changes": [
            {
                "if": {"item": "sausage"},
                "text": (
                    "The vendor nods at Benjamin. 'Told you. Dog went toward the playground, tail up like a flag.' "
                    "He is already guarding the next tray of sausages with his whole body."
                ),
            }
        ],
        "moves": {
            "bench": {"label": "Back to the bench", "message": "The sausage smell follows them up the path."},
        },
    },
    "playground": {
        "title": "The Playground",
        "text": (
            "Children shriek on the swings, flinging leaves by the handful. A girl in a yellow raincoat wears a pair "
            "of toy binoculars and is surveying everything very importantly."
        ),
        "changes": [
            {
                "if": {"item": "binoculars"},
                "text": (
                    "The girl in the yellow raincoat salutes Benjamin from the swings. 'Detective Benjamin! Up the "
                    "hill!' She has already moved on to investigating a pile of leaves."
                ),
            }
        ],
        "moves": {
            "bench": {"label": "Back to the bench", "message": "They cross the lawn again, leaves chasing them."},
            "hill": {"label": "Climb the path up the hill", "message": "The path climbs, and the wind grows stronger with every step."},
        },
    },
    "hill": {
        "title": "The Top of the Hill",
        "text": (
            "From the top of St. Hanshaugen you can see the whole park, and beyond it the gray streets. To the east, "
            "tram tracks run along Ullevålsveien. To the south, cars hiss along a busy road. The wind throws leaves in "
            "Benjamin's eyes. There are a thousand orange blobs down there, and one of them could be a dog."
        ),
        "changes": [
            {
                "if": {"decision": "scan", "value": "tram"},
                "text": (
                    "Benjamin has seen it: a flash of teal in the leaves, a white tail, and Otto standing on the tram "
                    "tracks chasing leaves. Far off, a tram bell clangs. There is no time to lose."
                ),
            }
        ],
        "choices": [
            {
                "decision": "scan",
                "value": "tram",
                "label": "Scan the park with the toy binoculars",
                "requires": [{"item": "binoculars", "blocked": "Without binoculars the park is just a blur of orange."}],
                "message": "Through the cracked left lens Benjamin sweeps the park. There: a flash of teal! A white tail! Otto is on the tram tracks chasing leaves, and a tram bell is ringing in the distance.",
            }
        ],
        "moves": {
            "playground": {"label": "Back down to the playground", "message": "They hurry back down the path."},
            "tramstreet": {
                "label": "Run down to the tram street",
                "requires": [
                    {
                        "decision": "scan",
                        "value": "tram",
                        "blocked": "Benjamin has no idea which street Otto took, and running blindly could be fatal. He needs to see the whole park first.",
                    }
                ],
                "message": "Benjamin runs down the slope, Sofie at his heels, with the tram bell growing louder.",
            },
            "carstreet": {"label": "Run down to the busy car road", "message": "They scramble down toward the roaring traffic."},
        },
    },
    "carstreet": {
        "title": "The Busy Road",
        "text": (
            "Cars roar past in a hiss of wet leaves. There is no dog here. A delivery driver leans out of his van and "
            "shouts over the engine: 'White dog with a blue leash? He ran toward the trams ten minutes ago! Crazy "
            "dog!' Benjamin swears quietly and looks back up the hill."
        ),
        "moves": {
            "hill": {"label": "Climb back up the hill", "message": "They climb back up, lungs burning."},
        },
    },
    "tramstreet": {
        "title": "The Tram Tracks",
        "text": (
            "Ullevålsveien. Otto is standing on the tracks, tail wagging, trying to catch a flying leaf, the teal leash "
            "trailing behind him. Down the street a tram thunders closer, bell clanging. Sofie grabs Benjamin's "
            "sleeve. 'Careful,' she whispers. 'If he panics...'"
        ),
        "changes": [
            {
                "if": {"decision": "rescue", "value": "treat"},
                "text": (
                    "Otto is safe, sitting on Benjamin's shoe and chewing a sausage with an expression of total "
                    "innocence. The tram rattles past, its bell ringing for nobody. Sofie is looking at Benjamin as "
                    "if seeing him for the first time."
                ),
            }
        ],
        "choices": [
            {
                "decision": "rescue",
                "value": "treat",
                "label": "Crouch, hold out the sausage and call softly",
                "requires": [{"item": "sausage", "blocked": "Benjamin has nothing to lure Otto with."}],
                "message": "Benjamin crouches, unwraps the sausage, and speaks in the calm voice he usually saves for phone calls to the bank. Otto's ears go up. He trots off the tracks and sits on Benjamin's shoe. The tram thunders past a hand's breadth away.",
            },
            {
                "decision": "rescue",
                "value": "grab",
                "label": "Lunge for the trailing leash",
                "message": "Benjamin dives for the teal leash. Startled, Otto bolts straight along the tracks, and the bell turns into a long scream of brakes.",
                "ending": "tram",
            },
            {
                "decision": "rescue",
                "value": "shout",
                "label": "Shout Otto's name and run at him",
                "message": "'OTTO!' Benjamin bellows and charges. Otto, spooked, bolts off the tracks and straight into the road, where a car is coming.",
                "ending": "car",
            },
            {
                "decision": "finish",
                "value": "thank",
                "label": "Thank Sofie for helping and ask her out properly",
                "requires": [
                    {"decision": "rescue", "value": "treat", "blocked": "Otto is not safe yet."},
                    {"decision": "sofie", "value": "help", "blocked": "Sofie has not been helping, so there is nothing to thank her for."},
                ],
                "message": "'I could not have found him without you,' says Benjamin, completely honest for once. 'Would you like to get coffee? With Otto, obviously.'",
                "ending": "love",
            },
            {
                "decision": "finish",
                "value": "apologize",
                "label": "Apologize for flirting while Otto was in danger",
                "requires": [
                    {"decision": "rescue", "value": "treat", "blocked": "Otto is not safe yet."},
                    {"decision": "sofie", "value": "flirt", "blocked": "Benjamin has nothing to apologize for."},
                ],
                "message": "'I am sorry I kept flirting when Otto was missing,' says Benjamin. Sofie nods slowly. 'That is something.'",
                "ending": "nonumber",
            },
            {
                "decision": "finish",
                "value": "brag",
                "label": "Boast that you are basically Oslo's best detective",
                "requires": [{"decision": "rescue", "value": "treat", "blocked": "Otto is not safe yet."}],
                "message": "'Elementary,' says Benjamin, flicking a leaf off his shoulder. 'I deduce everything. I am basically Oslo's best detective.' Sofie's smile fades.",
                "ending": "nonumber",
            },
        ],
        "moves": {
            "hill": {"label": "Retreat up the hill", "message": "Benjamin backs away from the tracks and climbs the hill."},
        },
    },
}

ENDINGS = {
    "love": {
        "title": "Best Weekend Ever",
        "result": "won",
        "kicker": "BEST ENDING · OTTO IS SAFE",
        "text": (
            "Sofie smiles, properly, the kind that reaches her eyes. 'Yes,' she says. 'I would like that. And "
            "Benjamin... that was impressive.' She writes her number on his hand with a pen from her bag while the "
            "wind throws a blizzard of orange and yellow leaves around them. Otto, delighted, barks at the sky. "
            "Benjamin Ernesto Aaron Hajdarpasic decides this is the best Saturday of his life."
        ),
    },
    "nonumber": {
        "title": "No Number",
        "result": "won",
        "kicker": "OTTO IS SAFE · BUT NO NUMBER",
        "text": (
            "'I am glad Otto is safe,' says Sofie, tying her scarf against the wind. 'Good luck with the detective "
            "thing.' She walks away across the leaves without leaving her number and without looking back. Otto "
            "sighs and leans his whole weight against Benjamin's leg. At least one of them is happy."
        ),
    },
    "tram": {
        "title": "The Last Tram",
        "result": "lost",
        "kicker": "GAME OVER · THE LAST TRAM",
        "text": (
            "There is a sound Benjamin will never forget: the long scream of tram brakes, and then the silence. The "
            "wind keeps blowing leaves across the tracks as if nothing has happened. Sofie holds his arm. He is "
            "still holding the empty teal leash. He will have to call his friend, and he has no idea how."
        ),
    },
    "car": {
        "title": "Brake Lights",
        "result": "lost",
        "kicker": "GAME OVER · BRAKE LIGHTS",
        "text": (
            "A screech of tires, then a silence that is worse than any noise. Benjamin stands on the pavement "
            "holding an empty teal leash while the wind drags the leaves across the road. Somewhere a car door "
            "opens. Sofie says nothing. He will have to call his friend, and he has no words."
        ),
    },
}

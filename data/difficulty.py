"""
data/difficulty.py - settings for the Easy / Medium / Hard levels
"""

# ---- Difficulty levels -------------------------------------------------------
# Every level is a dictionary of settings. The game reads these numbers, so
# you can change a level just by editing the numbers here.
#   actions          : how many searches / questions the player gets
#   questions        : how many final questions are asked after a correct accusation
#   hints            : how many hints the player can use (a hint costs HINT_COST points)
#   wrong_penalty    : points lost for accusing the wrong person
#   waste_penalty    : EXTRA actions lost when a search / question finds nothing new
#   bonus_per_action : speed bonus for each unused action
#   ranks            : score needed for (Legendary, Senior, Junior)
HINT_COST = 5

DIFFICULTY = {
    "Easy": {
        "actions": 20, "questions": 3, "hints": 3,
        "wrong_penalty": 10, "waste_penalty": 0, "bonus_per_action": 1,
        "ranks": (200, 150, 100),
        "description": "20 actions | 3 hints | 3 final questions | "
                       "wrong accusation -10",
    },
    "Medium": {
        "actions": 20, "questions": 5, "hints": 1,
        "wrong_penalty": 25, "waste_penalty": 0, "bonus_per_action": 2,
        "ranks": (230, 180, 120),
        "description": "20 actions | 1 hint | 5 final questions | "
                       "wrong accusation -25",
    },
    "Hard": {
        "actions": 20, "questions": 7, "hints": 0,
        "wrong_penalty": 40, "waste_penalty": 1, "bonus_per_action": 3,
        "ranks": (260, 200, 140),
        "description": "20 actions | no hints | 7 final questions | wrong accusation -40 | "
                       "a wasted move costs 1 extra action",
    },
}

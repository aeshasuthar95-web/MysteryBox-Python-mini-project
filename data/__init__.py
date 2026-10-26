"""
data package - all the game data (no game logic here)

    CASES       : the four mystery cases
    DIFFICULTY  : settings for the Easy / Medium / Hard levels
    HINT_COST   : points lost when the player uses a hint

How one case is built (see diamond.py, painting.py ...):

    title, story, culprit      text and the key of the real culprit
    locations                  places the player can search   {key: name}
    suspects                   people the player can question
        name, role, intro      shown on the buttons and at the start
        testimony              list of things the suspect can say
            id                 name of the statement
            requires           ids (clues / statements) the player must know first
            text               what the suspect says
            unlocks            a clue that is added when this is said (or None)
    clues                      things the player can find
        place                  where it is found (None = only found by questioning)
        requires               ids the player must know first (this unlocks clues in steps)
        text                   the clue text
    questions                  final questions after a correct accusation
        options, answer        answers (shown in random order) and the right one

To add a new case: copy one of the case files, edit it and add it to CASES below.
"""

from data.difficulty import DIFFICULTY, HINT_COST
from data.diamond import CASE as DIAMOND
from data.painting import CASE as PAINTING
from data.exam import CASE as EXAM
from data.train import CASE as TRAIN

CASES = {
    "diamond": DIAMOND,
    "painting": PAINTING,
    "exam": EXAM,
    "train": TRAIN,
}

__all__ = ["CASES", "DIFFICULTY", "HINT_COST"]

"""
logic/game.py - the rules of MysteryBox

The Game class keeps the state of one game (score, actions, clues ...) and
contains all the rules. It does not use tkinter, so it can be tested on its own.

Every action method returns a list of messages. Each message is a tuple
(tag, text), for example ("clue", "NEW CLUE (+10): ..."). The window (gui/app.py)
shows these messages in the investigation log.

Tags used: heading, clue, speech, info, bad, good
"""

import random

from data import CASES, DIFFICULTY, HINT_COST

# points
CLUE_POINTS = 10          # for every new clue
STATEMENT_POINTS = 5      # for every new statement from a suspect
CULPRIT_POINTS = 50       # for naming the right culprit
QUIZ_POINTS = 10          # for every correct final answer


class Game:
    """One game of MysteryBox."""

    def __init__(self, case_key, level_name):
        self.case_key = case_key
        self.case = CASES[case_key]
        self.level_name = level_name
        self.level = DIFFICULTY[level_name]

        self.score = 0
        self.actions_left = self.level["actions"]
        self.hints_left = self.level["hints"]
        self.found_clues = []     # ids of the clues the player has found
        self.heard = []           # ids of the statements the player has heard
        self.notebook = []        # entries for the notebook: (kind, text)
        self.over = False
        self.accused_right = False

        # pick random final questions for this game
        self.questions = random.sample(self.case["questions"], self.level["questions"])

    # ------------------------------------------------------------------
    # small helper methods
    # ------------------------------------------------------------------
    @property
    def total_clues(self):
        return len(self.case["clues"])

    @property
    def time_is_up(self):
        return self.actions_left <= 0 and not self.over

    def knows(self, requires):
        """True if the player already knows every clue / statement in the list."""
        known = self.found_clues + self.heard
        for item in requires:
            if item not in known:
                return False
        return True

    def _add_clue(self, clue_id):
        """Save a clue in the notebook. Returns False if it was already found."""
        if clue_id in self.found_clues:
            return False
        self.found_clues.append(clue_id)
        self.score += CLUE_POINTS
        self.notebook.append(("clue", self.case["clues"][clue_id]["text"]))
        return True

    def _next_clue_at(self, place):
        """Return the id of the next clue the player can find at a place (or None)."""
        for clue_id, clue in self.case["clues"].items():
            if (clue["place"] == place
                    and clue_id not in self.found_clues
                    and self.knows(clue["requires"])):
                return clue_id
        return None

    def _next_statement(self, suspect_key):
        """Return the next statement a suspect can say (or None)."""
        for line in self.case["suspects"][suspect_key]["testimony"]:
            if line["id"] not in self.heard and self.knows(line["requires"]):
                return line
        return None

    def _nothing_found(self, text):
        """The move gave nothing new. On Hard level it costs extra actions."""
        messages = [("info", text)]
        extra = self.level["waste_penalty"]
        if extra > 0:
            self.actions_left = max(0, self.actions_left - extra)
            messages.append(("bad", "Wasted move! You lose " + str(extra) + " extra action."))
        return messages

    # ------------------------------------------------------------------
    # player actions
    # ------------------------------------------------------------------
    def search(self, place):
        """Search a location. May give a new clue."""
        if self.over:
            return []
        self.actions_left -= 1
        messages = [("heading", "> You search " + self.case["locations"][place] + "...")]

        clue_id = self._next_clue_at(place)
        if clue_id is None:
            messages += self._nothing_found("Nothing new here. Maybe you need more information first.")
        else:
            self._add_clue(clue_id)
            messages.append(("clue", "NEW CLUE (+" + str(CLUE_POINTS) + "): "
                             + self.case["clues"][clue_id]["text"]))
        return messages

    def question(self, suspect_key):
        """Question a suspect. Gives the next statement and maybe a new clue."""
        if self.over:
            return []
        suspect = self.case["suspects"][suspect_key]
        self.actions_left -= 1
        messages = [("heading", "> You question " + suspect["name"] + "...")]

        line = self._next_statement(suspect_key)
        if line is None:
            messages += self._nothing_found("They have nothing more to say. Find more evidence first.")
            return messages

        self.heard.append(line["id"])
        self.score += STATEMENT_POINTS
        self.notebook.append(("said", suspect["name"] + ': "' + line["text"] + '"'))
        messages.append(("speech", '"' + line["text"] + '"  (+' + str(STATEMENT_POINTS) + ")"))

        if line["unlocks"] is not None and self._add_clue(line["unlocks"]):
            messages.append(("clue", "NEW CLUE (+" + str(CLUE_POINTS) + "): "
                             + self.case["clues"][line["unlocks"]]["text"]))
        return messages

    def use_hint(self):
        """Tell the player one move that will find something new (costs points)."""
        if self.over or self.hints_left <= 0:
            return []

        ideas = []
        for place, name in self.case["locations"].items():
            if self._next_clue_at(place) is not None:
                ideas.append("Try searching " + name + ".")
        for key, suspect in self.case["suspects"].items():
            if self._next_statement(key) is not None:
                ideas.append("Try questioning " + suspect["name"] + ".")

        if len(ideas) == 0:
            # nothing left to find, so the hint is free and not used up
            return [("heading", "HINT: You have found everything you can reach. "
                                "Read your notebook and make your accusation!")]

        self.hints_left -= 1
        self.score -= HINT_COST
        return [("heading", "HINT (-" + str(HINT_COST) + "): " + random.choice(ideas))]

    # ------------------------------------------------------------------
    # accusation and final questions
    # ------------------------------------------------------------------
    def accuse(self, suspect_key):
        """Accuse a suspect. A wrong accusation ends the game."""
        name = self.case["suspects"][suspect_key]["name"]
        messages = [("heading", "You accuse " + name + "...")]

        if suspect_key != self.case["culprit"]:
            penalty = self.level["wrong_penalty"]
            self.score -= penalty
            self.over = True
            messages.append(("bad", "WRONG! The real culprit escapes into the night. (-"
                             + str(penalty) + ")"))
            return messages

        self.accused_right = True
        self.score += CULPRIT_POINTS
        messages.append(("good", "CORRECT! You caught the culprit! (+" + str(CULPRIT_POINTS) + ")"))
        return messages

    def check_answer(self, number, question, chosen):
        """Check one final question. 'number' is the question number (1, 2, 3 ...)."""
        if chosen == question["answer"]:
            self.score += QUIZ_POINTS
            return [("good", "Question " + str(number) + ": Correct! (+" + str(QUIZ_POINTS) + ")")]
        return [("bad", "Question " + str(number) + ": Wrong. Answer: " + question["answer"])]

    def finish(self):
        """Add the speed bonus and close the game after the final questions."""
        messages = []
        bonus = self.actions_left * self.level["bonus_per_action"]
        if bonus > 0:
            self.score += bonus
            messages.append(("good", "Speed bonus: +" + str(bonus)))
        self.over = True
        return messages

    def rank(self):
        """Rank title for the final score (the limits depend on the level)."""
        legendary, senior, junior = self.level["ranks"]
        if self.score >= legendary:
            return "Legendary Detective"
        elif self.score >= senior:
            return "Senior Inspector"
        elif self.score >= junior:
            return "Junior Detective"
        return "Rookie"

    def summary_lines(self):
        """Lines for the final result."""
        return [
            "Case        : " + self.case["title"],
            "Difficulty  : " + self.level_name,
            "Final score : " + str(self.score),
            "Clues found : " + str(len(self.found_clues)) + " / " + str(self.total_clues),
            "Rank        : " + self.rank(),
        ]


def shuffled_options(question):
    """Return the answers of a question in a random order."""
    options = list(question["options"])
    random.shuffle(options)
    return options

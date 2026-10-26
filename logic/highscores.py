"""
logic/highscores.py - saves and loads the best scores in a small JSON file

The file highscores.json is created in the main project folder the first time
a score is saved.
"""

import json
import os

# the file is saved in the main project folder (one level above this logic folder)
PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCORE_FILE = os.path.join(PROJECT_FOLDER, "highscores.json")
MAX_SCORES = 10


def load_scores():
    """Read the scores from the file. Returns an empty list if there is no file."""
    if not os.path.exists(SCORE_FILE):
        return []
    try:
        with open(SCORE_FILE, "r", encoding="utf-8") as f:
            scores = json.load(f)
    except (ValueError, OSError):
        return []          # broken or unreadable file: start again with an empty list
    if not isinstance(scores, list):
        return []
    return scores


def save_score(name, score, case_title, level):
    """Add a score to the list and keep only the best ones."""
    scores = load_scores()
    scores.append({"name": name, "score": score, "case": case_title, "level": level})
    scores.sort(key=lambda entry: entry["score"], reverse=True)
    scores = scores[:MAX_SCORES]
    try:
        with open(SCORE_FILE, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2)
    except OSError:
        return False
    return True

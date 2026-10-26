"""
gui/theme.py - colours, fonts and the coloured button used in the window

All colours are written here in one place, so the look of the game
can be changed by editing only this file.
"""

import tkinter as tk

# ---- colours ------------------------------------------------------------
WINDOW_BG = "#eaf0f6"        # light blue-grey window background
HEADER_BG = "#1f4e79"        # dark blue title bar
HEADER_TEXT = "#ffffff"
HEADER_SUB = "#aed6f1"
STATUS_BG = "#d6e4f0"        # bar with score / actions / clues / hints
LOG_BG = "#ffffff"           # investigation log
NOTEBOOK_BG = "#fff9e0"      # notebook looks like yellow paper
BORDER = "#9fb3c8"

BLUE = "#2e86c1"             # place buttons
BLUE_HOVER = "#2471a3"
ORANGE = "#e67e22"           # suspect buttons
ORANGE_HOVER = "#ca6f1e"
GREEN = "#27ae60"            # new game button
GREEN_HOVER = "#1e8449"
YELLOW = "#f4d03f"           # hint button
YELLOW_HOVER = "#d4ac0d"
RED = "#c0392b"              # accusation button
RED_HOVER = "#922b21"
GREY = "#bdc3c7"             # disabled buttons
GREY_TEXT = "#7f8c8d"

# colours of the text in the log and notebook
TEXT_HEADING = "#1b2631"
TEXT_CLUE = "#1e8449"
TEXT_SPEECH = "#1a5276"
TEXT_BAD = "#c0392b"
TEXT_INFO = "#566573"

# colours of the three level buttons
LEVEL_COLORS = {"Easy": "#1e8449", "Medium": "#d68910", "Hard": "#c0392b"}

# ---- fonts --------------------------------------------------------------
FONT = "Segoe UI"            # normal Windows font (tkinter uses another one if missing)
FONT_NORMAL = (FONT, 10)
FONT_BOLD = (FONT, 10, "bold")
FONT_TITLE = (FONT, 20, "bold")
FONT_BIG = (FONT, 12, "bold")


class ColorButton(tk.Button):
    """A flat coloured button that changes colour when the mouse is over it."""

    def __init__(self, parent, text, command, color, hover, text_color="white", **options):
        tk.Button.__init__(self, parent, text=text, command=command, bg=color, fg=text_color,
                           activebackground=hover, activeforeground=text_color,
                           relief="flat", bd=0, padx=12, pady=6, cursor="hand2",
                           font=FONT_BOLD, **options)
        self.color = color
        self.hover = hover
        self.text_color = text_color
        self.bind("<Enter>", self.mouse_enter)
        self.bind("<Leave>", self.mouse_leave)

    def mouse_enter(self, event):
        if str(self["state"]) == "normal":
            self.config(bg=self.hover)

    def mouse_leave(self, event):
        if str(self["state"]) == "normal":
            self.config(bg=self.color)

    def enable(self):
        self.config(state="normal", bg=self.color, fg=self.text_color, cursor="hand2")

    def disable(self):
        self.config(state="disabled", bg=GREY, disabledforeground=GREY_TEXT, cursor="arrow")

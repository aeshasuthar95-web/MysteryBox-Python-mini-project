"""
gui/dialogs.py - the small pop-up windows of the game

    ask_accusation()    "Who is the culprit?"
    ask_question()      one final question with four answers
    show_high_scores()  the list of best scores

Each function waits until the player closes the window and then gives the
answer back, so the main window only has to call it like a normal function.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from gui import theme
from gui.theme import ColorButton
from logic.game import shuffled_options


def make_dialog(parent, title, closable=True):
    """Create an empty pop-up window."""
    win = tk.Toplevel(parent)
    win.title(title)
    win.config(bg=theme.WINDOW_BG)
    win.resizable(False, False)
    win.transient(parent)
    if not closable:
        win.protocol("WM_DELETE_WINDOW", lambda: None)    # the player must answer
    return win


def show_dialog(parent, win):
    """Put the pop-up in the middle of the main window and block the main window."""
    win.update_idletasks()
    x = parent.winfo_rootx() + (parent.winfo_width() - win.winfo_width()) // 2
    y = parent.winfo_rooty() + (parent.winfo_height() - win.winfo_height()) // 3
    win.geometry("+" + str(max(x, 0)) + "+" + str(max(y, 0)))
    win.wait_visibility()
    win.grab_set()


def make_header(win, text):
    """Blue title bar at the top of a pop-up."""
    tk.Label(win, text=text, bg=theme.HEADER_BG, fg=theme.HEADER_TEXT, font=theme.FONT_BIG,
             padx=25, pady=10, wraplength=380, justify="left", anchor="w").pack(fill="x")


def make_radio(win, text, value, variable):
    radio = tk.Radiobutton(win, text=text, value=value, variable=variable,
                           bg=theme.WINDOW_BG, activebackground=theme.WINDOW_BG,
                           selectcolor="white", font=theme.FONT_NORMAL, anchor="w")
    radio.pack(fill="x", padx=30, pady=3)


def ask_accusation(parent, suspects, forced=False):
    """Ask who the culprit is. Returns the key of the suspect, or None if cancelled."""
    win = make_dialog(parent, "Make an accusation", closable=not forced)
    make_header(win, "Who is the culprit?")

    choice = tk.StringVar(value="")
    for key, suspect in suspects.items():
        make_radio(win, suspect["name"] + " (" + suspect["role"] + ")", key, choice)

    result = {"key": None}

    def accuse():
        if choice.get() == "":
            messagebox.showwarning("Accusation", "Please choose a suspect.", parent=win)
            return
        result["key"] = choice.get()
        win.destroy()

    buttons = tk.Frame(win, bg=theme.WINDOW_BG)
    buttons.pack(pady=15)
    ColorButton(buttons, "Accuse", accuse, theme.RED, theme.RED_HOVER).pack(side="left", padx=5)
    if not forced:
        ColorButton(buttons, "Cancel", win.destroy, "#7f8c8d", "#626567").pack(side="left", padx=5)

    show_dialog(parent, win)
    parent.wait_window(win)
    return result["key"]


def ask_question(parent, number, total, question):
    """Show one final question. Returns the answer the player chose."""
    win = make_dialog(parent, "Question " + str(number) + " of " + str(total), closable=False)
    make_header(win, "Question " + str(number) + " of " + str(total))

    tk.Label(win, text=question["question"], bg=theme.WINDOW_BG, fg=theme.TEXT_HEADING,
             font=theme.FONT_BIG, wraplength=380, justify="left",
             padx=25, pady=12).pack(anchor="w")

    choice = tk.StringVar(value="")
    for option in shuffled_options(question):
        make_radio(win, option, option, choice)

    def submit():
        if choice.get() == "":
            messagebox.showwarning("Question", "Please choose an answer.", parent=win)
            return
        win.destroy()

    text = "Submit" if number == total else "Next"
    ColorButton(win, text, submit, theme.GREEN, theme.GREEN_HOVER).pack(pady=15)

    show_dialog(parent, win)
    parent.wait_window(win)
    return choice.get()


def show_high_scores(parent, scores):
    """Show the high score list in a table."""
    win = make_dialog(parent, "High scores")
    make_header(win, "High scores")

    if len(scores) == 0:
        tk.Label(win, text="No scores saved yet. Solve a case to be the first!",
                 bg=theme.WINDOW_BG, font=theme.FONT_NORMAL, padx=30, pady=30).pack()
    else:
        table = ttk.Treeview(win, columns=("place", "name", "score", "case", "level"),
                             show="headings", height=min(len(scores), 10))
        for column, title, width in (("place", "#", 35), ("name", "Name", 120),
                                     ("score", "Score", 60), ("case", "Case", 215),
                                     ("level", "Level", 70)):
            table.heading(column, text=title)
            table.column(column, width=width, anchor="w")

        table.tag_configure("first", background="#fcf3cf")      # gold for the best score
        table.tag_configure("odd", background="#eaf0f6")
        for number, entry in enumerate(scores, start=1):
            if number == 1:
                tag = "first"
            elif number % 2 == 0:
                tag = "odd"
            else:
                tag = ""
            table.insert("", "end", tags=(tag,),
                         values=(number, entry["name"], entry["score"],
                                 entry["case"], entry["level"]))
        table.pack(padx=20, pady=(15, 5))

    ColorButton(win, "Close", win.destroy, theme.BLUE, theme.BLUE_HOVER).pack(pady=15)
    show_dialog(parent, win)

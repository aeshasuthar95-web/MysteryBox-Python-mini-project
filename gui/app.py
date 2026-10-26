"""
gui/app.py - the main window of MysteryBox

This file builds the window and connects the buttons to the game rules
(logic/game.py). The pop-up windows are in gui/dialogs.py and the colours
are in gui/theme.py.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from data import CASES, DIFFICULTY, HINT_COST
from gui import dialogs, theme
from gui.theme import ColorButton
from logic import highscores
from logic.game import Game

HOW_TO_PLAY = (
    "Goal: find out who committed the crime.\n\n"
    "1. Choose a case and a difficulty level, then press New Game.\n"
    "2. Click a place to search it, or a suspect to question them.\n"
    "   Every search or question uses one action.\n"
    "3. New clues go into the Detective notebook. Some clues and\n"
    "   statements only appear after you found other clues first.\n"
    "4. A hint tells you one move that will find something new.\n"
    "   It costs " + str(HINT_COST) + " points.\n"
    "5. When you are sure, press Make Accusation.\n"
    "   If you are right you must answer some final questions.\n"
    "   If you are wrong, the game ends and you lose points.\n\n"
    "Points: new clue +10, new statement +5, right culprit +50,\n"
    "right final answer +10, speed bonus for every unused action."
)


class MysteryBoxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MysteryBox - Detective Game")
        self.root.geometry("1050x730")
        self.root.minsize(920, 650)
        self.root.config(bg=theme.WINDOW_BG)

        self.game = None
        self.case_keys = list(CASES.keys())
        self.action_buttons = []      # the place and suspect buttons of the current case

        self.setup_style()
        self.build_menu()
        self.build_header()
        self.build_controls()
        self.build_status_bar()
        self.build_bottom_bar()       # packed before the body so it never gets hidden
        self.build_body()

        self.new_game(ask=False)

    # ------------------------------------------------------------------
    # building the window
    # ------------------------------------------------------------------
    def setup_style(self):
        """Choose a good-looking theme for the combo box and the table."""
        style = ttk.Style()
        names = style.theme_names()
        if "vista" in names:
            style.theme_use("vista")
        elif "aqua" not in names and "clam" in names:
            style.theme_use("clam")

    def build_menu(self):
        menubar = tk.Menu(self.root)

        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="New Game", accelerator="Ctrl+N", command=self.new_game)
        game_menu.add_command(label="High Scores", command=self.show_high_scores)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="Game", menu=game_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="How to Play", command=self.show_how_to_play)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)
        self.root.bind("<Control-n>", lambda event: self.new_game())

    def build_header(self):
        """Dark blue bar with the title and the New Game button."""
        header = tk.Frame(self.root, bg=theme.HEADER_BG)
        header.pack(fill="x")

        titles = tk.Frame(header, bg=theme.HEADER_BG)
        titles.pack(side="left", padx=20, pady=10)
        tk.Label(titles, text="MysteryBox", bg=theme.HEADER_BG, fg=theme.HEADER_TEXT,
                 font=theme.FONT_TITLE).pack(anchor="w")
        tk.Label(titles, text="Detective Game", bg=theme.HEADER_BG, fg=theme.HEADER_SUB,
                 font=theme.FONT_NORMAL).pack(anchor="w")

        ColorButton(header, "New Game", self.new_game, theme.GREEN, theme.GREEN_HOVER
                    ).pack(side="right", padx=20)

    def build_controls(self):
        """Row with the case list and the three difficulty buttons."""
        controls = tk.Frame(self.root, bg=theme.WINDOW_BG)
        controls.pack(fill="x", padx=15, pady=(10, 0))

        tk.Label(controls, text="Case:", bg=theme.WINDOW_BG, font=theme.FONT_BOLD).pack(side="left")
        titles = [CASES[key]["title"] for key in self.case_keys]
        self.case_box = ttk.Combobox(controls, values=titles, state="readonly", width=30)
        self.case_box.current(0)
        self.case_box.pack(side="left", padx=(6, 25))

        tk.Label(controls, text="Level:", bg=theme.WINDOW_BG, font=theme.FONT_BOLD).pack(side="left")
        self.level_var = tk.StringVar(value="Medium")
        for level_name in DIFFICULTY:
            color = theme.LEVEL_COLORS[level_name]
            tk.Radiobutton(controls, text=level_name, value=level_name, variable=self.level_var,
                           command=self.update_level_info, bg=theme.WINDOW_BG,
                           activebackground=theme.WINDOW_BG, selectcolor="white",
                           fg=color, activeforeground=color,
                           font=theme.FONT_BOLD).pack(side="left", padx=6)

        self.level_info = tk.Label(self.root, bg=theme.WINDOW_BG, fg=theme.TEXT_INFO,
                                   font=theme.FONT_NORMAL, anchor="w")
        self.level_info.pack(fill="x", padx=15, pady=(2, 8))
        self.update_level_info()

    def build_status_bar(self):
        """Light blue bar with score, actions left, clues found, hints left and level."""
        bar = tk.Frame(self.root, bg=theme.STATUS_BG, bd=1, relief="solid")
        bar.pack(fill="x", padx=15, pady=(0, 8))

        self.score_label = self.make_stat(bar, "SCORE", "#1e8449")
        self.actions_label = self.make_stat(bar, "ACTIONS LEFT", "#1f618d")
        self.clues_label = self.make_stat(bar, "CLUES FOUND", "#7d3c98")
        self.hints_label = self.make_stat(bar, "HINTS LEFT", "#d68910")
        self.level_label = self.make_stat(bar, "LEVEL", "#1b2631")

    def make_stat(self, parent, caption, color):
        """One box of the status bar: a small caption and a big coloured value."""
        box = tk.Frame(parent, bg=theme.STATUS_BG)
        box.pack(side="left", expand=True, pady=6)
        tk.Label(box, text=caption, bg=theme.STATUS_BG, fg=theme.TEXT_INFO,
                 font=(theme.FONT, 8, "bold")).pack()
        value = tk.Label(box, text="0", bg=theme.STATUS_BG, fg=color,
                         font=(theme.FONT, 15, "bold"))
        value.pack()
        return value

    def build_bottom_bar(self):
        bottom = tk.Frame(self.root, bg=theme.WINDOW_BG)
        bottom.pack(side="bottom", fill="x", padx=15, pady=(4, 12))

        self.hint_button = ColorButton(bottom, "Get Hint", self.on_hint, theme.YELLOW,
                                       theme.YELLOW_HOVER, text_color=theme.TEXT_HEADING)
        self.hint_button.pack(side="left")
        self.accuse_button = ColorButton(bottom, "Make Accusation", self.on_accuse,
                                         theme.RED, theme.RED_HOVER)
        self.accuse_button.pack(side="left", padx=10)

    def build_body(self):
        body = tk.Frame(self.root, bg=theme.WINDOW_BG)
        body.pack(fill="both", expand=True, padx=15)
        body.columnconfigure(1, weight=3)
        body.columnconfigure(2, weight=2)
        body.rowconfigure(0, weight=1)

        # left side: buttons for places and suspects (made again for every case)
        left = tk.Frame(body, bg=theme.WINDOW_BG)
        left.grid(row=0, column=0, sticky="n", padx=(0, 10))
        self.places_frame = self.make_group(left, "Investigate")
        self.places_frame.pack(fill="x")
        self.suspects_frame = self.make_group(left, "Question a suspect")
        self.suspects_frame.pack(fill="x", pady=(10, 0))

        # middle: investigation log (white)
        log_frame = self.make_group(body, "Investigation log")
        log_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        self.log_text = self.make_text_box(log_frame, theme.LOG_BG)

        # right side: notebook (yellow paper)
        note_frame = self.make_group(body, "Detective notebook")
        note_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        self.note_text = self.make_text_box(note_frame, theme.NOTEBOOK_BG)

    def make_group(self, parent, title):
        return tk.LabelFrame(parent, text=title, bg=theme.WINDOW_BG, fg=theme.HEADER_BG,
                             font=theme.FONT_BOLD, padx=8, pady=8)

    def make_text_box(self, parent, background):
        """A read-only text box with a scroll bar and coloured text styles."""
        frame = tk.Frame(parent, bg=theme.BORDER, bd=1)
        frame.pack(fill="both", expand=True)
        scroll = ttk.Scrollbar(frame)
        scroll.pack(side="right", fill="y")
        box = tk.Text(frame, wrap="word", width=10, font=theme.FONT_NORMAL, bg=background,
                      relief="flat", padx=8, pady=6, yscrollcommand=scroll.set,
                      state="disabled", cursor="arrow")
        box.pack(side="left", fill="both", expand=True)
        scroll.config(command=box.yview)

        # tags = named text styles, used like: insert(text, "clue")
        box.tag_config("heading", font=theme.FONT_BOLD, foreground=theme.TEXT_HEADING)
        box.tag_config("clue", foreground=theme.TEXT_CLUE)
        box.tag_config("good", foreground=theme.TEXT_CLUE, font=theme.FONT_BOLD)
        box.tag_config("speech", foreground=theme.TEXT_SPEECH)
        box.tag_config("bad", foreground=theme.TEXT_BAD, font=theme.FONT_BOLD)
        box.tag_config("info", foreground=theme.TEXT_INFO)
        return box

    def build_case_buttons(self):
        """Make the place and suspect buttons for the current case."""
        for frame in (self.places_frame, self.suspects_frame):
            for widget in frame.winfo_children():
                widget.destroy()
        self.action_buttons = []

        case = self.game.case
        for key, name in case["locations"].items():
            button = ColorButton(self.places_frame, name, lambda k=key: self.on_search(k),
                                 theme.BLUE, theme.BLUE_HOVER, width=24)
            button.pack(fill="x", pady=2)
            self.action_buttons.append(button)

        for key, suspect in case["suspects"].items():
            text = suspect["name"] + " (" + suspect["role"] + ")"
            button = ColorButton(self.suspects_frame, text, lambda k=key: self.on_question(k),
                                 theme.ORANGE, theme.ORANGE_HOVER, width=24)
            button.pack(fill="x", pady=2)
            self.action_buttons.append(button)

    # ------------------------------------------------------------------
    # showing text
    # ------------------------------------------------------------------
    def log(self, messages):
        """Add messages (tag, text) to the investigation log."""
        box = self.log_text
        box.config(state="normal")
        for tag, text in messages:
            if tag == "heading" and box.index("end-1c") != "1.0":
                box.insert("end", "\n")          # empty line before a new heading
            box.insert("end", text + "\n", tag)
        box.config(state="disabled")
        box.see("end")

    def clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")

    def refresh(self):
        """Update the status bar, the notebook and the buttons."""
        game = self.game
        self.score_label.config(text=str(game.score))
        self.actions_label.config(text=str(game.actions_left))
        self.clues_label.config(text=str(len(game.found_clues)) + " / " + str(game.total_clues))
        self.hints_label.config(text=str(game.hints_left))
        self.level_label.config(text=game.level_name, fg=theme.LEVEL_COLORS[game.level_name])

        self.note_text.config(state="normal")
        self.note_text.delete("1.0", "end")
        if len(game.notebook) == 0:
            self.note_text.insert("end", "Nothing yet. Start investigating!", "info")
        for kind, text in game.notebook:
            if kind == "clue":
                self.note_text.insert("end", "Clue: " + text + "\n\n", "clue")
            else:
                self.note_text.insert("end", text + "\n\n", "speech")
        self.note_text.config(state="disabled")
        self.note_text.see("end")

        # turn the buttons on or off
        for button in self.action_buttons:
            if game.over:
                button.disable()
            else:
                button.enable()
        if game.over:
            self.accuse_button.disable()
        else:
            self.accuse_button.enable()
        if game.over or game.hints_left <= 0:
            self.hint_button.disable()
        else:
            self.hint_button.enable()
        self.hint_button.config(text="Get Hint (" + str(game.hints_left) + " left)")

    def update_level_info(self):
        self.level_info.config(text=DIFFICULTY[self.level_var.get()]["description"])

    # ------------------------------------------------------------------
    # starting a game
    # ------------------------------------------------------------------
    def new_game(self, ask=True):
        if ask and self.game is not None and not self.game.over:
            if not messagebox.askyesno("New game", "A game is running. Start a new game?"):
                return

        case_key = self.case_keys[self.case_box.current()]
        self.game = Game(case_key, self.level_var.get())
        case = self.game.case

        self.build_case_buttons()
        self.clear_log()
        messages = [("heading", case["title"]), ("plain", case["story"]), ("heading", "Suspects")]
        for suspect in case["suspects"].values():
            messages.append(("info", "- " + suspect["name"] + " (" + suspect["role"] + "): "
                             + suspect["intro"]))
        messages.append(("info", "Choose a place to search or a suspect to question."))
        self.log(messages)
        self.refresh()

    # ------------------------------------------------------------------
    # button actions
    # ------------------------------------------------------------------
    def on_search(self, place):
        self.after_move(self.game.search(place))

    def on_question(self, suspect_key):
        self.after_move(self.game.question(suspect_key))

    def on_hint(self):
        self.log(self.game.use_hint())
        self.refresh()

    def after_move(self, messages):
        """Show the result of a move and check if the player is out of actions."""
        self.log(messages)
        self.refresh()
        if self.game.time_is_up:
            messagebox.showinfo("Out of actions", "You have no actions left.\n"
                                                  "You must name the culprit now.")
            self.on_accuse(forced=True)

    # ------------------------------------------------------------------
    # accusation and final questions
    # ------------------------------------------------------------------
    def on_accuse(self, forced=False):
        if self.game is None or self.game.over:
            return
        suspect_key = dialogs.ask_accusation(self.root, self.game.case["suspects"], forced)
        if suspect_key is not None:
            self.resolve_accusation(suspect_key)

    def resolve_accusation(self, suspect_key):
        game = self.game
        self.log(game.accuse(suspect_key))

        if not game.over:                       # the right culprit: ask the final questions
            total = len(game.questions)
            for number, question in enumerate(game.questions, start=1):
                chosen = dialogs.ask_question(self.root, number, total, question)
                self.log(game.check_answer(number, question, chosen))
            self.log(game.finish())
        self.finish_game()

    def finish_game(self):
        game = self.game
        self.refresh()
        lines = game.summary_lines()
        self.log([("heading", "CASE CLOSED")] + [("info", line) for line in lines])
        messagebox.showinfo("Case closed", "\n".join(lines))

        if game.accused_right:
            name = simpledialog.askstring("High score", "Enter your name to save your score:",
                                          parent=self.root)
            if name is not None and name.strip() != "":
                saved = highscores.save_score(name.strip()[:20], game.score,
                                              game.case["title"], game.level_name)
                if saved:
                    self.log([("info", "Your score was saved in the high score list.")])

    # ------------------------------------------------------------------
    # menu windows
    # ------------------------------------------------------------------
    def show_high_scores(self):
        dialogs.show_high_scores(self.root, highscores.load_scores())

    def show_how_to_play(self):
        messagebox.showinfo("How to play", HOW_TO_PLAY)

    def show_about(self):
        messagebox.showinfo("About MysteryBox",
                            "MysteryBox - Detective Game\n"
                            "Version 1.0\n\n"
                            "A Python mini project made with tkinter.")

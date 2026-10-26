"""
main.py - MysteryBox, a detective game made with Python and tkinter

How to run (in VS Code):
    open this folder in VS Code, open main.py and press the Run button
    (or type  python main.py  in the VS Code terminal)

Project structure:
    main.py          starts the game (this file)
    data/            the cases and the difficulty levels
    logic/           the rules of the game and the high score file
    gui/             the window, the pop-ups and the colours
"""

import tkinter as tk

from gui.app import MysteryBoxApp


def main():
    root = tk.Tk()
    MysteryBoxApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

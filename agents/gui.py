from .player import KobayakawaPlayer
from tkinter import simpledialog
import engine.actions as actions


class KobayakawaTkAgent(KobayakawaPlayer):
    def __init__(self, game, view, ctrl):
        # ask for player name
        player_name = simpledialog.askstring("Input", "Enter your name", parent=view)
        super().__init__(game, player_name)

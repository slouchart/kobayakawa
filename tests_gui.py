from tkinter import Tk
from graphics.controller import Controller
from graphics.view import MainWindow
from engine import *
from agents import KobayakawaTkAgent, KobayakawaHeuristicAgent


class GameEngineFactory(GameEngine):
    player_agent = KobayakawaTkAgent
    opponent_agent = KobayakawaHeuristicAgent


root = Tk()
root.title("Kobayakawa")
game = GameEngineFactory()
app = MainWindow(master=root)
controller = Controller(game, app)

controller.enable()


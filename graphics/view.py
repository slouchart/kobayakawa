from tkinter import *
from tkinter.font import Font


class MainWindow(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.main_font = Font(family="Helvetica", size=14)
        self.interior = None
        self.initialize()

    def initialize(self):
        self.interior = Frame(width=800, height=600, bd=2, relief=SUNKEN, bg='green')
        self.interior.pack(padx=2, pady=2, fill=BOTH, expand=True)
        self.interior.pack_propagate(False)

__author__ = 'tom, stef, pieter'

import Tkinter as tk

"""
The super file which is above and beyond everything happening visually.
Of course a multi-line comment is only justified if it contains multiple lines.
"""


class GUI(tk.Frame):
    # Class for graphical shizzle.
    # It is initialized by a master call and updated every cycle.

    # Initialize grid and such
    def __init__(self, master=None):
        print("Init GUI...")
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

        # self.top = Tkinter.Tk()
        # # Code to add widgets will go here...
        # self.top.mainloop()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid()

    # An update for every cycle?
    def update(self):
        print("Updating grid...")

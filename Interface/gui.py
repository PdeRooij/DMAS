__author__ = 'tom, stef, pieter'

import Tkinter  # Should we want to use Tkinter, here is a template

"""
The super file which is above and beyond everything happening visually.
Of course a multi-line comment is only justified if it contains multiple lines.
"""

class GUI:

    # Class for graphical shizzle.
    # It is initialized by a master call and updated every cycle.

    # Initialize grid and such
    def __init__(self):
        self.top = Tkinter.Tk()
        # Code to add widgets will go here...
        self.top.mainloop()

    # An update for every cycle?
    def update(self):
        pass

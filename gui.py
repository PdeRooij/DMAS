__author__ = 'tom, stef, pieter'

from kivy.app import App

"""
The super file which is above and beyond everything happening visually.
Of course a multi-line comment is only justified if it contains multiple lines.
"""


class GUIApp(App):
    # Class for graphical shizzle.
    # It is initialized by a master call and updated every cycle.

    # Initialize grid and such
    def build(self):
        self.title = "Traffic simulator"

    def update(self):
        pass

if __name__ == '__main__':
    GUIApp().run()
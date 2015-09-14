__author__ = 'tom, stef, pieter'

from Queue import Queue

# Class representing a crossing in the model.
# It contains the location in the grid and queues for every direction.


class Crossing:

    # Generate empty crossing
    def __init__(self):
        self.north = Queue()
        self.east = Queue()
        self.south = Queue()
        self.west = Queue()

    # Take next in queues, generate traffic situation
    def resolve(self):
        pass
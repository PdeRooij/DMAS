__author__ = 'tom, stef, pieter'

from directions import Directions
from Queue import Queue

# Class representing a crossing in the model.
# It contains the location in the grid and queues for every direction.


class Crossing:

    # Generate empty crossing
    def __init__(self):
        self.dr = Directions()  # Store a directions instance

        # Make dictionary of roads from every direction
        self.roads = {}.fromkeys(self.dr.directions, Queue())
        # Also a hold for if a driver decided to wait
        self.hold = {}.fromkeys(self.dr.directions)

    # Take next in queues, generate traffic situation
    def resolve(self):
        pass
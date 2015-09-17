__author__ = 'tom, stef, pieter'

from directions import Directions

# A situation generated as two or more drivers encounter each other.


class Situation:

    # Generate situation from traffic supplied by a crossing
    def __init__(self, **kwargs):
        self.directions = Directions()
        self.traffic = {}    # Dictionary of drivers from a certain direction
        for arg in kwargs:
            self.traffic[arg] = kwargs[arg]

    # Distribute current situation to involved drivers from their viewpoint
    def distribute(self):
        # Consider every direction
        for direction, driver in self.traffic.iteritems():
            # TODO implement providing driver's view
            pass

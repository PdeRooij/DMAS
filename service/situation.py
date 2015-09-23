from directions import Directions

__author__ = 'tom, stef, pieter'

# A situation generated as two or more drivers encounter each other.


class Situation:

    # Generate situation from traffic supplied by a crossing
    def __init__(self, traffic):
        self.directions = Directions()
        self.traffic = traffic  # Dictionary of drivers from a certain direction

    # Distribute current situation to involved drivers from their viewpoint
    def distribute(self):
        # Initialize list of chosen actions of drivers, tuple (direction, driver, action)
        actions = []
        # Consider every direction
        for direction, driver in self.traffic.iteritems():
            # Driver's view is simply a 3-item list, representing a driver from [left, ahead, right]
            # I am going to apply some enumeration magic here, please ask if unclear. :)
            if driver:
                # There is a driver from this direction, generate her view
                view = [None, None, None]

                ## Consider drivers from every other direction
                # First get 'other' directions
                other_dr = list(self.directions[self.directions[direction]:len(self.directions)]) +\
                        list(self.directions[0:self.directions[direction]])
                # NOTE: Composition is important here! Slicing required for [left, ahead, right]
                # Loop over those directions, idx corresponds with view
                for idx, dr in enumerate(other_dr):
                    if self.traffic[dr]:
                        # There is a driver from that direction, mark as present in view
                        view[idx] = 1

                # Let the driver decide on situation and store action (direction, action)
                actions.append((direction, driver.decide(view)))

        return actions

    # Computes outcome and rewards for involved drivers
    def compute_outcome(self, actions, rewards):
        # Consider all decisions
        for direction, action in actions:
            if action == 'wait':
                self.traffic[direction].remember(rewards['wait'])

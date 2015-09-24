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
        # Initialize list of chosen actions of drivers, tuple (direction, action)
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
            elif action == 'go':
                # Check if there is a driver from the right or the left
                dr_left = self.directions[direction]+1
                dr_right = self.directions[direction]-1
                collision = False   # Flag whether there was a collision
                # TODO this is not yet safe for drivers from all directions!!
                if self.traffic[dr_left]:
                    # There is a driver to the left
                    if actions[dr_left] == 'go':
                        # This driver chose to go as well, there is a collision
                        collision = True
                        # Give corresponding reward and remove from actions list
                        self.traffic[dr_left].remember(rewards['crash'])
                if collision:
                    # There was a collision, give this driver corresponding reward
                    self.traffic[direction].remember(rewards['crash'])
                else:
                    # No crash, good to go!
                    self.traffic[direction].remember(rewards['clear'])


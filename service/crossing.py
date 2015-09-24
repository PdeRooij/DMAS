from Queue import Queue
from directions import Directions
from situation import Situation

__author__ = 'tom, stef, pieter'

# Class representing a crossing in the model.
# It contains the location in the grid and queues for every direction.


class Crossing:

    # Generate empty crossing
    def __init__(self, location):
        self.loc = location     # [x, y]
        self.dr = Directions()  # Store a directions instance

        # Make dictionary of roads from every direction
        self.roads = {}.fromkeys(self.dr.directions, Queue())
        # Also a hold for if a driver decided to wait
        self.hold = {}.fromkeys(self.dr.directions)
        # And finally a slot for end-points of an animation
        self.next = {}.fromkeys(self.dr.directions)
        self.next['crash'] = None   # Also add a point in the middle indicating crash

    # Take next in queues, generate traffic situation
    def resolve(self):
        # First take the drivers already on hold
        traffic = self.hold
        gen = False     # Only make a situation if there is traffic (hopefully reducing overhead)

        # Check whether there are drivers queued
        for direction, q in self.roads.iteritems():
            # Only dequeue a driver if there wasn't already one on hold and there is a queue
            if not traffic[direction] and not q.empty():
                gen = True  # Creating a situation is justified
                # There is a driver queued here, add to situation
                traffic[direction] = q.get()

        # Initialize a situation if there is traffic and give that back
        if gen:
            return Situation(traffic)

    # Move drivers to next location in crossing
    def move_drivers(self, traffic, collision=False):
        # Check if there was a crash, if so, collision will contain involved drivers
        if collision:
            # There is a collision, put involved drivers in crash location
            self.next['crash'] = collision
        # Move drivers to the opposite side
        for direction, driver in traffic.iteritems():
            if driver:
                # There is a driver, move him to the next in the opposite direction
                self.next[self.dr[self.dr[direction]-2]] = driver

    # Returns the drivers that have to be moved elsewhere
    def translate_drivers(self):
        # Put all drivers that have to be moved in to_move
        to_move = self.next
        # Make a list of all transitions
        pieter_4_life = []
        for direction, driver in to_move.iteritems():
            if direction == 'crash':
                # Forget about this, because it is handled by the model
                pass
                for d in driver:
                    # TODO move this in a higher hierarchy
                    d.respawn()
            else:
                # Move this driver to next crossing
                next_cr = self.loc
                if direction == 'North':
                    # Increases y by 1
                    next_cr[1] += 1
                elif direction == 'East':
                    # Increase x by 1
                    next_cr[0] += 1
                elif direction == 'South':
                    # Decrease y by 1
                    next_cr[1] -= 1
                elif direction == 'West':
                    # Decrease x by 1
                    next_cr[0] -= 1
                next_dr = self.dr[self.dr[direction]-2]     # Compute opposite direction (queue it will move into)
                pieter_4_life.append((driver, next_cr, next_dr))

        return pieter_4_life
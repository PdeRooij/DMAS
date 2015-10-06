from Queue import Queue
from random import Random
from copy import deepcopy
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
        # Note to self: fromkeys with Queue() is nice, but only makes one queue....
        self.roads = {}.fromkeys(self.dr.directions)
        for road in self.roads:
            self.roads[road] = Queue()
        # Also a hold for if a driver decided to wait
        self.hold = {}.fromkeys(self.dr.directions)
        # And finally a slot for end-points of an animation
        self.next = {}.fromkeys(self.dr.directions)
        self.next['crash'] = None   # Also add a point in the middle indicating crash

    # Take next in queues, generate traffic situation
    def resolve(self):
        gen = False     # Only make a situation if there is traffic (hopefully reducing overhead)
        # First take the drivers already on hold
        traffic = self.hold

        # Check whether there are drivers queued
        for direction, q in self.roads.iteritems():
            if traffic[direction]:
                # There was a driver in the hold, so do generate a situation
                gen = True
            # Only dequeue a driver if there wasn't already one on hold and there is a queue
            elif not q.empty():
                gen = True  # Creating a situation is justified
                # There is a driver queued here, add to situation
                traffic[direction] = q.get()

        # Initialize a situation if there is traffic and give that back
        if gen:
            return Situation(traffic)

    # Move drivers to next location in crossing
    def move_drivers(self, situation, collision=False):
        # Check if there was a crash, if so, collision will contain involved drivers
        if collision:
            # There is a collision, put involved drivers in crash location
            self.next['crash'] = collision

        move = situation.move    # Get drivers to be moved
        # Move drivers to the opposite side
        for direction, driver in move.iteritems():
            if driver:
                # There is a driver, move him to the next in the opposite direction
                self.next[self.dr[self.dr[direction]-2]] = driver

    # Returns the drivers that have to be moved elsewhere
    def translate_drivers(self):
        # Make a list of all transitions and a crashed list
        pieter_4_life = []
        crashed = []
        for direction, driver in self.next.iteritems():
            if driver:
                # There are actually people here...
                if direction == 'crash':
                    # Just return the crashed drivers on this spot
                    crashed = driver    # This is then actually a list of crashed drivers
                else:
                    # Move this driver to next crossing
                    next_cr = deepcopy(self.loc)
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

        # Empty next slots and return a list of transitions
        self.next = {}.fromkeys(self.dr.directions)
        self.next['crash'] = None
        return pieter_4_life, crashed

    # Puts a driver coming from another crossing in the right queue
    def enqueue(self, driver, direction):
        self.roads[direction].put(driver)
        driver.status = 'queued'

    # Spawns a driver at the edge of the grid.
    def put_spawn(self, driver, edge_x, edge_y):
        edge = []   # List of directions that are on an edge

        # Calculate which direction is the edge
        if not self.loc[0]:
            # X is zero, so crossing is at the left edge of the grid
            edge.append('West')
        if not self.loc[1]:
            # Y is zero, so crossing is at the top edge of the grid
            edge.append('North')
        if self.loc[0] == edge_x:
            # X equals maximal x, so crossing is at the right edge of the grid
            edge.append('East')
        if self.loc[1] == edge_y:
            # Y equals maximal y, so crossing is at the bottom edge of the grid
            edge.append('South')

        # Enqueue the driver at (one of) the edge(s)
        if len(edge) > 1 and Random().randint(0, 1):
            # If the crossing is at a corner, randomly assign to one of the edges
            self.enqueue(driver, edge[1])
        else:
            self.enqueue(driver, edge[0])

    # Generates a list of occupied spots for the GUI
    def occupied(self):
        occ = [0, 0, 0, 0, 0]   # Initialize list as if the crossing is entirely free

        # Check whether queues are filled
        for idx, dr in enumerate(self.dr[0::]):
            occ[idx] = self.roads[dr].qsize()   # Just put the length of the queue in the list

        # Check if there is a crash, if so, set last element of occ to the number of crashed drivers
        if self.next['crash']:
            occ[4] = len(self.next['crash'])

        # Return list of occupancies
        return occ

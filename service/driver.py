__author__ = 'tom, stef, pieter'

from memory import Memory

# Class simulating a driver.
# Each driver has a (unique) ID, a history (memory)


class Driver:

    # Spawn driver with specified id and empty memory
    def __init__(self, id='unknown'):
        self.id = id
        self.mem = Memory()

    # Decide what to do in given situation
    def decide(self, situation):
        return 'go'
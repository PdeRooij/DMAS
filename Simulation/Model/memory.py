__author__ = 'tom, stef, pieter'

from Queue import Queue

"""
Everything related to memory is included in this file.
Both a queue representing an agent's memory as well as chunks are implemented here.
"""

# Class for memories
class Memory:

    # Make a new, empty memory queue of (standard) length 10.
    def __init__(self, length=10):
        self.mem = Queue()
        self.length = length
        self.items = 0

    # Compare current condition (chunk?) to similar events
    def match(self, chunk):
        if self.items == 0:
            return


# Represents one specific memory
class Chunk:

    # Something here to store relevant information of an event
    def __init__(self):
        pass
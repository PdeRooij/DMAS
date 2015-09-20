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

    # Compare current condition (chunk?) to similar events
    def match(self, chunk):
        if self.mem:
            # There are past memories
            same = []  # List for similar memories
            # Consider all memories
            for m in self.mem.queue:
                if m.equals(chunk):
                    # Similar situation found, add to list
                    same.append(m)
            # Return list of similar events
            return same
        else:
            # No experiences yet, so no matches.
            return []


# Represents one specific memory
class Chunk:
    # Something here to store relevant information of an event
    def __init__(self, traffic, act, r):
        self.traffic = traffic  # Situation characterized by drivers from left, ahead or right
        self.action = act       # Chosen action
        self.reward = r         # Reward received after taking action in this situation

    # A chunk equals another if the situation is similar
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.traffic == other.traffic)

    # Specify when memories are not similar, which obviously is te inverse of the above
    def __ne__(self, other):
        return not self == other
__author__ = 'tom, stef, pieter'

"""
Everything related to memory is included in this file.
Both a queue representing an agent's memory as well as chunks are implemented here.
"""


# Class for memories
class Memory:
    # Make a new, empty memory of (standard) length 10.
    def __init__(self, length=10):
        # Memory is a stack (list in Python)
        self.mem = []
        self.length = length

    # Makes a new chunk and stores it in memory
    def store(self, traffic, act, r):
        print "STORE CHUNK IN MEMORY\n"
        self.mem.append(Chunk(traffic, act, r))

    # Compare current condition (chunk?) to similar events
    def match(self, chunk):
        if self.mem:
            # There are past memories
            same = []  # List for similar memories
            # Consider all memories
            for m in self.mem:
                if m == chunk:
                    # Similar situation found, add to list
                    same.append(m)
            # Return list of similar events
            return same
        else:
            # No experiences yet, so no matches.
            return []

    # This method gets the latest unique situations and returns those
    def last_act(self):
        # Make lists of unique situations and latest memory of it
        uniq_sit = []
        actions = []

        # Loop over memories in reverse order (recency) and get latest unique situations
        for m in reversed(self.mem):
            if not uniq_sit.__contains__(m.traffic):
                # New unique situation encountered, add to lists
                uniq_sit.append(m.traffic)
                actions.append(m)

        # Return latest action for every unique situation
        return actions

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
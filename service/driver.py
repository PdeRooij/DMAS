__author__ = 'tom, stef, pieter'

from memory import Memory
from random import Random

# Class simulating a driver.
# Each driver has a (unique) ID, a history (memory)


class Driver:

    # Spawn driver with specified id and empty memory
    def __init__(self, name='unknown'):
        self.id = name
        self.mem = Memory()
        self.spawn = [0, 0]     # Where the driver spawns
        self.goal = [0, 0]      # Where the driver is headed to
        self.status = 'spawning'    # Status (driving, queued, etc.)

    # Decide what to do in given situation
    def decide(self, situation):
        rand = Random()
        matches = self.mem.match(situation)     # List of matching situations in memory
        if matches:
            # At least one matching situation is found. Take best action from experience.
            return 'go'
        else:
            # No matching situations, randomly select action
            act = rand.randint(0, 1)
            if act == 0:
                return 'wait'
            else:
                return 'go'

    # Compute utilities of actions based on similar past situations
    def compute_utility(self, memories):
        util = {'go': 0, 'wait': 0}     # Dictionary with utilities of each action, start at 0
        # Consider every memory
        for m in memories:
            # Add the outcome of a memory to the action taken
            util[m.action] += m.reward
        # Return the utilities of each action
        return util
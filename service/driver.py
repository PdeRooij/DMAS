from memory import Memory
from random import Random

__author__ = 'tom, stef, pieter'

# Class simulating a driver.
# Each driver has a (unique) ID, a history (memory)


class Driver:

    # Spawn driver with specified id and empty memory
    def __init__(self, name='unknown'):
        self.id = name
        self.mem = Memory()
        # Working memory
        self.view = None        # Last view of situation
        self.act = None         # Last chosen action
        self.spawn = [0, 0]     # Where the driver spawns
        self.goal = [0, 0]      # Where the driver is headed to
        self.heading = [0, 1, 0]    # Heading at the moment (always ahead as of yet)
        self.status = 'spawning'    # Status (driving, queued, etc.)
        self.log = {'crash' : 0,    # Driver's log containing stats
                    'go' : 0,
                    'wait' : 0,
                    'last_action' : 'none'
                    }

    # Decide what to do in given situation
    def decide(self, traffic):
        # A check because the remember approach might be prone to error
        if self.view:
            print 'WARNING!! Apparently took an action without getting a reward!'

        self.view = traffic     # Store view in working memory
        rand = Random()
        matches = self.mem.match(traffic)     # List of matching situations in memory
        if matches:
            # print ("IS IN MATCH\n")
            # At least one matching situation is found. Take best action from experience.
            utils = self.compute_utility(matches)
            self.act = ['go', 'wait'][rand.randint(0, 1)]   # Select random action
            high = -1000000
            for act, util in utils.iteritems():
                diff = util - high
                if diff > 0 and rand.randint(0, diff) > diff / 20:
                    # Check utility is the highest and if the difference is large enough,
                    # random noise added
                    self.act = act
                    high = util
        else:
            # print ("NO MATCH\n")
            # No matching situation or , randomly select action
            act = rand.randint(0, 1)
            if act == 0:
                self.act = 'wait'   # Also store in WM
                self.status = 'waiting'
            else:
                self.act = 'go'
                self.status = 'driving'

        # Add action to the log
        self.log['last_action'] = self.act
        self.log[self.act] += 1
        # Finally return the decision
        return self.act

    # Combines current memory with given reward
    def remember(self, reward):
        # Again a check because this method might be prone to error
        if not (self.view and self.act):
            print 'WARNING!! This driver forgot what to remember!'
        self.mem.store(self.view, self.act, reward)
        self.view = self.act = None     # Clear WM

    # Compute utilities of actions based on similar past situations
    @staticmethod
    def compute_utility(memories):
        util = {'go': 0, 'wait': 0}     # Dictionary with utilities of each action, start at 0
        occ = {'go': 0, 'wait': 0}      # Dictionary with occurrences of each action

        # Consider every memory
        for m in memories:
            # Add the outcome of a memory to the action taken
            util[m.action] += m.reward
            occ[m.action] += 1  # Increment times this action is chosen

        # Normalize utilities
        for act, n in occ.iteritems():
            # Divide utility of this action by number of times it was chosen
            if n > 0:
                # Only do division if there is a positive integer here
                util[act] /= n

        # Return the normalized utilities of each action
        return util

    # Initiates a respawn cycle. Takes dimensions of grid (x,y) and returns spawn point.
    # TODO uncomment if we want to spawn not only at bottom and right
    def respawn(self, x, y):
        # Signify spawning at an edge of the grid
        self.status = 'spawning'
        rand = Random()

        # 50/50 chance of differing in x or y
        if rand.randint(0, 1):
            # Differing in y
            spawn_y = goal_y = rand.randint(0, y-1)
            # Spawn left or right
            # if rand.randint(0, 1):
            #     spawn_x = 0
            #     goal_x = x-1
            # else:
            spawn_x = x-1
            goal_x = 0
        else:
            # Differing in x
            spawn_x = goal_x = rand.randint(0, x-1)
            # Spawn top or bottom
            # if rand.randint(0, 1):
            #     spawn_y = 0
            #     goal_y = y-1
            # else:
            spawn_y = y-1
            goal_y = 0

        # Compose new spawn point
        self.spawn = [spawn_x, spawn_y]
        # Also compose the new goal destination, currently opposite side.
        self.goal = [goal_x, goal_y]

        return self.spawn

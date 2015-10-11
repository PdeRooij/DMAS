__author__ = 'tom, stef, pieter'

class Statistics:

    def __init__(self):
        self.drivers = []
        # [left_go, right_go, left_wait, right_wait, go_ratio, wait_ratio]
        self.stats = [0, 0, 0 ,0, 0, 0]


    def update(self, driver_list):
        # Copy list of drivers
        self.drivers = driver_list
        # Reset values
        self.stats = [1, 1, 1 ,1, 1, 1]
        # Iterate over list of drivers and do statistics
        for driver in self.drivers:
            # Check if driver gave way to the left or did not
            # Check if view == [1, 0, 0]
            if driver.view[0] == 1 and driver.view[2] == 0 and driver.act == 'go':
                self.stats[0] += 1
            elif driver.view[0] == 1 and driver.view[2] == 0 and driver.act == 'wait':
                self.stats[2] += 1
            # Check if driver gave way to the right or did not
            # Check if view == [0, 0, 1]
            elif driver.view[0] == 0 and driver.view[2] == 1 and driver.act == 'go':
                self.stats[1] += 1
            elif driver.view[0] == 1 and driver.view[2] == 0 and driver.act == 'wait':
                self.stats[3] += 1

        # Calculate ratio of agent going
        self.stats[4] = self.stats[0] / float(self.stats[0] + self.stats[1])
        # Calculate ratio of agent waiting
        self.stats[5] = self.stats[2] / float(self.stats[2] + self.stats[3])

        # Return list of statistics
        return self.stats


    #def write_to_log(self, stats_list):



""" to log:

number of agents in the grid

For each crossing:
current movement of agent
total number of agents present


For each grid point:
number of agents in queue
number of agents crossed
number of agents waited


"""







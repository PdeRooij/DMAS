__author__ = 'tom, stef, pieter'

class Statistics:

    def __init__(self):
        self.drivers = []
        # [left_go, right_go, left_wait, right_wait, left_go_ratio, right_go_ratio
        # left_wait_ratio, right_wait_ratio]
        self.stats = [0] * 8


    def update(self, driver_list):
        # Copy list of drivers
        self.drivers = driver_list
        # Reset values to 0 TODO change to 0 when debugged
        self.stats = [1] * 8
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

        # Calculate ratio of agents going when agent coming from the left
        self.stats[4] = self.stats[0] / float(self.stats[0] + self.stats[1])

         # Calculate ratio of agents going when agent coming from the right
        self.stats[5] = self.stats[1] / float(self.stats[0] + self.stats[1])

        # Calculate ratio of agents waiting when agent coming from the left
        self.stats[6] = self.stats[2] / float(self.stats[2] + self.stats[3])

        # Calculate ratio of agents waiting when agent coming from the right
        self.stats[7] = self.stats[3] / float(self.stats[2] + self.stats[3])

        # Return list of statistics
        # TODO remove this line
        self.stats = [1] * 8
        return self.stats



    def write_to_log(self, stats_list):

        log_file = open("simlog.txt", "w")
        log_file.write(stats_list, sep='\t'))
        log_file.close()












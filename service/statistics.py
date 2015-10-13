__author__ = 'tom, stef, pieter'

class Statistics:

    def __init__(self, driver_list):
        self.drivers = driver_list
        self.stats = {
            'left_go': 0,
            'right_go': 0,
            'left_wait': 0,
            'right_wait': 0,
            'go_ratio': 0,
            'wait_ratio': 0
        }

    def update(self):
        # Reset values
        for key in self.stats:
            self.stats[key] = 0

        # Iterate over list of drivers and do statistics
        for driver in self.drivers:
            # TODO this has to change: utilize memory instead of working memory
            # Check if driver gave way to the left or did not
            if driver.view == [1, 0, 0]:
                # Situation in which there was a driver from the left
                if driver.act == 'go':
                    self.stats[0] += 1
                elif driver.act == 'wait':
                    self.stats[2] += 1

            # Check if driver gave way to the right or did not
            elif driver.view == [0, 0,  1]:
                # Situation in which there was a driver from the right
                if driver.act == 'go':
                    self.stats[1] += 1
                elif driver.act == 'wait':
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












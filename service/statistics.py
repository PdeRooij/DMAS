__author__ = 'tom, stef, pieter'


class Statistics:

    def __init__(self):
        self.stats = {
            'left_go': 0,
            'right_go': 0,
            'left_wait': 0,
            'right_wait': 0,
            'go_ratio': 0,
            'wait_ratio': 0,
            'left_go_ratio' : 0,
            'right_go_ratio' : 0,
            'left_wait_ratio' : 0,
            'right_wait_ratio' : 0
        }
        self.csv_file = ''

    def driver_update(self, driver_list):
        self.drivers = driver_list

    def update(self):
        # Reset values
        for key in self.stats:
            self.stats[key] = 0

        # Iterate over list of drivers and do statistics
        print self.drivers
        for driver in self.drivers:
            # Check if driver gave way to the left or did not
            print ("\n")
            print(driver.mem.queue)
            print driver.mem.queue[-1].traffic
            print ("PRINTED LINE?\n")
            if driver.mem.mem[-1].traffic == [1, 0, 0]:
                # Situation in which there was a driver from the left
                if driver.act == 'go':
                    self.stats['left_go'] += 1
                elif driver.act == 'wait':
                    self.stats['left_wait'] += 1

            # Check if driver gave way to the right or did not
            elif driver.mem.mem[-1].traffic == [0, 0,  1]:
                # Situation in which there was a driver from the right
                if driver.act == 'go':
                    self.stats['right_go'] += 1
                elif driver.act == 'wait':
                    self.stats['right_wait'] += 1

        print ("I PASSED FOR LOOP\n")

        if self.stats['left_go'] and self.stats['right_go']:
            # Calculate ratio of agents going when agent coming from the left
            self.stats['left_go_ratio'] = self.stats['left_go'] / float(self.stats['left_go'] + self.stats['right_go'])

             # Calculate ratio of agents going when agent coming from the right
            self.stats['right_go_ratio'] = self.stats['right_go'] / float(self.stats['left_go'] + self.stats['right_go'])

        if self.stats['left_wait'] and self.stats['right_wait']:
            # Calculate ratio of agents waiting when agent coming from the left
            self.stats['left_wait_ratio'] = self.stats['left_wait'] / float(self.stats['left_wait'] + self.stats['right_wait'])

            # Calculate ratio of agents waiting when agent coming from the right
            self.stats['right_wait_ratio'] = self.stats['right_wait'] / float(self.stats['left_wait'] + self.stats['right_wait'])

        print("\n")
        print ("STATS!!!!!!\n")
        print self.stats
        # Return dict of statistics
        return self.stats

    def create_csv(self):
        pass

    def write_to_log(self):
        pass












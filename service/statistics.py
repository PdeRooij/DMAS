__author__ = 'tom, stef, pieter'

from os import makedirs, getcwd
from os.path import join, isdir, isfile
from glob import glob
import csv

class Statistics:

    def __init__(self):
        self.drivers = []
        self.stats = {
            'left_go': 0.0,
            'right_go': 0.0,
            'left_wait': 0.0,
            'right_wait': 0.0,
            'go_ratio': 0.0,
            'wait_ratio': 0.0,
            'left_go_ratio': 0.0,
            'right_go_ratio': 0.0,
            'left_wait_ratio': 0.0,
            'right_wait_ratio': 0.0
        }
        self.csv_file = ''
        self.csv_exist = True

    def driver_update(self, driver_list):
        self.drivers = driver_list

    def update(self):
        # Reset values
        for key in self.stats:
            self.stats[key] = 0.0

        # Iterate over list of drivers and do statistics
        #print self.drivers
        for driver in self.drivers:
            # Check if driver gave way to the left or did not
            # print ("\n")
            # print(driver.mem.queue)
            # print driver.mem.queue[-1].traffic
            # print ("PRINTED LINE?\n")
            uniq_mem = driver.mem.last_act()
            for m in uniq_mem:
                if m.traffic == [1, None, None]:
                    # Situation in which there was a driver from the left
                    if m.action == 'go':
                        self.stats['left_go'] += 1
                    elif m.action == 'wait':
                        self.stats['left_wait'] += 1

                # Check if driver gave way to the right or did not
                elif m.traffic == [None, None,  1]:
                    # Situation in which there was a driver from the right
                    if m.action == 'go':
                        self.stats['right_go'] += 1
                    elif m.action == 'wait':
                        self.stats['right_wait'] += 1

        #print ("I PASSED FOR LOOP\n")

        if self.stats['left_go'] or self.stats['right_go']:
            # Calculate ratio of agents going when agent coming from the left
            self.stats['left_go_ratio'] = self.stats['left_go'] / (self.stats['left_go'] + self.stats['right_go'])

             # Calculate ratio of agents going when agent coming from the right
            self.stats['right_go_ratio'] = self.stats['right_go'] / (self.stats['left_go'] + self.stats['right_go'])

        if self.stats['left_wait'] or self.stats['right_wait']:
            # Calculate ratio of agents waiting when agent coming from the left
            self.stats['left_wait_ratio'] = self.stats['left_wait'] / (self.stats['left_wait'] + self.stats['right_wait'])

            # Calculate ratio of agents waiting when agent coming from the right
            self.stats['right_wait_ratio'] = self.stats['right_wait'] / (self.stats['left_wait'] + self.stats['right_wait'])

        # print("\n")
        # print ("STATS!!!!!!\n")
        # print self.stats
        # Return dict of statistics
        return self.stats

    # Get filename of not yet existing .csv name
    def create_csv(self, p):
        # p = Parameters from parameters.py
        r = p['reward']

        if not isdir('statistics'):
            makedirs('statistics')

        # n_driver, clear, crash, wait, destination, gridx x gridy
        self.csv_file = 'n{}_cl{}_cr{}_w{}_d{}_{}x{}_00000.csv'.format(
            p['n_drivers'], r['clear'], r['crash'], r['wait'], r['destination'],
            p['grid_size'][0], p['grid_size'][1]
        )

        # Get latest number of existing .csv files
        max = -1
        #print(getcwd())
        #print(self.csv_file[:-9])
        for file in glob(join('statistics', self.csv_file[:-9]+'*')):  # join('statistics', self.csv_file[:-9])
            #print(file)
            #print(int(file[-9:-4]))
            if int(file[-9:-4]) > max:
                max = int(file[-9:-4])

        max += 1
        max = str(max).zfill(5)
        self.csv_file = join('statistics', self.csv_file[:-9] + max + '.csv')
        print("New CSV file: {}\n".format(self.csv_file))

    # Write statistics to .csv
    def write_to_log(self):
        # Check if csv filename is initialiased
        if self.csv_file:
            # Headers need to be added if file is created
            if not isfile(self.csv_file):
                self.csv_exist = False

            fieldnames = self.stats.keys()
            #print("CSV file used: {}".format(self.csv_file))
            with open(self.csv_file, 'a') as csvfile:
                csv_stats = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Write header to file first time
                if self.csv_exist == False:
                    csv_stats.writeheader()
                    self.csv_exist = True

                # Add values from dict as new row
                csv_stats.writerow(self.stats)
        else:
            print("No CSV file to write to 0.o")

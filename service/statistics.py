from os import makedirs, getcwd
from os.path import join, isdir, isfile
from glob import glob
import csv

__author__ = 'tom, stef, pieter'


class Statistics:
    def __init__(self):
        self.drivers = []
        self.counts = {'left_go': 0,
                       'right_go': 0,
                       'left_wait': 0,
                       'right_wait': 0
                       }
        self.ratios = {
            'go_ratio': 0.0,
            'wait_ratio': 0.0,
            'left_go_ratio': 0.0,
            'right_go_ratio': 0.0,
            'left_wait_ratio': 0.0,
            'right_wait_ratio': 0.0
        }
        self.stats = self.counts.copy()
        self.stats.update(self.ratios)
        self.csv_file = ''
        self.csv_exist = True

    def driver_update(self, driver_list):
        self.drivers = driver_list

    def update(self):
        # Reset values
        for key in self.counts:
            self.counts[key] = 0

        # Iterate over list of drivers and do statistics
        print self.drivers
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
                        self.counts['left_go'] += 1
                    elif m.action == 'wait':
                        self.counts['left_wait'] += 1

                # Check if driver gave way to the right or did not
                elif m.traffic == [None, None, 1]:
                    # Situation in which there was a driver from the right
                    if m.action == 'go':
                        self.counts['right_go'] += 1
                    elif m.action == 'wait':
                        self.counts['right_wait'] += 1

        # print ("I PASSED FOR LOOP\n")

        if self.counts['left_go'] or self.counts['right_go']:
            # Calculate ratio of agents going when agent coming from the left
            self.ratios['left_go_ratio'] = float(self.counts['left_go']) / len(self.drivers) * 100

            # Calculate ratio of agents going when agent coming from the right
            self.ratios['right_go_ratio'] = float(self.counts['right_go']) / len(self.drivers) * 100

        if self.counts['left_wait'] or self.counts['right_wait']:
            # Calculate ratio of agents waiting when agent coming from the left
            self.ratios['left_wait_ratio'] = float(self.counts['left_wait']) / len(self.drivers) * 100

            # Calculate ratio of agents waiting when agent coming from the right
            self.ratios['right_wait_ratio'] = float(self.counts['right_wait']) / len(self.drivers) * 100

        # print("\n")
        # print ("STATS!!!!!!\n")
        # print self.stats
        # Return dict of statistics
        self.stats = self.counts.copy()
        self.stats.update(self.ratios)
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
        maximum = -1
        print(getcwd())
        print(self.csv_file[:-9])
        for file_name in glob(join('statistics', self.csv_file[:-9] + '*')):  # join('statistics', self.csv_file[:-9])
            print(file_name)
            print(int(file_name[-9:-4]))
            if int(file_name[-9:-4]) > maximum:
                maximum = int(file_name[-9:-4])

        maximum += 1
        maximum = str(maximum).zfill(5)
        self.csv_file = join('statistics', self.csv_file[:-9] + maximum + '.csv')
        print("New CSV file: {}\n".format(self.csv_file))

    # Write statistics to .csv
    def write_to_log(self):
        # Check if csv filename is initialised
        if self.csv_file:
            # Headers need to be added if file is created
            if not isfile(self.csv_file):
                self.csv_exist = False

            fieldnames = self.stats.keys()
            print("CSV file used: {}".format(self.csv_file))
            with open(self.csv_file, 'a') as csvfile:
                csv_stats = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Write header to file first time
                if not self.csv_exist:
                    csv_stats.writeheader()
                    self.csv_exist = True

                # Add values from dict as new row
                csv_stats.writerow(self.stats)
        else:
            print("No CSV file to write to 0.o")

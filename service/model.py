from parameters import Parameters
from crossing import Crossing
from driver import Driver

__author__ = 'tom, stef, pieter'

"""
Instance governing implementation of the simulation.
It holds the parameters of a specific simulation
and keeps track of a cycle's state.
"""


class Model:
    # Prepare the model
    def __init__(self):
        print("Init Model...")
        self.parameters = Parameters()
        self.crossings = []
        self.drivers = []

    # Resets the model to initial state
    def reset(self):
        # Spawn crossings
        dim = self.parameters.get('grid_size')
        self.crossings = []     # Crossings in grid orientation
        row = 0
        # Notice!! Location is [x, y], but in the grid, one first has to access row, then column (so [y][x])
        while row < dim[1]:
            cr_row = []
            col = 0
            while col < dim[0]:
                cr_row.append(Crossing([col, row]))
                col += 1
            self.crossings.append(cr_row)
            row += 1

        # Spawn drivers
        self.drivers = []
        n = self.parameters.get('n_drivers')
        while n > 0:
            driver = Driver('driver' + str(n))
            self.drivers.append(driver)
            # Put at a grid edge
            new_loc = driver.respawn(dim[0], dim[1])
            self.crossings[new_loc[1]][new_loc[0]].put_spawn(driver, dim[0]-1, dim[1]-1)
            n -= 1

    # Handles the phase in which drivers are moved inside crossings
    def transintra(self):
        # Make a (nested) list of starting positions at the beginning of the cycle
        self.state = []

        # Per grid if auto just moved
        print("Y: {}, X: {}".format(self.crossings[0], self.crossings[1]))
        self.may_move = [[True, True]] * (len(self.crossings[0]) * len(self.crossings[1]))

        # Iterate over every crossing
        for i, crossing in enumerate([crossing for row in self.crossings for crossing in row]):
            # Ask for the state of a crossing and append to grid state
            self.state.append(crossing.occupied())

            # Resolve situations, make drivers decide and compute outcome
            sitrep = crossing.resolve()
            if sitrep:
                # There is actually something to do at this crossing
                actions = sitrep.distribute()
                crashed = sitrep.compute_outcome(actions, self.parameters.get('reward'), crossing.loc)
                self.state[-1][-1] = len(crashed)    # Also add crashed drivers to state
                crossing.move_drivers(sitrep, crashed)

                # Don't allow just moved to be used in transinter
                self.may_move[i+crossing.next_cr[0].dir/3][i+crossing.next_cr[1]%3] = False


        # Give global state to the simulation (GUI)
        return self.state

    # Phase in which drivers are moved between crossings
    def transinter(self):
        dim = self.parameters.get('grid_size')  # Load in the grid size
        print("May move:")
        print(self.may_move)

        # Iterate over every crossing
        for crossing in [crossing for row in self.crossings for crossing in row]:
            print("Crossing: {}".format(crossing))
            # Only move car across crossings when it was put in north/west the previous cycle
            if self.may_move[i]:
                # Get the drivers that want to move elsewhere
                translations, crashed = crossing.translate_drivers()

                # Actually move drivers to the correct destinations
                for driver, n_cr, n_dr in translations:
                    # Check whether a driver wants to move outside the grid
                    if n_cr[0] < 0 or n_cr[0] > dim[0]-1 or n_cr[1] < 0 or n_cr[1] > dim[1]-1:
                        # That means that the driver has reached its destination
                        driver.status = 'finished'
                        # Also make this driver respawn
                        new_loc = driver.respawn(dim[0], dim[1])
                        self.crossings[new_loc[1]][new_loc[0]].put_spawn(driver, dim[0]-1, dim[1]-1)
                    else:
                        # Just move to next crossing
                        self.crossings[n_cr[1]][n_cr[0]].enqueue(driver, n_dr)

                # Respawn crashed drivers
                # NOTE: do this after moving within crossing,
                # because they still have to go to the middle, generating a transition
                for driver in crashed:
                    new_loc = driver.respawn(dim[0], dim[1])
                    self.crossings[new_loc[1]][new_loc[0]].put_spawn(driver, dim[0]-1, dim[1]-1)
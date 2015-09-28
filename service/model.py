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

        # Spawn crossings
        dim = self.parameters.get('grid_size')
        self.crossings = []     # Crossings in grid orientation
        row = dim[0]
        while row > 0:
            cr_row = []
            col = dim[1]
            while col > 0:
                print 'cr_loc:', dim[0]-row, dim[1]-col
                cr_row.append(Crossing([dim[0]-row, dim[1]-col]))
                col -= 1
            self.crossings.append(cr_row)
            row -= 1

        # Spawn drivers
        self.drivers = []
        n = self.parameters.get('n_drivers')
        while n > 0:
            driver = Driver('driver' + str(n))
            self.drivers.append(driver)
            # Put at a grid edge
            new_loc = driver.respawn(dim[0], dim[1])
            self.crossings[new_loc[0]][new_loc[1]].put_spawn(driver, dim[0]-1, dim[1]-1)
            n -= 1

    # Handles the phase in which drivers are moved inside crossings
    def transintra(self):
        # Iterate over every crossing
        for crossing in [crossing for row in self.crossings for crossing in row]:
            # Resolve situations, make drivers decide and compute outcome
            sitrep = crossing.resolve()
            if sitrep:
                # There is actually something to do at this crossing
                actions = sitrep.distribute()
                crashed = sitrep.compute_outcome(actions, self.parameters.get('reward'), crossing.loc)
                crossing.move_drivers(sitrep, crashed)

    # Phase in which drivers are moved between crossings
    def transinter(self):
        dim = self.parameters.get('grid_size')  # Load in the grid size

        # Iterate over every crossing
        for crossing in [crossing for row in self.crossings for crossing in row]:
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
                    self.crossings[new_loc[0]][new_loc[1]].put_spawn(driver, dim[0]-1, dim[1]-1)
                else:
                    # Just move to next crossing
                    self.crossings[n_cr[0]][n_cr[1]].enqueue(driver, n_dr)

            # Respawn crashed drivers
            # NOTE: do this after moving within crossing,
            # because they still have to go to the middle, generating a transition
            for driver in crashed:
                new_loc = driver.respawn(dim[0], dim[1])
                self.crossings[new_loc[0]][new_loc[1]].put_spawn(driver, dim[0]-1, dim[1]-1)

    # DEPRACATED PROCEDURE SINCE SEGREGATION
    # A procedure to update the model to the next cycle
    def update(self):

        # Iterate over every crossing
        for crossing in [crossing for row in self.crossings for crossing in row]:
            # Resolve situations, make drivers decide and compute outcome
            # TODO ensure right order in this loop!
            sitrep = crossing.resolve()
            actions = sitrep.distribute()
            crashed = sitrep.compute_outcome(actions, self.parameters.get('reward'), crossing.loc)
            # TODO make them collisions collide collisions yolo
            crossing.move_drivers(sitrep, crashed)
            # Respawn crashed drivers
            # NOTE: do this after moving, because they still have to go to the middle, generating a transition
            dim = self.parameters.get('grid_size')
            for driver in crashed:
                new_loc = driver.respawn(dim[0], dim[1])
                self.crossings[new_loc[0]][new_loc[1]].put_spawn(driver, dim[0]-1, dim[1]-1)
            # Move remaining drivers
            translations = crossing.translate_drivers()
            # Actually move drivers to the correct destinations
            for driver, n_cr, n_dr in translations:
                # Check whether a driver wants to move outside the grid
                if n_cr[0] < 0 or n_cr[0] > dim[0]-1 or n_cr[1] < 0 or n_cr[1] > dim[1]-1:
                    # That means that the driver has reached its destination
                    driver.status = 'finished'
                    # Also make this driver respawn
                    new_loc = driver.respawn(dim[0], dim[1])
                    self.crossings[new_loc[0]][new_loc[1]].put_spawn(driver, dim[0]-1, dim[1]-1)
                else:
                    # Just move to next crossing
                    self.crossings[n_cr[0]][n_cr[1]].enqueue(driver, n_dr)

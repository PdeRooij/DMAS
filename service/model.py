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

        # Spawn drivers
        self.drivers = []
        n = self.parameters.get('n_drivers')
        while n > 0:
            self.drivers.append(Driver('driver' + str(n)))
            n -= 1

        # Spawn crossings
        dim = self.parameters.get('grid_size')
        self.crossings = []     # Crossings in grid orientation
        row = dim[0]
        while row > 0:
            cr_row = []
            col = dim[1]
            while col > 0:
                cr_row.append(Crossing())
                col -= 1
            self.crossings.append(cr_row)
            row -= 1

    # A procedure to update the model to the next cycle
    def update(self):

        # Iterate over every crossing
        for crossing in [crossing for row in self.crossings for crossing in row]:
            # Resolve situations, make drivers decide and compute outcome
            sitrep = crossing.resolve()
            actions = sitrep.distribute()

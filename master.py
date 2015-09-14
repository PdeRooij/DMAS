
#!usr/bin/python

__author__ = 'tom, stef, pieter'

from model.model import Model # from Model.model
from interface.gui import GUI  # from Interface.gui

"""
This class contains the main loop of the simulation.
It ensures everything is set-up properly, then it starts the simulation
and runs it in cycles while handling the transitions between those.
"""

############################
"These are the functions to rule them all."
############################

class Simulation:

    # Class containing the entire simulation.
    # Everything is run by a subsequent call by this class.

    # Initialize the simulation
    def __init__(self):
        # Build model and interface
        self.model = Model()
        self.gui = GUI()

        # Initiate zeroth cycle
        self.cycle = 0

    # Run the simulation
    def run(self):
        # For as long as the number of cycles specified in the parameters
        max_cycles = self.model.parameters.get('max_cycles')
        while self.cycle < max_cycles:
            self.model.update()
            self.gui.update()

        # Here something to analyze emergence?
        # It could be a separate method
        analysis = True
        while analysis:
            # Make false to end analysis
            analysis = False

    # Perhaps something to leave the user a neat and tidy system
    def quit(self):
        # Teehee! I got you good! Not doin' nothin'... or do I?
        pass

# Initialize a simulation instance and call its run function
if __name__ == '__main__':
    sim = Simulation()
    sim.run()
    sim.quit()
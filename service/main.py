#!usr/bin/python

__author__ = 'tom, stef, pieter'

from sys import exit
import osc  # from kivy.lib import osc
from time import sleep
from model import Model

"""
This class contains the main loop of the simulation.
It ensures everything is set-up properly, then it starts the simulation
and runs it in cycles while handling the transitions between those.
"""

############################
"These are the functions to rule them all."
############################


# Class that does all the agent stuff when simulation is running (not used yet)
class Simulation():
    # Initialize the simulation
    def __init__(self):
        print("\nInit master...")
        # Build model
        self.model = Model()
        self.agent_action = []

        # Initiate zeroth cycle
        self.cycle = 0

    # Run the simulation
    def run(self):
        # For as long as the number of cycles specified in the parameters
        max_cycles = self.model.parameters.get('max_cycles')
        print("Max cycles: {}".format(max_cycles))
        #while self.cycle < max_cycles:
        self.model.update()
        self.gui.update()
        self.cycle += 1

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

# osc for publishing/receiving messages to/from the listener (gui or non-gui)
class osc_message():
    def __init__(self):
        osc.init()
        oscid = osc.listen(ipAddr='0.0.0.0', port=3000)
        # Receive start/stop message
        osc.bind(oscid, self.startquit, '/start')
        self.can_start = False
        # Send status of simulation
        osc.bind(oscid, self.send_hello, '/hello')
        # Hello world messages
        osc.bind(oscid, self.simulation_status_send, '/simu-status_ask')

        # Init actual model
        #self.sim = Simulation()

        self.model = Model()
        self.cycle = 0
        self.max_cycles = self.model.parameters.get('max_cycles')
        print("Max cycles: {}".format(self.max_cycles))

        # Send server is running
        self.simulation_status_send()

        # Code always running / waiting for instructions
        while True:
            # Try so that a server stopped message can be send
            try:
                print("Current cycle: {}".format(self.cycle))
                osc.readQueue(oscid)
                # Only run simulation when started and max cycles not reached
                #print("Start: {}, Max Cycles: {}".format(self.can_start, self.max_cycles))
                if self.can_start == True and self.cycle < self.max_cycles:
                    #self.sim.run()

                    # Hello world test
                    self.cycle += 1
                    self.send_hello()

                sleep(0.5)

            # Send message server stopped
            except (KeyboardInterrupt, SystemExit):
                self.send_server_stop()
                exit()

    # Change simulation status based on message from listener
    def startquit(self, can_start, *args):
        if can_start[2] == True:
            print("\n    Simulation started    ")
            print(can_start)
            print("params: can_start: {}, max_cycle: {}, agent_num: {}, grid: {}x{}"
                  .format(can_start[2], can_start[3], can_start[4], can_start[5], can_start[6]))
            self.can_start = True
            self.max_cycles = can_start[3]
            self.agent_num = can_start[4]
            self.grid = [can_start[5], can_start[6]]
        elif can_start[2] == False:
            print("\n    Simulation ended    ")
            self.cycle = 0
            self.can_start = False
        else:
            print("\n    Simulation paused    ")
            self.can_start = False

    # Informs the listener whether the simulation is running or not
    def simulation_status_send(self, *args):
        print("Send simulation status")
        msg = []
        osc.sendMsg('/simu-status', [self.can_start, self.cycle, ], port=3002)

    # Send text message "Hello world" to listener
    def send_hello(self, *args):
        #print("sending cycle")
        osc.sendMsg('/receive_hello', [self.cycle, ], port=3002)

    # Send message server stopped
    def send_server_stop(self, *args):
        osc.sendMsg('/server-stop', port=3002)

# Initialize a server instance for agent simulation
if __name__ == '__main__':
    osc_message()
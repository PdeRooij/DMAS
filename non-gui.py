#!usr/bin/python

__author__ = 'tom, stef, pieter'

import os
import sys
import service.osc as osc
from time import sleep
from service.model import Model

class ClientServerApp():
    def __init__(self):
        osc.init()
        oscid = osc.listen(port=3002)
        # Send start/stop simulation
        osc.bind(oscid, self.start_simulation, '/send_start')
        # Receive cycle status
        osc.bind(oscid, self.output_cycle, '/receive_hello')
        # Retrieve simulation status
        osc.bind(oscid, self.simulation_status_receive, '/simu-status')
        # Retrieve server stopped
        osc.bind(oscid, self.server_stopped, '/server-stop')
        # Receive grid status
        osc.bind(oscid, self.grid_update, '/states')

        # Params
        self.cycle = 0
        self.server_running = False
        self.start_simu = True
        self.max_cycle = 10
        self.agents_num = 10
        self.grid = [1, 1]

        # Read params from txt file
        self.params_txt()

        # Send message asking for simulation status
        osc.sendMsg('/simu-status_ask', [], port=3000)

        while True:
            osc.readQueue(oscid)

    #   Give Commands to Service
    # Tells the server to start/pause the agent simulation and the parameters
    def start_simulation(self):
        print("PERMISSION GRANTED: Simulation start!")
        osc.sendMsg('/start', [True, self.max_cycle, self.agents_num,
                               self.grid[0], self.grid[1]], port=3000)

    def stop_simulation(self):
        print("ABORT THE SIMULATION!")
        osc.sendMsg('/start', [False, ], port=3000)
        self.cycle = 0
        self.start_simu = True

    # Read parameters from .txt file
    def params_txt(self):
        txt_file = "result-params.txt"
        if os.path.isfile(txt_file):
            # self.params = open(txt_file).readlines()
            with open(txt_file) as f:
                self.params = f.readlines()

            # Convert lines from txt file to int numbers
            print(self.params.pop(0))
            self.params = [l.strip('\n') for l in self.params]
            self.params = [map(int, l.split(',')) for l in self.params]
            print(self.params)

        else:
            print("'result-params.txt' not found")
            sys.exit()

    # Use next line of txt file for params
    def set_params(self):
        p = self.params.pop(0)
        self.max_cycle = p[0]
        self.agents_num = p[1]
        self.grid = [p[2], p[3]]

    # !!! Commands to server for statistics !!!
    def command_simulation(self):
        if self.server_running:
            # Reset server if simulation has started
            if not self.start_simu:
                self.stop_simulation()
                self.start_simu = True

            print("Service is running!")
            # Still new params to send
            if self.params:
                # Set new params
                self.set_params()

                # Send next set of parameters for simulation if available
                print("Commands incomming!")
                self.start_simulation()

            # All params have been send
            else:
                print("All simulations succesfully ran :D")
                sys.exit()

        # Service is not running
        else:
            print("ServicE noT activE!!! 0.o")
            sys.exit()

    # Cycle status
    def output_cycle(self, message, *args):
        print("Cycle: {}".format(message[2]))
        self.cycle = message[2]

        # Max cycles reached, rerun simulation with new params
        if self.cycle >= self.max_cycle:
            print("Max cycles reached, new simulation should be run!")
            self.start_simu = False
            self.command_simulation()

    #   Receive status from Service
    # Receive whether the service and/or simulation is running
    def simulation_status_receive(self, message, *args):
        print("Simulation status: {}".format(message))
        self.start_simu = not message[2]
        self.cycle = message[3]
        self.server_running = True
        self.grid = [message[4], message[5]]

        # Run the simulation for results
        self.command_simulation()

    # Server sends message it crashed
    def server_stopped(self, message, *args):
        print("SERVER HAS CRASHED !@#!@#!@$")
        self.server_running = False
        self.start_simu = True
        self.cycle = 0

    def grid_update(self, *args):
        pass

if __name__ == '__main__':
    ClientServerApp()
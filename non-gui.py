#!usr/bin/python

__author__ = 'tom, stef, pieter'

import service.osc as osc
from time import sleep
from service.model import Model

class ClientServerApp():
    def __init__(self):
        osc.init()
        oscid = osc.listen(port=3002)
        osc.bind(oscid, self.start_simulation, '/send_start')
        osc.bind(oscid, self.output_hello, '/receive_hello')
        self.start_simulation()
        while True:
            osc.readQueue(oscid)
            #sleep(0.5)

    def start_simulation(self, *args):
        print("PERMISSION GRANTED: Simulation start!")
        osc.sendMsg('/start', [True, ], port=3000)

    def output_hello(self, message, *args):
            print("Received: {}".format(message[2]))

if __name__ == '__main__':
    ClientServerApp()
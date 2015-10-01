#!/usr/bin/python
__author__ = 'tom, stef, pieter'

import sys
from kivy.app import App
from kivy.lib import osc
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, ReferenceListProperty, ListProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.graphics import Rectangle, Color
from os import path
platform = platform()

from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')

"""
The super file which is above and beyond everything happening visually.
Of course a multi-line comment is only justified if it contains multiple lines.
"""

# class Car(ObjectProperty):
#     pass

class Crossing(Label):
    # north, east, south, west, middle
    spot = ListProperty([0, 0, 0, 0, 0])
    grid_no = NumericProperty(-1)

    def __init__(self, **kwargs):
        super(Crossing, self).__init__(**kwargs)
        # call draw_car when 'spot' values are changed
        self.bind(spot=self.draw_car)

    # Draw/removes car when variable spot is changed
    def draw_car(self, *args):
        print("Grid no: {}".format(self.grid_no))
        print("draw car with: {}".format(self.spot))
        print(self.pos)
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(source=path.join('img','red-car.png'), pos=[self.pos[0]/2, self.pos[1]/2],
                      size=[self.size[0]/5, self.size[1]/5])
            # if self.spot[0] >= 1:
            #     Rectangle(source=path.join('img','red-car.png'), pos_hint = {'top': .9},
            #               size=[self.size[0]/5, self.size[1]/5])
            # if self.spot[1] >= 1:
            #     Rectangle(source=path.join('img','red-car.png'), pos= {'right': .9},
            #               size=[self.size[0]/5, self.size[1]/5])
            # if self.spot[2] >= 1:
            #     Rectangle(source=path.join('img','red-car.png'), pos=[self.pos[0]/2, self.pos[1]/2],
            #               size=[self.size[0]/5, self.size[1]/5])
        #self.canvas.add(path.join('img','red-car2.png'))
        #self.canvas.add(Image(pos=self.pos, size=(100, 100)))


# Class for graphical shizzle.
class GUIApp(App):
    # Variables that automatically update GUI
    start_simu = BooleanProperty(True)
    server_running = BooleanProperty(False)
    cycle = NumericProperty(0)
    max_cycle = NumericProperty(100)
    agents_num = NumericProperty(10)
    rows = NumericProperty(2)
    columns = NumericProperty(2)
    grid = ReferenceListProperty(rows, columns)

    def __init__(self, **kwargs):
        super(GUIApp, self).__init__(**kwargs)

        # Grid changes
        self._size_handler_trigger = Clock.schedule_once(self._size_handler)  # Clock.create_trigger
        self.bind(grid=self._size_handler_trigger)


    # Initialize grid and such
    def build(self):
        self.title = "Traffic simulator"

        # Android
        self.service = None
        self.start_service()

        # osc messages init
        osc.init()
        oscid = osc.listen(port=3002)
        # Send start/stop simulation
        osc.bind(oscid, self.start_simulation, '/send_start')
        # Receive hello world
        osc.bind(oscid, self.output_hello, '/receive_hello')
        # Retrieve simulation status
        osc.bind(oscid, self.simulation_status_receive, '/simu-status')
        # Retrieve server stopped
        osc.bind(oscid, self.server_stopped, '/server-stop')
        # Read received messages
        Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0)
        # Receive grid status
        osc.bind(oscid, self.grid_update, '/states')

        # Send message asking for simulation status
        osc.sendMsg('/simu-status_ask', [], port=3000)

        # Grid changes
        # self._size_handler_trigger = Clock.schedule_once(self._size_handler)  # Clock.create_trigger
        # self.bind(grid=self._size_handler_trigger)

        # normal variables
        self.grid_spots = []

        if not self.server_running:
            print("Simulation server not running")
            self.root.ids.label.text = "Simulation server not running :(\n"

    def start_service(self):
        if platform == 'android':
            from android import AndroidService
            service = AndroidService('Agent emergence service', 'running')
            service.start('service started')
            self.service = service

    # GUI pause
    def on_pause(self):
        # Keep the app running when minimizing app
        return True

    # GUI close
    def on_stop(self):
        # On Android, stop service
        if platform == 'android':
            self.service.stop()
            self.service = None

    # Tells the server to start/pause the agent simulation and the parameters
    def start_simulation(self, *args):
        if self.start_simu == True:
            print("PERMISSION GRANTED: Simulation start!")
            self.root.ids.label.text += 'Simulation START\n'
            osc.sendMsg('/start', [True, int(self.max_cycle), int(self.agents_num),
                                   int(self.grid[0]), int(self.grid[1])], port=3000)
            self.start_simu = False
        else:
            print("Simulation is on holiday")
            self.root.ids.label.text += 'Simulation PAUSE\n'
            osc.sendMsg('/start', ['pause', ], port=3000)
            self.start_simu = True

    # Tells the server to stop the agent simulation
    def stop_simulation(self, *args):
        print("ABORT THE SIMULATION!")
        self.root.ids.label.text += 'Simulation STOP\n'
        osc.sendMsg('/start', [False, ], port=3000)
        self.start_simu = True
        self.cycle = 0
        crossing_obj = App.get_running_app().root.ids.gridy.children
        for child in crossing_obj:
            child.spot = [0, 0, 0, 0, 0]

    # Receive whether the service and/or simulation is running
    def simulation_status_receive(self, message, *args):
        print("Simulation status: {}".format(message))
        self.root.ids.label.text = "Simulation server running!!!\n"
        self.start_simu = not message[2]
        self.cycle = message[3]
        self.root.ids.label.text += "Current cycle: {}\n".format(self.cycle)
        self.server_running = True
        self.grid = [message[4], message[5]]

    # Print out the received message "Hello world"... printed out :(   now it prints cycle status
    def output_hello(self, message, *args):
        print("Received: {}".format(message[2]))
        self.root.ids.label.text += '{}\n'.format(message[2])
        self.cycle = message[2]

    # Server sends message it crashed
    def server_stopped(self, message, *args):
        self.server_running = False
        self.start_simu = True
        self.cycle = 0
        self.root.ids.label.text += 'SERVER HAS CRASHED !@#!@#!@$\n\n'

    # Update grid agents based on server message
    def grid_update(self, message, *args):
        print(message)
        if message[2] == "start":
            print("Starting grid update...")
            self.grid_spots[:] = []
        elif message[2] == "end":
            print("All grid messages received")
            print(self.grid_spots)
            # Update GUI grid agents
            crossing_obj = App.get_running_app().root.ids.gridy.children
            for i, s in enumerate(reversed(self.grid_spots)):
                crossing_obj[i].spot = s

            #self.grid_spots[:] = []
            print("Grid updated ^-^")
        else:
            self.grid_spots.append(message[2:7])

    def _size_handler(self, *largs):
        print("Grid change")
        # Get number of crossings in grid
        crossing_obj = App.get_running_app().root.ids.gridy.children
        crossing_len = len(crossing_obj)
        grid_size = self.grid[0] * self.grid[1]

        # Add crossings if grid is not full yet
        while crossing_len < grid_size:
            print("crossing_len: {}".format(crossing_len))
            # grid_no = grid id number
            App.get_running_app().root.ids.gridy.add_widget(Crossing(grid_no=crossing_len))
            crossing_len += 1

        # Remove crossings one for one while more crossings than grid size
        while crossing_len > grid_size:
            App.get_running_app().root.ids.gridy.remove_widget(crossing_obj[0])
            crossing_len -= 1


if __name__ == '__main__':
    # This is the GUI for the agent simulation
    if len(sys.argv) > 1:
        # More arguments given than just the filename
        print('Oooh, you discovered the super secret corners of our program!')
        print("Let's see what you shady things you expect from me...")
        # Handle optional command line arguments
        for argument in sys.argv[1:]:
            # Of course, we do not intend to comply. :)
            print("Nope, don't know what to do with argument", argument)

    # In the end, just run the program.
    GUIApp().run()
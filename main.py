__author__ = 'tom, stef, pieter'

from kivy.app import App
from kivy.lib import osc
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, ListProperty, ReferenceListProperty
from kivy.utils import platform
platform = platform()

from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')

"""
The super file which is above and beyond everything happening visually.
Of course a multi-line comment is only justified if it contains multiple lines.
"""

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

        # variables
        #self.grid = [2,2]
        # Send message asking for simulation status
        osc.sendMsg('/simu-status_ask', [], port=3000)

        if not self.server_running:
            print("Simulation server not running")
            self.root.ids.label.text = "Simulation server not running :(\n"

    def start_service(self):
        if platform == 'android':
            from android import AndroidService
            service = AndroidService('Agent emergence service', 'running')
            service.start('service started')
            self.service = service

    def on_pause(self):
        # Keep the app running when minimizing app
        return True

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

    # Receive whether the service and/or simulation is running
    def simulation_status_receive(self, message, *args):
        print("Simulation status: {}".format(message))
        self.root.ids.label.text = "Simulation server running!!!\n"
        self.start_simu = not message[2]
        self.cycle = message[3]
        self.root.ids.label.text += "Current cycle: {}\n".format(self.cycle)
        self.server_running = True

    # Print out the received message "Hello world"... printed out :(   now it prints cycle status
    def output_hello(self, message, *args):
        print("Received: {}".format(message[2]))
        self.root.ids.label.text += '{}\n'.format(message[2])
        self.cycle = message[2]

    def server_stopped(self, message, *args):
        self.server_running = False
        self.start_simu = True
        self.cycle = 0
        self.root.ids.label.text += 'SERVER HAS CRASHED !@#!@#!@$\n\n'

if __name__ == '__main__':
    GUIApp().run()
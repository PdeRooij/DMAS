__author__ = 'tom, stef, pieter'

from kivy.app import App
from kivy.lib import osc
from kivy.clock import Clock
from kivy.properties import BooleanProperty

"""
The super file which is above and beyond everything happening visually.
Of course a multi-line comment is only justified if it contains multiple lines.
"""

# Class for graphical shizzle.
class GUIApp(App):
    # Variables that automatically update GUI
    start_simu = BooleanProperty(True)
    server_running = BooleanProperty(False)

    # Initialize grid and such
    def build(self):
        self.title = "Traffic simulator"

        # osc messages init
        osc.init()
        oscid = osc.listen(port=3002)
        # Send start/stop simulation
        osc.bind(oscid, self.start_simulation, '/send_start')
        # Receive hello world
        osc.bind(oscid, self.output_hello, '/receive_hello')
        # Retrieve simulation status
        osc.bind(oscid, self.simulation_status_receive, '/simu-status')
        Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0)

        # variables
        # Send message asking for simulation status
        osc.sendMsg('/simu-status_ask', [], port=3000)

        if not self.server_running:
            print("Simulation server not running")
            self.root.ids.label.text = "Simulation server not running :(\n"

    def update(self):
        pass

    def on_stop(self):
        # send message to let server stop sending message to here
        pass
    
    def start_simulation(self, *args):
        if self.start_simu == True:
            print("PERMISSION GRANTED: Simulation start!")
            self.root.ids.label.text += 'Simulation START\n'
            osc.sendMsg('/start', [self.start_simu, ], port=3000)
            self.start_simu = False
        else:
            print("ABORT THE SIMULATION!")
            self.root.ids.label.text += 'Simulation STOP\n'
            osc.sendMsg('/start', [self.start_simu, ], port=3000)
            self.start_simu = True

    def simulation_status_receive(self, message, *args):
        print("Simulation status: {}".format(message[2]))
        self.root.ids.label.text = "Simulation server running!!!\n"
        self.start_simu = not message[2]
        self.server_running = True

    def output_hello(self, message, *args):
        print("Received: {}".format(message[2]))
        self.root.ids.label.text += '%s\n' % message[2]

if __name__ == '__main__':
    GUIApp().run()
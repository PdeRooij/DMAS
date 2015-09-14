from kivy.app import App
from kivy.lang import Builder
from kivy.lib import osc
from kivy.utils import platform
from kivy.clock import Clock

activityport = 3001
serviceport = 3000

kv = '''
Button:
    text: 'push me!'
    on_press: app.ping()
'''

class ServiceApp(App):
    def build(self):
        if platform == 'android':
            from android import AndroidService
            service = AndroidService('my pong service', 'running')
            service.start('service started')
            self.service = service

        osc.init()
        oscid = osc.listen(ipAddr='127.0.0.1', port=activityport)
        osc.bind(oscid, some_api_callback, '/some_api')
        Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0)

        return Builder.load_string(kv)

    def ping(self):
        osc.sendMsg('/some_api', ['ping', ], port=someotherport)

    def some_api_callback(self, message, *args):
        print("got a message! %s" % message)
        self.root.text += '\n%s' % message[2]

if __name__ == '__main__':
    ServiceApp().run()
from time import sleep
from kivy.lib import osc

serviceport = 3000
activityport = 3001

def some_api_callback(message, *args):
    print("got a message! %s" % message)
    answer_message()

def answer_message():
    osc.sendMsg('/some_api', [asctime(localtime()), ], port=activityport)

if __name__ == '__main__':
    osc.init()
    oscid = osc.listen(ipAddr='127.0.0.1', port=serviceport)
    osc.bind(oscid, some_api_callback, '/some_api')

    while True:
        osc.readQueue(oscid)
        sleep(.1)
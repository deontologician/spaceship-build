'''This is the commandline'''

import cmd
import shlex
import spaceship


class SpaceshipCommand(cmd.Cmd):
    intro = 'Welcome to Spaceship Build'
    prompt = '> '
    file = None

    def __init__(self, busname):
        self.bus = spaceship.Bus(busname)
    
    #----Spaceship Commands
    def do_broadcast(self, arg):
        'Broadcast message from terminal to attached Buses: BROADCAST FIRE'
        topic, message, *_ = shlex.split(arg)
        self.bus.broadcast(topic, message)

    def do_subscribe(self, topic_key):
        'Subscribe to message using the topic key, they will be visiable in the console: SUBSCRIBE DAMAGEREPORT'
        self.bus.subscribe(topic_key, spaceship.basic_subscriber)

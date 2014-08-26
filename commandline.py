'''This is the commandline'''

import sys
import cmd
import shlex
import spaceship
import random
from inventory import Inventory


class SpaceshipCommand(cmd.Cmd):
    intro = 'Welcome to Spaceship Build'
    prompt = '> '
    file = None

    def __init__(self, busname):
        self.bus = spaceship.Bus(busname)
        self.inventory = Inventory()
        super().__init__()

    def do_exit(self, _):
        '''Exits the game'''
        print(random.choice([
            'So long!',
            'Toodles!',
            'Sayonara!',
            'Best of luck!',
            "Don't leave!"]))
        return True
    
    #----Spaceship Commands
    def do_broadcast(self, arg):
        '''Broadcast message from terminal to attached Buses:

        > broadcast guns.all fire!
        > broadcast system.report 'Everything nominal'
        '''
        topic, message, *_ = shlex.split(arg)
        self.bus.broadcast(topic, message)

    def do_subscribe(self, topic_key=''):
        '''Subscribe to message using the topic key, they will be
        visible in the console. If no argument given, all topics are
        subscribed to.

        > subscribe damage.report
        > subscribe guns
        > subscribe
        '''
        self.bus.subscribe(topic_key, spaceship.basic_subscriber)

'''This is the commandline'''

import sys
import cmd
import shlex
import spaceship
import random
from inventory import Inventory
from shop import Shop

class SpaceshipCommand(cmd.Cmd):
    intro = 'Welcome to Spaceship Build'
    prompt = '> '
    file = None

    def __init__(self, busname):
        self.bus = spaceship.Bus(busname)
        self.inventory = Inventory()
        self.shop = Shop()
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

    def do_EOF(self, arg):
        '''Handles Ctrl+D'''
        return self.do_exit(arg)
    
    #----Spaceship Commands
    def do_broadcast(self, arg):
        '''Broadcast message from terminal to attached Buses:

        > broadcast guns.all fire!
        > broadcast system.report 'Everything nominal'
        '''
        topic, message, *_ = shlex.split(arg)
        self.bus.broadcast(topic, message)

    def do_buy(self, type_name):
        '''This purchases an item from the shop and puts it into the
        player's inventory

        > buy raygun
        Raygun-001 purchased and added to inventory.
        '''
        item = self.shop.buy(type_name)
        if item is None:
            print("Can't buy {!r} there's nothing like that."
                  .format(type_name))
        else:
            self.inventory.store(item)
            print(item, "purchased and added to inventory.")
       
        
    def do_subscribe(self, topic_key=''):
        '''Subscribe to message using the topic key, they will be
        visible in the console. If no argument given, all topics are
        subscribed to.

        > subscribe damage.report
        > subscribe guns
        > subscribe
        '''
        self.bus.subscribe(topic_key, spaceship.basic_subscriber)

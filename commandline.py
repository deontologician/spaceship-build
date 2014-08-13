'''This is the commandline'''

import cmd
import shlex
import spaceship


class SpaceshipCommand(cmd.Cmd):
	intro = 'Welcome to Spaceship Build'
	prompt = '>'
	bus = spaceship.Bus('Spaceshipbus')
	file = None
	
	#----Spaceship Commands
	def do_broadcast(self, arg):
		'Broadcast message from terminal to attached Buses: BROADCAST FIRE'
		self.bus.broadcast(*shlex.split(arg))

	def do_subscribe(self, arg):
		'Subscribe to message using the topic key, they will be visiable in the console: SUBSCRIBE DAMAGEREPORT'
		self.bus.subscribe(arg, spaceship.basic_subscriber)

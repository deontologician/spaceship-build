import uuid
import spaceship

class Component:

    def __init__(self):
        self.id = uuid.uuid4()
        self.name = '{} - {:03}'.format(type(self).__name__, type(self).counter)
        self.mass = 0
        self.bus = spaceship.Bus(self.name)


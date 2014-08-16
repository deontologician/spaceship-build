import uuid
import spaceship

class Component:

    def __init__(self):
        self.id = uuid.uuid4()
        self.name = '{} - {:03}'.format(type(self).__name__, type(self).counter)
        self.mass = 0
        self.bus = spaceship.Bus(self.name)

class BasicGun:
    counter = 1

    def __init__(self):
        self.id = uuid.uuid4()
        self.name = '{}-{:03}'.format(type(self).__name__, self.counter)
        self.counter += 1
        self.ammo_port = AmmoPort32mm()
        self.power_port = PowerPort()
        self.cooling_port = CoolingPort()
        self.attachment = MediumAttachment(self)
        self.weight = 32
        self.baseline_power_draw = 1

        self.bus = Bus(self.name)


class BasicChassis:
    def __init__(self):
        self.power_port = PowerPort()
        self.ammo_port = AmmoPort32mm()
        self.cooling_port = CoolingPort()
        self.attachments = {
            'A': [MediumAttachment(self), MediumAttachment(self)],
            'B': [SmallAttachment(self), SmallAttachment(self)],
        }

        self.mass = 50
        self.baseline_power_draw = 0
        self.baseline_cooling_draw = 0

        self.bus = Bus()


class CoolingConduit:
    def __init__(self):
        self.port_a = None
        self.port_b = None
        self.bandwidth = 34
        self.bus = Bus()

    def attach(self, port_a, port_b=None):
        '''Attach the cable to one or more ports'''
        self.port_a = port_a
        self.port_b = port_b


class AmmoFeed32mm:
    def __init__(self):
        self.out_port = None
        self.in_port = None
        self.bandwidth = 32
        self.latency = 1

    def attach(self, in_port=None, out_port=None):
        self.in_port = in_port
        self.out_port = out_port


class PowerCable:
    def __init__(self):
        self.port_a = None
        self.port_b = None
        self.bandwidth = 50

    def attach(self, port_a, port_b=None):
        self.port_a = port_a
        self.port_b = port_b




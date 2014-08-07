import cmd

class Bus(object):
    def __init__(self, priority):
        self.priority = priority
        self.parent = None
        self.children = []
        self.subscribers = []

    def attach(self, other):
        '''Attach this bus to another. Whichever bus has the higher
        priority becomes the parent
        '''
        if self.priority < other.priority:
            other.combine(self)
        else:
            other.parent = self
            self.children.append(other)

    def detach(self):
        '''Detach this Bus from its parent'''
        self.parent.children.remove(self)
        self.parent = None

    def broadcast(self, topic, message):
        for subscriber in self.subscribers:
            subscriber.push(topic, message)
        for child in self.children:
            child.broadcast(topic, message)


class BasicGun(object):
    def __init__(self):
        self.ammo_port = AmmoPort32mm()
        self.power_port = PowerPort()
        self.cooling_port = CoolingPort()
        self.attachment = MediumAttachment(self)

        self.weight = 32
        self.baseline_power_draw = 1

        self.bus = Bus()


class BasicChassis(object):
    def __init__(self):
        self.power_port = PowerPort()
        self.ammo_port = AmmoPort32mm()
        self.cooling_port = CoolingPort()
        self.attachments = {
            'A': [MediumAttachment(self), MediumAttachment(self)],
            'B': [SmallAttachment(self), SmallAttachment(self)],
        }

        self.weight = 50
        self.baseline_power_draw = 0
        self.baseline_cooling_draw = 0

        self.bus = Bus()


class CoolingConduit(object):
    def __init__(self):
        self.port_a = None
        self.port_b = None
        self.bandwidth = 34
        self.bus = Bus()

    def attach(self, port_a, port_b=None):
        '''Attach the cable to one or more ports'''
        self.port_a = port_a
        self.port_b = port_b


class AmmoFeed32mm(object):
    def __init__(self):
        self.out_port = None
        self.in_port = None
        self.bandwidth = 32
        self.latency = 1

    def attach(self, in_port=None, out_port=None):
        self.in_port = in_port
        self.out_port = out_port


class PowerCable(object):
    def __init__(self):
        self.port_a = None
        self.port_b = None
        self.bandwidth = 50

    def attach(self, port_a, port_b=None):
        self.port_a = port_a
        self.port_b = port_b


class AmmoPort32mm(object):
    pass

class PowerPort(object):
    pass

class CoolingPort(object):
    pass


class Attachment(object):
    def __init__(self, owner):
        self.owner = owner # Some component
        self.attachee = None  # Some other attachment

    def attach(self, other):
        if self.attachee is None:
            self.attachee = other
            other.attach(self)

    def detach(self):
        self.attachee = None

    
class MediumAttachment(Attachment):
    weight_tolerance = 50


class SmallAttachment(Attachment):
    weight_tolerance = 25


class Terminal(object):
    def __init__(self):
        self.buses = {
            'A': None,
            'B': None,
            'C': None,
        }

    def connect(self, component):
        for key, value in self.probes.iteritems():
            if value is None:
                self.probes[key] = component

    def broadcast(self, topic, message):
        for bus in self.buses:
            bus.broadcast(topic, message)


def main():
    terminal = Terminal()
    chassis = BasicChassis()
    terminal.connect(chassis.bus)
    gun = BasicGun()
    cooling_conduit = CoolingConduit()
    cooling_conduit.attach(gun.cooling_port, chassis.cooling_port)
    ammo_feed = AmmoFeed32mm()
    ammo_feed.attach(in_port=chassis.ammo_port, out_port=gun.ammo_port)
    power_cable = PowerCable()
    power_cable.attach(chassis.power_port, gun.power_port)
    chassis.attachments['A'][0].attach(gun.attachment)
    # Ok now the gun is attached... let's fire the gun
    broadcast('fire.gun')
    


if __name__ == '__main__':
    main()



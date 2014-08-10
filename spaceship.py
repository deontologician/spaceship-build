import cmd
import uuid
import pathlib
from collections import namedtuple
from io import StringIO


class BusMessage:
    __slots__ = ('topic', 'message', 'sender', 'size')

    def __init__(self, topic, message, sender, size=0):
        self.topic = topic
        self.message = message
        self.sender = sender
        self.size = size


class Bus:
    '''Data connections between components.'''

    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []

    @property
    def child_count(self):
        return sum(1 + child.child_count for child in self.children)

    @property
    def lineage(self):
        obj = self
        while obj.parent:
            yield obj.parent
            obj = obj.parent

    @property
    def path(self):
        path = pathlib.PurePosixPath(self.name)
        for ancestor in self.lineage:
            path = ancestor.name / path
        return path

    def _push(self, msg):
        for child in self.children:
            if msg.sender != child.path:
                child._push(msg)
        if self.parent is not None:
            self.parent._push(msg)

    def broadcast(self, topic, fmt, *args, **kwargs):
        msg = fmt.format(*args, **kwargs)
        bus_msg = BusMessage(topic, msg, self.path)
        if self.parent is None:
            print('[{}]@{}:\n\t{}'.format(topic, self.path, msg))
            

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def remove_child(self, child):
        self.children.remove(child)
        child.parent = None

    def attach(self, other):
        '''Attach two buses. Will decide who is the parent and who is
        the child'''
        parent = self
        child = other
        if self.parent and other.parent:
            msg = '{} Unable to attach to {}, both already have parents'
            self.broadcast('bus.error', msg.format(self, other))
            other.broadcast('bus.error', msg.format(other, self))
            return
        elif self in other.lineage or other in self.lineage:
            msg = '{} and {} are already attached.'
            self.broadcast('bus.error', msg.format(self, other))
            return
        elif not self.parent and not other.parent:
            if self.child_count < other.child_count:
                parent, child = child, parent
            self.broadcast(
                'bus.debug',
                'Root {} has more children than root {}', parent, child)
        elif not other.parent:
            self.broadcast('bus.debug', '{} has no parent', other)
        elif not self.parent:
            parent, child = child, parent
            self.broadcast('bus.debug', '{} has no parent', self)
        else:
            self.broadcast('bus.error', "This shouldn't happen!")

        parent.add_child(child)
        self.broadcast(
            'bus.info', '{} is now a child of {}', child, parent)

    def detach(self, other):
        '''Detach this Bus from its parent'''
        if other is self.parent:
            other.remove_child(self)
        elif other in self.children:
            self.remove_child(other)
        else:
            self.broadcast(
                'error.bus',
                'Unable to detach {.name} and {.name}: neither is a parent of '
                'the other'.format(self, other))

    def __repr__(self):
        return 'Bus({.path})'.format(self)


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

        self.weight = 50
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


class AmmoPort32mm:
    pass

class PowerPort:
    pass

class CoolingPort:
    pass


class Attachment:
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


class Terminal:
    def __init__(self):
        self.buses = {
            'A': None,
            'B': None,
            'C': None,
        }

    def connect(self, bus):
        for key, value in self.probes.iteritems():
            if value is None:
                self.buses[key] = bus
                bus.subscribe('*')

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
    terminal.broadcast('gun.fire', {'times': 1})
    


if __name__ == '__main__':
    main()



import cmd
import uuid
import pathlib
from collections import namedtuple
from io import StringIO


BusMessage = namedtuple('BusMessage', 'topic message sender size')

def basic_subscriber(msg):
    '''Simple subscriber that just prints out the message received'''
    print('[{}]@{}:\n\t{}'.format(msg.topic, msg.sender, msg.message))


def is_prefix(a, b):
    '''Returns whether a is a prefix of path b'''
    return b.as_posix().startswith(a.as_posix())


class Bus:
    '''Data connections between components.'''

    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4()
        self.parent = None
        self.children = []
        self.subscribers = {}

    def subscribe(self, topic_filter, subscriber):
        '''Adds a subscriber. Any time a message comes through this
        Bus, if the topic_filter matches the topic, the subscriber
        will be called with the message'''
        self.subscribers[topic_filter] = subscriber

    @property
    def child_count(self):
        return sum(1 + child.child_count for child in self.children)

    @property
    def lineage(self):
        '''Returns a list of all ancestor Buses up with the last
        element being the root'''
        obj = self
        while obj.parent:
            yield obj.parent
            obj = obj.parent

    @property
    def path(self):
        '''Returns the path of the current bus in the hierarchy'''
        path = pathlib.PurePosixPath(self.name)
        for ancestor in self.lineage:
            path = ancestor.name / path
        return path

    def _push(self, msg):
        '''Rebroadcast to parents and children and notify any
        interested subscribers. This method is called by others.

        Rules:
        1. Only send to a parent if you're a prefix of the sender
        2. Only send to children who are not a prefix of the sender

        '''
        #send to subscribers
        for topic_filter, subscriber in self.subscribers.items():
            if msg.topic.startswith(topic_filter):
                subscriber(msg)

        # broadcast to children
        for child in self.children:
            if not is_prefix(child.path, msg.sender):
                child._push(msg)

        # broadcast to parents
        if self.parent is not None and is_prefix(self.path, msg.sender):
            self.parent._push(msg)

    def broadcast(self, topic, fmt, *args, **kwargs):
        msg = fmt.format(*args, **kwargs)
        bus_msg = BusMessage(topic, msg, self.path, size=0)
        self._push(bus_msg)

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

def bus_test():
    '''Shows how Buses can be attached, and subscribers put in'''
    a, b, c, d, e, f, g = (Bus(x) for x in 'abcdefg')
    a.attach(b)
    b.attach(c)
    b.attach(d)
    e.attach(f)
    e.attach(g)
    a.attach(e)
    print('All the bus paths:')
    print(a, b, c, d, e, f, g)
    a.subscribe('cabling.error', basic_subscriber)
    a.subscribe('cabling.info', basic_subscriber)
    g.broadcast('cabling.error.abort', 'This bus got aborted!') # should print
    f.broadcast('cabling.info.uhok', 'I have a message') # should print
    f.broadcast('some.other.topic', 'This should not print') # should not print
    # Second round to ensure everyone gets the message
    def super_sub(node):
        def subscriber(msg):
            print('{} got a message from {}:\n\t{}'.format(
                node, msg.sender, msg.message))
        return subscriber

    a.subscribers.clear()
    a.subscribe('', super_sub(a))
    b.subscribe('', super_sub(b))
    c.subscribe('', super_sub(c))
    d.subscribe('', super_sub(d))
    e.subscribe('', super_sub(e))
    f.subscribe('', super_sub(f))
    g.subscribe('', super_sub(g))
    g.broadcast('big.topic', 'I heard this!')



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

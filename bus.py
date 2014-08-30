'''Contains the Bus class and related functions'''

from collections import namedtuple
import pathlib
import uuid


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

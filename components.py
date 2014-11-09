'''Contains components and the component superclass'''

import uuid

import bus
from common import caps_to_hyphens, letterer


class ComponentMeta(type):
    '''Adds the counter to each class independently on creation'''

    def __new__(metacls, classname, parents, attributes):
        # This ensures each Component subclass has its own counter
        attributes['_counter'] = 0
        if 'shop_name' not in attributes:
            attributes['shop_name'] = caps_to_hyphens(classname)
        return super().__new__(metacls, classname, parents, attributes)


class Component(metaclass=ComponentMeta):
    '''All components should subclass this'''

    @classmethod
    def _make_name(cls):
        '''Called only once in the constructor to create a component's
        name'''
        number = cls._counter
        cls._counter += 1
        return '{}-{}'.format(cls.shop_name, letterer(number).upper())

    def __str__(self):
        return self.name

    def __repr__(self):
        args = ('{}={!r}'.format(k, v)
                for k, v in sorted(self.__dict__.items())
                if k not in ('bus', 'id'))
        return '{classname}({args})'.format(
            classname=self.__class__.__name__,
            args=', '.join(args))

    def __init__(self):
        self.name = self._make_name()
        if not hasattr(self, 'mass'):
            # By default, weighs one kilogram
            self.mass = 1
        self.id = str(uuid.uuid4())
        self.bus = bus.Bus(self.name)

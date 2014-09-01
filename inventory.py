'''Player Inventory'''
from collections import Counter


class Inventory:
    '''This is the inventory. You may store and retrieve items.'''

    def __init__(self):
        self._inv = {}

    def store(self, item):
        '''Stores an item in the inventory'''
        self._inv[item.name] = item

    def retrieve(self, item_name):
        ''' Returns an item from the inventory'''
        return self._inv.get(item_name, None)

    def destroy(self, item_name):
        ''' Destroys an item from the inventory'''
        del self._inv[item_name]

    def contents(self):
        ''' Returns the full contents of the inventory'''
        return list(self._inv.keys())

    def summary_contents(self):
        '''Returns the summary contents of the inventory'''
        classes = map(type, list(self._inv.values()))
        return Counter(classes)
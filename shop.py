
class Shop:
    '''This is the shop. You may buy items presently. Later, you will
    be able to sell items.
    '''
    def __init__(self):
        self._inv = {}
        
    def add_to_inventory(self, item_type):
        '''Adds a new item type to the shop inventory'''
        self._inv[item_type.type_name] = item_type

    def buy(self, type_name):
        '''Buy an item from the store'''
        itemclass = self._inv.get(type_name)
        return itemclass if itemclass is None else itemclass()


if __name__ == '__main__':
    class Raygun:
        pass
    shop = Shop()
    shop.add_to_inventory('raygun', Raygun)

    my_raygun = shop.buy('raygun')
    print('I got:', my_raygun)

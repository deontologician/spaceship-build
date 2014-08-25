
class Shop:
    '''This is the shop. You may buy items presently. Later, you will
    be able to sell items.
    '''
    def __init__(self):
        self._inv = {}
        
    def add_to_inventory(self, type_name, item_type):
        '''Adds a new item type to the inventory'''
        self._inv[type_name] = item_type

    def buy(self, type_name):
        '''buy an item from the store'''
        return self._inv[type_name]()


if __name__ == '__main__':
    class Raygun:
        pass
    shop = Shop()
    shop.add_to_inventory('raygun', Raygun)

    my_raygun = shop.buy('raygun')
    print('I got:', my_raygun)

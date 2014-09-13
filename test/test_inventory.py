import inventory
from unittest.mock import MagicMock
from collections import Counter

def test_store_retrieve():
    fake_gun = MagicMock()
    fake_gun.name = 'fakegun'
    inv = inventory.Inventory()
    inv.store(fake_gun)
    retrieved_gun = inv.retrieve('fakegun')
    assert fake_gun is retrieved_gun

def test_not_there_retrieve():
    inv = inventory.Inventory()
    retrieved = inv.retrieve('shouldnt_be_here')
    assert retrieved is None

def test_destroy():
    inv = inventory.Inventory()
    fake_gun = MagicMock()
    fake_gun.name = 'fakegun'
    inv.store(fake_gun)
    assert inv.destroy('fakegun') is True
    retrieved = inv.retrieve('fakegun')
    assert retrieved is None

def test_destroy_nothing():
    inv = inventory.Inventory()
    assert inv.destroy('shouldnt_be_there') is False

def test_contents():
    # setup
    fake_gun = MagicMock()
    fake_gun.name = 'fakegun'
    fake_shield = MagicMock()
    fake_shield.name = 'fakeshield'
    fake_zorb = MagicMock()
    fake_zorb.name = 'fakezorb'
    inv = inventory.Inventory()
    inv.store(fake_gun)
    inv.store(fake_shield)
    inv.store(fake_zorb)

    # what's expected
    expected = ['fakegun', 'fakeshield', 'fakezorb']

    # run the test
    results = inv.contents()

    # assert
    assert sorted(results) == sorted(expected)

def test_emptyinv():
    #set up
    inv = inventory.Inventory()

    #what's expected
    expected = []

    #run the test
    results = inv.contents()

    #assert
    assert expected == results

def test_multi_contents():
    #set up
    class FakeGun:
        pass
    class FakeShield:
        pass
    fake_gun = FakeGun()
    fake_gun.name = 'fakegun'

    fake_shield = FakeShield()
    fake_shield.name = 'fakeshield'
    fake_shield2 = FakeShield()
    fake_shield2.name = 'fakershield'
    inv = inventory.Inventory()
    inv.store(fake_gun)
    inv.store(fake_shield2)
    inv.store(fake_shield)

    # what's expected
    expected = ['fakegun', 'fakershield', 'fakeshield']

    # run the test
    results = inv.contents()

    #assert
    assert sorted(results) == sorted(expected)

def test_summary_emptyinv():
    #set up
    inv = inventory.Inventory()
    expected_list = []

    #what's expected
    expected = Counter(expected_list)

    #run the test
    results = inv.summary_contents()

    #assert
    assert expected == results

def test_summary_contents():
    #set up
    class FakeGun:
        pass
    class FakeShield:
        pass
    class FakeZorb:
        pass
    fake_gun = FakeGun()
    fake_gun.name = 'fakegun'

    fake_shield = FakeShield()
    fake_shield.name = 'fakeshield'
    
    fake_zorb = FakeZorb()
    fake_zorb.name = 'fakezorb'

    inv = inventory.Inventory()
    inv.store(fake_gun)
    inv.store(fake_shield)
    inv.store(fake_zorb)

    expected_list = [fake_shield, fake_gun, fake_zorb]

    #what's expected
    expected = Counter(map(type, expected_list))

    #run the test
    results = inv.summary_contents()

    #assert
    assert expected == results

def test_multi_summary_contents_mixed():
        #set up
    class FakeGun:
        pass
    class FakeShield:
        pass
    fake_gun = FakeGun()
    fake_gun.name = 'fakegun'

    fake_shield = FakeShield()
    fake_shield.name = 'fakeshield'
    fake_shield2 = FakeShield()
    fake_shield2.name = 'fakershield'
    inv = inventory.Inventory()
    inv.store(fake_gun)
    inv.store(fake_shield2)
    inv.store(fake_shield)

    expected_list = [fake_shield, fake_shield2, fake_gun]

    #what's expected
    expected = Counter(map(type, expected_list))

    #run the test
    results = inv.summary_contents()

    #assert
    assert expected == results

def test_multi_summary_contents_same():
    #set up
    class FakeGun:
        pass
    fake_gun = FakeGun()
    fake_gun.name = 'fakegun'
    fake_gun2 = FakeGun()
    fake_gun2.name = 'fakergun'
    inv = inventory.Inventory()
    inv.store(fake_gun)
    inv.store(fake_gun2)

    #what's expected
    expected = Counter([FakeGun, FakeGun])

    #run the test
    results = inv.summary_contents()

    #assert
    assert expected == results
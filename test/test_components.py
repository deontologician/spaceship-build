'''Tests for components.py'''

from unittest.mock import MagicMock

import pytest

import components as C



@pytest.fixture
def fake_bus():
    def raise_broadcast(topic, message):
        if 'error' in topic:
            raise Exception(message)

    bus = MagicMock(name='fakebus')
    bus.broadcast = raise_broadcast


def test_components():
    class FakeComponent(C.Component):
        def __init__(self, attr):
            self.attr = attr
            super().__init__()

    inst_a = FakeComponent(1)
    inst_b = FakeComponent(2)

    assert inst_a.name == 'fake-component-A'
    assert inst_b.name == 'fake-component-B'
    assert FakeComponent._counter == 2
    assert FakeComponent.shop_name == 'fake-component'
    assert inst_a.mass == 1
    assert inst_b.mass == 1
    assert len(inst_a.id) == len(inst_b.id)
    expected = "FakeComponent(attr=1, mass=1, name='fake-component-A')"
    assert repr(inst_a) == expected

# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

from .mock import MockEvent

##__________________________________________________________________||
def test_setattr_same_object():
    obj = MockEvent()
    var1 = [ ]
    obj.var1 = var1
    obj.var1 = var1

def test_setattr_different_objects():
    obj = MockEvent()
    obj.var1 = [ ]
    with pytest.raises(ValueError):
        obj.var1 = [ ]

def test_getattr():
    obj = MockEvent()
    var1 = [ ]
    obj.var1 = var1
    assert obj.var1 is var1

##__________________________________________________________________||

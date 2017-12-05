# Tai Sakuma <tai.sakuma@gmail.com>

import pytest

from scribblers.selection import ObjectSelection
from scribblers.obj import Object
from .mock import MockEvent

##__________________________________________________________________||
class MockSelection():
    def __init__(self):
        self.is_begin_called = False
        self.is_end_called = False

    def begin(self, event):
        self.is_begin_called = True

    def __call__(self, obj):
        return obj.pt >= 40

    def end(self):
        self.is_end_called = True

##__________________________________________________________________||
@pytest.fixture()
def obj():
    selection = MockSelection()

    return ObjectSelection(
        in_obj = 'Jet',
        out_obj = 'JetSelected',
        selection = selection
    )

@pytest.fixture()
def event():
    event = MockEvent()
    event.Jet = [ ]
    return event

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_begin(obj, event):

    assert not obj.selection.is_begin_called

    obj.begin(event)
    assert event.JetSelected == [ ]
    assert obj.selection.is_begin_called

def test_end(obj, event):

    obj.begin(event)
    assert not obj.selection.is_end_called
    assert obj.out is not None

    obj.end()
    assert obj.selection.is_end_called
    assert obj.out is None

def test_event(obj, event):

    obj.begin(event)

    in_obj = [Object((('pt', 50), )), Object((('pt', 45), )), Object((('pt', 20), ))]
    event.Jet[:] = in_obj

    obj.event(event)
    assert event.JetSelected == [Object((('pt', 50), )), Object((('pt', 45), ))]
    assert event.JetSelected[0] is in_obj[0] # not a copy
    assert event.JetSelected[1] is in_obj[1] # not a copy

##__________________________________________________________________||

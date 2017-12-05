# Tai Sakuma <tai.sakuma@gmail.com>

import pytest

import copy

from scribblers.correction import ObjectCorrection
from scribblers.obj import Object
from .mock import MockEvent

##__________________________________________________________________||
class MockCorrection():
    def __init__(self):
        self.is_begin_called = False
        self.is_end_called = False

    def begin(self, event):
        self.is_begin_called = True

    def __call__(self, obj):
        ret = copy.copy(obj)
        ret.pt = obj.pt*2
        return ret

    def end(self):
        self.is_end_called = True

##__________________________________________________________________||
@pytest.fixture()
def correction():
    return MockCorrection()

@pytest.fixture()
def obj(correction):
    return ObjectCorrection(
        in_obj = 'Jet',
        out_obj = 'JetCorrected',
        correction = correction
    )

@pytest.fixture()
def event():
    event = MockEvent()
    event.Jet = [ ]
    return event

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_begin(obj, correction, event):

    assert not correction.is_begin_called

    obj.begin(event)
    assert event.JetCorrected == [ ]
    assert correction.is_begin_called

def test_end(obj, correction, event):

    obj.begin(event)

    assert not correction.is_end_called
    assert obj.out is not None

    obj.end()
    assert correction.is_end_called
    assert obj.out is None

def test_event(obj, correction, event):

    obj.begin(event)

    in_obj = [Object((('pt', 50), ('eta', 1.2))), Object((('pt', 45), ('eta', 1.5) )), Object((('pt', 20), ('eta', -0.2) ))]
    event.Jet[:] = in_obj

    obj.event(event)
    assert event.JetCorrected == [Object((('pt', 100), ('eta', 1.2))), Object((('pt', 90), ('eta', 1.5) )), Object((('pt', 40), ('eta', -0.2) ))]
    assert event.Jet == [Object((('pt', 50), ('eta', 1.2))), Object((('pt', 45), ('eta', 1.5) )), Object((('pt', 20), ('eta', -0.2) ))]

##__________________________________________________________________||

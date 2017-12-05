# Tai Sakuma <tai.sakuma@gmail.com>

import pytest
import numpy as np

from scribblers.essentials import FuncOnNumpyArrays
from scribblers.obj import Object
from .mock import MockEvent

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return FuncOnNumpyArrays(
        src_arrays = ['mht', 'met'],
        out_name = 'mhtOverMet',
        func = np.divide
    )

@pytest.fixture()
def event():
    event = MockEvent()
    event.mht = [ ]
    event.met = [ ]
    return event

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_begin(obj, event):
    obj.begin(event)
    assert event.mhtOverMet == [ ]

def test_event(obj, event):

    obj.begin(event)

    event.mht[:] = [25]
    event.met[:] = [12]
    obj.event(event)
    assert event.mhtOverMet == [pytest.approx(2.083333)]

def test_end(obj, event):
    obj.begin(event)
    assert obj.func is not None

    obj.end()
    assert obj.func is None

##__________________________________________________________________||

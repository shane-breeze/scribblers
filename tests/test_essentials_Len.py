# Tai Sakuma <tai.sakuma@gmail.com>

import pytest

from scribblers.essentials import Len
from scribblers.obj import Object
from .mock import MockEvent

##__________________________________________________________________||
class MockTClonesArray(object):
    def __init__(self):
        self.len = 0

    def GetEntriesFast(self):
        return self.len

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return Len(
        src_name = 'Jet',
        out_name = 'nJet'
    )

@pytest.fixture()
def jet_tclonesarray():
    return MockTClonesArray()

@pytest.fixture()
def event(jet_tclonesarray):
    event = MockEvent()
    event.Jet = [ ]
    event.JetTClonesArray = jet_tclonesarray
    return event

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_begin(obj, event):
    obj.begin(event)
    assert event.nJet== [ ]

def test_event(obj, event):

    obj.begin(event)

    event.Jet[:] = [
        Object([('Pt', 40.0), ('Eta', 1.1), ('Phi', 0.1)]),
        Object([('Pt', 30.0), ('Eta', 2.1), ('Phi', 0.2)]),
        Object([('Pt', 20.0), ('Eta', 3.1), ('Phi', 0.3)]),
    ]
    obj.event(event)
    assert event.nJet == [3]

def test_event_tclonesarray(event, jet_tclonesarray):

    obj = Len(
        src_name = 'JetTClonesArray',
        out_name = 'nJetTClonesArray'
    )

    obj.begin(event)

    jet_tclonesarray.len = 43
    obj.event(event)
    assert event.nJetTClonesArray == [43]

##__________________________________________________________________||

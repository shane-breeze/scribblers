# Tai Sakuma <tai.sakuma@gmail.com>

import pytest

from scribblers.obj import Flatten
from scribblers.obj import Object
from .mock import MockEvent

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return Flatten(
        in_obj = 'Jet',
        in_attr_names = ['Pt', 'Eta', 'Phi'],
        out_array_prefix = 'jet',
        out_array_names = ['pt', 'eta', 'phi']
    )

@pytest.fixture()
def event():
    event = MockEvent()
    event.Jet = [ ]
    return event

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_init_raise():
    with pytest.raises(ValueError):
        Flatten(
            in_obj = 'Jet',
            in_attr_names = ['Pt', 'Eta', 'Phi'],
            out_array_prefix = 'jet',
            out_array_names = ['pt', 'eta'] # not the same length as in_array_names
        )

def test_begin(obj, event):
    obj.begin(event)
    assert event.jet_pt == [ ]
    assert event.jet_eta == [ ]
    assert event.jet_phi == [ ]

def test_begin_empty_names(event):

    obj = Flatten(
        in_obj = 'Jet',
        in_attr_names = [ ], # empty
        out_array_prefix = 'jet'
    )

    obj.begin(event)

def test_event(obj, event):

    obj.begin(event)

    event.Jet[:] = [
        Object([('Pt', 40.0), ('Eta', 1.1), ('Phi', 0.1)]),
        Object([('Pt', 30.0), ('Eta', 2.1), ('Phi', 0.2)]),
        Object([('Pt', 20.0), ('Eta', 3.1), ('Phi', 0.3)]),
    ]
    obj.event(event)
    assert event.jet_pt == [40.0, 30.0, 20.0]
    assert event.jet_eta == [1.1, 2.1, 3.1]
    assert event.jet_phi == [0.1, 0.2, 0.3]

def test_event_empty(obj, event):

    obj.begin(event)

    event.Jet[:] = [ ]
    obj.event(event)
    assert event.jet_pt == [ ]
    assert event.jet_eta == [ ]
    assert event.jet_phi == [ ]

def test_event_empty_after_non_empty(obj, event):

    obj.begin(event)

    event.Jet[:] = [
        Object([('Pt', 40.0), ('Eta', 1.1), ('Phi', 0.1)]),
        Object([('Pt', 30.0), ('Eta', 2.1), ('Phi', 0.2)]),
        Object([('Pt', 20.0), ('Eta', 3.1), ('Phi', 0.3)]),
    ]
    obj.event(event)
    assert event.jet_pt == [40.0, 30.0, 20.0]
    assert event.jet_eta == [1.1, 2.1, 3.1]
    assert event.jet_phi == [0.1, 0.2, 0.3]

    event.Jet[:] = [ ]
    obj.event(event)
    assert event.jet_pt == [ ]
    assert event.jet_eta == [ ]
    assert event.jet_phi == [ ]

def test_end(obj, event):

    obj.begin(event)
    assert obj.out_arrays is not None
    assert obj.zipped_out_arrays is not None

    obj.end()
    assert obj.out_arrays is None
    assert obj.zipped_out_arrays is None

##__________________________________________________________________||

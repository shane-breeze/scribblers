# Tai Sakuma <tai.sakuma@gmail.com>

import pytest

from scribblers.heppy import ArraysIntoObjectZip
from scribblers.obj import Object
from .mock import MockEvent

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return ArraysIntoObjectZip(
        in_array_prefix = 'jet',
        in_array_names = ['pt', 'eta', 'phi'],
        out_obj = 'Jet',
        out_attr_names = ['Pt', 'Eta', 'Phi']
        )

@pytest.fixture()
def event():
    event = MockEvent()
    event.jet_pt = [ ]
    event.jet_eta = [ ]
    event.jet_phi = [ ]
    return event

##__________________________________________________________________||
def test_repr(obj, event):
    repr(obj)

def test_init_raise():
    with pytest.raises(ValueError):
        ArraysIntoObjectZip(
            in_array_prefix = 'jet',
            in_array_names = ['pt', 'eta', 'phi'],
            out_obj = 'Jet',
            out_attr_names = ['Pt', 'Eta'] # not the same length as in_array_names
        )

def test_begin(obj, event):
    obj.begin(event)
    expected = [ ]
    assert event.Jet == expected

def test_event(obj, event):

    obj.begin(event)

    event.jet_pt[:] = [40.0, 30.0, 20.0]
    event.jet_eta[:] = [1.1, 2.1, 3.1]
    event.jet_phi[:] = [0.1, 0.2, 0.3]
    obj.event(event)
    expected = [
        Object([('Pt', 40.0), ('Eta', 1.1), ('Phi', 0.1)]),
        Object([('Pt', 30.0), ('Eta', 2.1), ('Phi', 0.2)]),
        Object([('Pt', 20.0), ('Eta', 3.1), ('Phi', 0.3)]),
    ]
    assert event.Jet == expected

def test_event_default_out_obj(event):

    obj = ArraysIntoObjectZip(
        in_array_prefix = 'jet',
        in_array_names = ['pt', 'eta', 'phi'],
        # out_obj = 'Jet',
        out_attr_names = ['Pt', 'Eta', 'Phi']
    )

    obj.begin(event)

    event.jet_pt[:] = [40.0, 30.0, 20.0]
    event.jet_eta[:] = [1.1, 2.1, 3.1]
    event.jet_phi[:] = [0.1, 0.2, 0.3]
    obj.event(event)
    expected = [
        Object([('Pt', 40.0), ('Eta', 1.1), ('Phi', 0.1)]),
        Object([('Pt', 30.0), ('Eta', 2.1), ('Phi', 0.2)]),
        Object([('Pt', 20.0), ('Eta', 3.1), ('Phi', 0.3)]),
    ]
    assert event.jet == expected

def test_event_default_out_obj_attr_names(event):

    obj = ArraysIntoObjectZip(
        in_array_prefix = 'jet',
        in_array_names = ['pt', 'eta', 'phi'],
    )

    obj.begin(event)

    event.jet_pt[:] = [40.0, 30.0, 20.0]
    event.jet_eta[:] = [1.1, 2.1, 3.1]
    event.jet_phi[:] = [0.1, 0.2, 0.3]
    obj.event(event)
    expected = [
        Object([('pt', 40.0), ('eta', 1.1), ('phi', 0.1)]),
        Object([('pt', 30.0), ('eta', 2.1), ('phi', 0.2)]),
        Object([('pt', 20.0), ('eta', 3.1), ('phi', 0.3)]),
    ]
    assert event.jet == expected

def test_event_empty_arrays(obj, event):

    obj.begin(event)

    event.jet_pt[:] = [ ] # empty
    event.jet_eta[:] = [ ] # empty
    event.jet_phi[:] = [ ] # empty
    obj.event(event)
    expected = [ ]
    assert event.Jet == expected

def test_event_empty_names(event):

    obj = ArraysIntoObjectZip(
        in_array_prefix = 'jet',
        in_array_names = [ ], # empty
    )

    obj.begin(event)

    obj.event(event)
    expected = [ ]
    assert event.jet == expected

def test_end(obj, event):

    obj.begin(event)
    assert obj.out is not None
    obj.end()
    assert obj.out is None

##__________________________________________________________________||

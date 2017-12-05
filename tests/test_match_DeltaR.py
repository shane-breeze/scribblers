# Tai Sakuma <tai.sakuma@gmail.com>

import pytest

import math

from scribblers.match import DeltaR
from scribblers.obj import Object

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return DeltaR(
        obj1_eta_phi_names = ('eta', 'phi'),
        obj2_eta_phi_names = ('eta', 'phi')
    )

def test_repr(obj):
    repr(obj)

def test_call(obj):
    o1 = Object((('eta', 0), ('phi', 0)))
    o2 = Object((('eta', 0), ('phi', 0)))
    assert obj(o1, o2) == 0.0

    o1 = Object((('eta', 0.5), ('phi', 0.5)))
    o2 = Object((('eta', 0), ('phi', 0)))
    assert obj(o1, o2) == math.sqrt(0.5**2 + 0.5**2)

def test_call_exactly_multiple_2pi(obj):

    o1 = Object((('eta', 0), ('phi', 0)))
    o2 = Object((('eta', 0), ('phi', 2*math.pi)))
    assert obj(o1, o2) == 0.0

    o1 = Object((('eta', 0), ('phi', 0)))
    o2 = Object((('eta', 0), ('phi', 4*math.pi)))
    assert obj(o1, o2) == 0.0

    o1 = Object((('eta', 0), ('phi', 2*math.pi)))
    o2 = Object((('eta', 0), ('phi', 0)))
    assert obj(o1, o2) == 0.0

    o1 = Object((('eta', 0), ('phi', 4*math.pi)))
    o2 = Object((('eta', 0), ('phi', 0)))
    assert obj(o1, o2) == 0.0

##__________________________________________________________________||

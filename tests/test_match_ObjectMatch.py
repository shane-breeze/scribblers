# Tai Sakuma <tai.sakuma@gmail.com>

import pytest

import math

from scribblers.match import ObjectMatch, DeltaR
from scribblers.obj import Object
from .mock import MockEvent

##__________________________________________________________________||
class MockDistance(object):
    def __init__(self):
        pass

    def __repr__(self):
        name_value_pairs = (
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def __call__(self, obj1, obj2):
        return math.hypot(obj1.x - obj2.x, obj1.y - obj2.y)

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return ObjectMatch(
        in_obj1 = 'A',
        in_obj2 = 'B',
        out_obj1_matched = 'Amatched',
        out_obj2_matched_sorted = 'BmatchedSorted',
        out_obj1_unmatched = 'Aunmatched',
        out_obj2_unmatched = 'Bunmatched',
        distance_func = MockDistance(),
        max_distance = 2
    )

@pytest.fixture()
def event():
    event = MockEvent()
    event.A = [ ]
    event.B = [ ]
    return event

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_begin(obj, event):

    obj.begin(event)
    assert event.Amatched == [ ]
    assert event.BmatchedSorted == [ ]
    assert event.Aunmatched == [ ]
    assert event.Bunmatched == [ ]

def test_end(obj, event):

    obj.begin(event)
    obj.end()
    assert obj.obj1_matched is None
    assert obj.obj2_matched_sorted is None
    assert obj.obj1_unmatched is None
    assert obj.obj2_unmatched is None

def test_event_simple(obj, event):

    obj.begin(event)

    a1 = Object((('x', 0), ('y', 0)))
    a2 = Object((('x', 3), ('y', 0)))
    a3 = Object((('x', 6), ('y', 0)))
    a4 = Object((('x', 9), ('y', 0)))
    b1 = Object((('x', 13), ('y', 0)))
    b2 = Object((('x', 6.5), ('y', 0)))
    b3 = Object((('x', 5), ('y', 0)))
    b4 = Object((('x', 2), ('y', 0)))
    b5 = Object((('x', 1), ('y', 0)))

    event.A[:] = [a1, a2, a3, a4]
    event.B[:] = [b1, b2, b3, b4, b5]
    obj.event(event)

    assert event.Amatched == [a1, a2, a3]
    assert event.BmatchedSorted == [b5, b4, b2]
    assert event.Aunmatched == [a4]
    assert event.Bunmatched == [b1, b3]

def test_match_empty_AB(obj):

    A = [ ]
    B = [ ]
    Amatched, BmatchedSorted, Aunmatched, Bunmatched = obj._match(A, B)

    assert len(Amatched) == 0
    assert len(BmatchedSorted) == 0
    assert len(Aunmatched) == 0
    assert len(Bunmatched) == 0

def test_match_empty_A(obj):

    o1 = Object((('x', 0), ('y', 0)))
    o2 = Object((('x', 1), ('y', 0)))

    A = [ ]
    B = [o1, o2]
    Amatched, BmatchedSorted, Aunmatched, Bunmatched = obj._match(A, B)

    assert Amatched == [ ]
    assert BmatchedSorted == [ ]
    assert Aunmatched == [ ]
    assert Bunmatched == [o1, o2]

def test_match_empty_B(obj):

    o1 = Object((('x', 0), ('y', 0)))
    o2 = Object((('x', 1), ('y', 0)))

    A = [o1, o2]
    B = [ ]
    Amatched, BmatchedSorted, Aunmatched, Bunmatched = obj._match(A, B)

    assert Amatched == [ ]
    assert BmatchedSorted == [ ]
    assert Aunmatched == [o1, o2]
    assert Bunmatched == [ ]

def test_match_simple(obj):

    a1 = Object((('x', 0), ('y', 0)))
    a2 = Object((('x', 0), ('y', 3)))
    b1 = Object((('x', 1), ('y', 0)))
    b2 = Object((('x', 3), ('y', 0)))

    A = [a1, a2]
    B = [b1, b2]
    Amatched, BmatchedSorted, Aunmatched, Bunmatched = obj._match(A, B)

    assert Amatched == [a1]
    assert BmatchedSorted == [b1]
    assert Aunmatched == [a2]
    assert Bunmatched == [b2]

def test_match_2A_within_distance(obj):

    a1 = Object((('x', 0), ('y', 0)))
    a2 = Object((('x', 1.5), ('y', 0)))
    b1 = Object((('x', 1), ('y', 0)))
    b2 = Object((('x', 5), ('y', 0)))

    A = [a1, a2]
    B = [b1, b2]
    Amatched, BmatchedSorted, Aunmatched, Bunmatched = obj._match(A, B)

    assert Amatched == [a2]
    assert BmatchedSorted == [b1]
    assert Aunmatched == [a1]
    assert Bunmatched == [b2]

def test_match_2B_within_distance(obj):

    a1 = Object((('x', 0), ('y', 0)))
    a2 = Object((('x', 5), ('y', 0)))
    b1 = Object((('x', 1), ('y', 0)))
    b2 = Object((('x', 1.5), ('y', 0)))

    A = [a1, a2]
    B = [b1, b2]
    Amatched, BmatchedSorted, Aunmatched, Bunmatched = obj._match(A, B)

    assert Amatched == [a1]
    assert BmatchedSorted == [b1]
    assert Aunmatched == [a2]
    assert Bunmatched == [b2]

##__________________________________________________________________||

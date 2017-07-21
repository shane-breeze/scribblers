import unittest
import math

from ..match import ObjectMatch, DeltaR
from ..obj import Object
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
class Test_ObjectMatch(unittest.TestCase):

    def setUp(self):
        self.obj = ObjectMatch(
            in_obj1 = 'A',
            in_obj2 = 'B',
            out_obj1_matched = 'Amatched',
            out_obj2_matched_sorted = 'BmatchedSorted',
            out_obj1_unmatched = 'Aunmatched',
            out_obj2_unmatched = 'Bunmatched',
            distance_func = MockDistance(),
            max_distance = 2
        )

        self.event = MockEvent()
        self.event.A = [ ]
        self.event.B = [ ]

    def tearDown(self):
        pass

    def test_repr(self):
        repr(self.obj)

    def test_begin(self):

        obj = self.obj
        event = self.event

        obj.begin(event)
        self.assertEqual([ ], event.Amatched)
        self.assertEqual([ ], event.BmatchedSorted)
        self.assertEqual([ ], event.Aunmatched)
        self.assertEqual([ ], event.Bunmatched)

    def test_end(self):

        obj = self.obj
        event = self.event

        obj.begin(event)
        obj.end()
        self.assertIsNone(obj.obj1_matched)
        self.assertIsNone(obj.obj2_matched_sorted)
        self.assertIsNone(obj.obj1_unmatched)
        self.assertIsNone(obj.obj2_unmatched)

    def test_event_empty_AB(self):

        obj = self.obj
        event = self.event

        obj.begin(event)

        self.event.A[:] = [ ]
        self.event.B[:] = [ ]
        obj.event(event)

        self.assertEqual(0, len(event.Amatched))
        self.assertEqual(0, len(event.BmatchedSorted))
        self.assertEqual(0, len(event.Aunmatched))
        self.assertEqual(0, len(event.Bunmatched))

    def test_event_empty_A(self):

        obj = self.obj
        event = self.event

        obj.begin(event)

        o1 = Object((('x', 0), ('y', 0)))
        o2 = Object((('x', 1), ('y', 0)))

        self.event.A[:] = [ ]
        self.event.B[:] = [o1, o2]
        obj.event(event)

        self.assertEqual([ ], event.Amatched)
        self.assertEqual([ ], event.BmatchedSorted)
        self.assertEqual([ ], event.Aunmatched)
        self.assertEqual([o1, o2], event.Bunmatched)

    def test_event_empty_B(self):

        obj = self.obj
        event = self.event

        obj.begin(event)

        o1 = Object((('x', 0), ('y', 0)))
        o2 = Object((('x', 1), ('y', 0)))

        self.event.A[:] = [o1, o2]
        self.event.B[:] = [ ]
        obj.event(event)

        self.assertEqual([ ], event.Amatched)
        self.assertEqual([ ], event.BmatchedSorted)
        self.assertEqual([o1, o2], event.Aunmatched)
        self.assertEqual([ ], event.Bunmatched)

    def test_event_simple(self):

        obj = self.obj
        event = self.event

        obj.begin(event)

        a1 = Object((('x', 0), ('y', 0)))
        a2 = Object((('x', 0), ('y', 3)))
        b1 = Object((('x', 1), ('y', 0)))
        b2 = Object((('x', 3), ('y', 0)))

        self.event.A[:] = [a1, a2]
        self.event.B[:] = [b1, b2]
        obj.event(event)

        self.assertEqual([a1], event.Amatched)
        self.assertEqual([b1], event.BmatchedSorted)
        self.assertEqual([a2], event.Aunmatched)
        self.assertEqual([b2], event.Bunmatched)

    def test_event_2A_within_distance(self):

        obj = self.obj
        event = self.event

        obj.begin(event)

        a1 = Object((('x', 0), ('y', 0)))
        a2 = Object((('x', 1.5), ('y', 0)))
        b1 = Object((('x', 1), ('y', 0)))
        b2 = Object((('x', 5), ('y', 0)))

        self.event.A[:] = [a1, a2]
        self.event.B[:] = [b1, b2]
        obj.event(event)

        self.assertEqual([a2], event.Amatched)
        self.assertEqual([b1], event.BmatchedSorted)
        self.assertEqual([a1], event.Aunmatched)
        self.assertEqual([b2], event.Bunmatched)

    def test_event_2B_within_distance(self):

        obj = self.obj
        event = self.event

        obj.begin(event)

        a1 = Object((('x', 0), ('y', 0)))
        a2 = Object((('x', 5), ('y', 0)))
        b1 = Object((('x', 1), ('y', 0)))
        b2 = Object((('x', 1.5), ('y', 0)))

        self.event.A[:] = [a1, a2]
        self.event.B[:] = [b1, b2]
        obj.event(event)

        self.assertEqual([a1], event.Amatched)
        self.assertEqual([b1], event.BmatchedSorted)
        self.assertEqual([a2], event.Aunmatched)
        self.assertEqual([b2], event.Bunmatched)

##__________________________________________________________________||

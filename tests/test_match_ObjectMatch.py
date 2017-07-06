import unittest

from ..match import ObjectMatch, DeltaR
from ..obj import Object
from .mock import MockEvent

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
            distance_func = DeltaR(obj1_eta_phi_names = ('eta', 'phi'), obj2_eta_phi_names = ('eta', 'phi')),
            max_distance = 0.4
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

    def test_event(self):

        obj = self.obj
        event = self.event

        obj.begin(event)

        self.event.A[:] = [ ]
        self.event.B[:] = [ ]
        obj.event(event)

##__________________________________________________________________||

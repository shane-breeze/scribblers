import unittest

from ..obj import Flatten
from ..obj import Object
from .mock import MockEvent

##__________________________________________________________________||
class Test_Flatten(unittest.TestCase):

    def setUp(self):
        self.obj = Flatten(
            in_obj = 'Jet',
            in_attr_names = ['Pt', 'Eta', 'Phi'],
            out_array_prefix = 'jet',
            out_array_names = ['pt', 'eta', 'phi']
        )
        self.event = MockEvent()
        self.event.Jet = [ ]

    def tearDown(self):
        pass

    def test_repr(self):
        repr(self.obj)

    def test_init_raise(self):
        self.assertRaises(
            ValueError,
            Flatten,
            in_obj = 'Jet',
            in_attr_names = ['Pt', 'Eta', 'Phi'],
            out_array_prefix = 'jet',
            out_array_names = ['pt', 'eta'] # not the same length as in_array_names
        )

    def test_begin(self):

        obj = self.obj
        event = self.event

        obj.begin(event)
        self.assertEqual([ ], event.jet_pt)
        self.assertEqual([ ], event.jet_eta)
        self.assertEqual([ ], event.jet_phi)

    def test_begin_empty_names(self):

        obj = Flatten(
            in_obj = 'Jet',
            in_attr_names = [ ], # empty
            out_array_prefix = 'jet'
        )
        event = self.event

        obj.begin(event)

    def test_event(self):

        obj = self.obj
        event = self.event

        obj.begin(event)

        event.Jet[:] = [
            Object([('Pt', 40.0), ('Eta', 1.1), ('Phi', 0.1)]),
            Object([('Pt', 30.0), ('Eta', 2.1), ('Phi', 0.2)]),
            Object([('Pt', 20.0), ('Eta', 3.1), ('Phi', 0.3)]),
        ]
        obj.event(event)
        self.assertEqual([40.0, 30.0, 20.0], event.jet_pt)
        self.assertEqual([1.1, 2.1, 3.1], event.jet_eta)
        self.assertEqual([0.1, 0.2, 0.3], event.jet_phi)

    def test_event_empty(self):

        obj = self.obj
        event = self.event

        obj.begin(event)

        event.Jet[:] = [ ]
        obj.event(event)
        self.assertEqual([ ], event.jet_pt)
        self.assertEqual([ ], event.jet_eta)
        self.assertEqual([ ], event.jet_phi)

    def test_event_empty_after_non_empty(self):

        obj = self.obj
        event = self.event

        obj.begin(event)

        event.Jet[:] = [
            Object([('Pt', 40.0), ('Eta', 1.1), ('Phi', 0.1)]),
            Object([('Pt', 30.0), ('Eta', 2.1), ('Phi', 0.2)]),
            Object([('Pt', 20.0), ('Eta', 3.1), ('Phi', 0.3)]),
        ]
        obj.event(event)
        self.assertEqual([40.0, 30.0, 20.0], event.jet_pt)
        self.assertEqual([1.1, 2.1, 3.1], event.jet_eta)
        self.assertEqual([0.1, 0.2, 0.3], event.jet_phi)

        event.Jet[:] = [ ]
        obj.event(event)
        self.assertEqual([ ], event.jet_pt)
        self.assertEqual([ ], event.jet_eta)
        self.assertEqual([ ], event.jet_phi)

    def test_end(self):

        obj = self.obj
        event = self.event

        obj.begin(event)
        self.assertIsNotNone(obj.out_arrays)
        self.assertIsNotNone(obj.zipped_out_arrays)
        obj.end()
        self.assertIsNone(obj.out_arrays)
        self.assertIsNone(obj.zipped_out_arrays)

##__________________________________________________________________||

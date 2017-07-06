import unittest

from ..heppy import ArraysIntoObjectZip
from ..obj import Object
from .mock import MockEvent

##__________________________________________________________________||
class Test_ArraysIntoObjectZip(unittest.TestCase):

    def setUp(self):

        self.obj = ArraysIntoObjectZip(
            in_array_prefix = 'jet',
            in_array_names = ['pt', 'eta', 'phi'],
            out_obj = 'Jet',
            out_attr_names = ['Pt', 'Eta', 'Phi']
        )

        self.event = MockEvent()
        self.event.jet_pt = [ ]
        self.event.jet_eta = [ ]
        self.event.jet_phi = [ ]

    def tearDown(self):
        pass

    def test_repr(self):
        repr(self.obj)

    def test_init_raise(self):
        self.assertRaises(
            ValueError,
            ArraysIntoObjectZip,
            in_array_prefix = 'jet',
            in_array_names = ['pt', 'eta', 'phi'],
            out_obj = 'Jet',
            out_attr_names = ['Pt', 'Eta'] # not the same length as in_array_names
        )

    def test_begin(self):

        obj = self.obj
        event = self.event

        obj.begin(event)
        expected = [ ]
        self.assertEqual(expected, event.Jet)

    def test_event(self):

        obj = self.obj
        event = self.event

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
        self.assertEqual(expected, event.Jet)

    def test_event_default_out_obj(self):

        obj = ArraysIntoObjectZip(
            in_array_prefix = 'jet',
            in_array_names = ['pt', 'eta', 'phi'],
            # out_obj = 'Jet',
            out_attr_names = ['Pt', 'Eta', 'Phi']
        )
        event = self.event

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
        self.assertEqual(expected, event.jet)

    def test_event_default_out_obj_attr_names(self):

        obj = ArraysIntoObjectZip(
            in_array_prefix = 'jet',
            in_array_names = ['pt', 'eta', 'phi'],
        )
        event = self.event

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
        self.assertEqual(expected, event.jet)

    def test_event_empty_arrays(self):

        obj = self.obj
        event = self.event

        obj.begin(event)

        event.jet_pt[:] = [ ] # empty
        event.jet_eta[:] = [ ] # empty
        event.jet_phi[:] = [ ] # empty
        obj.event(event)
        expected = [ ]
        self.assertEqual(expected, event.Jet)

    def test_event_empty_names(self):

        obj = ArraysIntoObjectZip(
            in_array_prefix = 'jet',
            in_array_names = [ ], # empty
        )
        event = self.event

        obj.begin(event)

        obj.event(event)
        expected = [ ]
        self.assertEqual(expected, event.jet)

    def test_end(self):

        obj = self.obj
        event = self.event

        obj.begin(event)
        self.assertIsNotNone(obj.out)
        obj.end()
        self.assertIsNone(obj.out)

##__________________________________________________________________||

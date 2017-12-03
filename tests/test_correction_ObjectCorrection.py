import unittest
import copy

from scribblers.correction import ObjectCorrection
from scribblers.obj import Object
from .mock import MockEvent

##__________________________________________________________________||
class MockCorrection():
    def __init__(self):
        self.is_begin_called = False
        self.is_end_called = False

    def begin(self, event):
        self.is_begin_called = True

    def __call__(self, obj):
        ret = copy.copy(obj)
        ret.pt = obj.pt*2
        return ret

    def end(self):
        self.is_end_called = True

##__________________________________________________________________||
class Test_Object(unittest.TestCase):

    def setUp(self):
        self.correction = MockCorrection()

        self.obj = ObjectCorrection(
            in_obj = 'Jet',
            out_obj = 'JetCorrected',
            correction = self.correction
        )

        self.event = MockEvent()
        self.event.Jet = [ ]

    def tearDown(self):
        pass

    def test_repr(self):
        repr(self.obj)

    def test_begin(self):

        obj = self.obj
        event = self.event

        self.assertFalse(self.correction.is_begin_called)

        obj.begin(event)
        self.assertEqual([ ], event.JetCorrected)
        self.assertTrue(self.correction.is_begin_called)

    def test_end(self):

        obj = self.obj
        event = self.event

        obj.begin(event)

        self.assertFalse(self.correction.is_end_called)
        self.assertIsNotNone(obj.out)

        obj.end()
        self.assertTrue(self.correction.is_end_called)
        self.assertIsNone(obj.out)

    def test_event(self):

        obj = self.obj
        event = self.event

        obj.begin(event)

        in_obj = [Object((('pt', 50), ('eta', 1.2))), Object((('pt', 45), ('eta', 1.5) )), Object((('pt', 20), ('eta', -0.2) ))]
        event.Jet[:] = in_obj

        obj.event(event)
        self.assertEqual(
            [Object((('pt', 100), ('eta', 1.2))), Object((('pt', 90), ('eta', 1.5) )), Object((('pt', 40), ('eta', -0.2) ))],
            event.JetCorrected
        )
        self.assertEqual(
            [Object((('pt', 50), ('eta', 1.2))), Object((('pt', 45), ('eta', 1.5) )), Object((('pt', 20), ('eta', -0.2) ))],
            event.Jet
        )
##__________________________________________________________________||

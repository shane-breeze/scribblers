import unittest

from ..selection import ObjectSelection
from ..obj import Object
from .mock import MockEvent

##__________________________________________________________________||
class MockSelection():
    def __init__(self):
        self.is_begin_called = False
        self.is_end_called = False

    def begin(self, event):
        self.is_begin_called = True

    def __call__(self, obj):
        return obj.pt >= 40

    def end(self):
        self.is_end_called = True

##__________________________________________________________________||
class Test_Object(unittest.TestCase):

    def setUp(self):
        self.selection = MockSelection()

        self.obj = ObjectSelection(
            in_obj = 'Jet',
            out_obj = 'JetSelected',
            selection = self.selection
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

        self.assertFalse(self.selection.is_begin_called)

        obj.begin(event)
        self.assertEqual([ ], event.JetSelected)
        self.assertTrue(self.selection.is_begin_called)

    def test_end(self):

        obj = self.obj
        event = self.event

        obj.begin(event)

        self.assertFalse(self.selection.is_end_called)
        self.assertIsNotNone(obj.out)

        obj.end()
        self.assertTrue(self.selection.is_end_called)
        self.assertIsNone(obj.out)

    def test_event(self):

        obj = self.obj
        event = self.event

        obj.begin(event)

        in_obj = [Object((('pt', 50), )), Object((('pt', 45), )), Object((('pt', 20), ))]
        event.Jet[:] = in_obj

        obj.event(event)
        self.assertEqual([Object((('pt', 50), )), Object((('pt', 45), ))], event.JetSelected)
        self.assertIs(in_obj[0], event.JetSelected[0]) # not a copy
        self.assertIs(in_obj[1], event.JetSelected[1]) # not a copy

##__________________________________________________________________||

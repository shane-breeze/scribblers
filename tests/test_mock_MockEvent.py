import unittest

from .mock import MockEvent

##__________________________________________________________________||
class Test_MockEvent(unittest.TestCase):

    def test_setattr_same_object(self):
        obj = MockEvent()
        var1 = [ ]
        obj.var1 = var1
        obj.var1 = var1

    def test_setattr_different_objects(self):
        obj = MockEvent()
        obj.var1 = [ ]
        self.assertRaises(ValueError, obj.__setattr__, 'var1', [ ])

    def test_getattr(self):
        obj = MockEvent()
        var1 = [ ]
        obj.var1 = var1
        self.assertIs(var1, obj.var1)

##__________________________________________________________________||

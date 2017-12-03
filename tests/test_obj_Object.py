# Tai Sakuma <tai.sakuma@cern.ch>
import unittest
import copy

from scribblers.obj import Object

##__________________________________________________________________||
class Test_Object(unittest.TestCase):

    def setUp(self):
        self.obj = Object([('pt', 40.0), ('eta', 1.1), ('phi', 0.1)])

    def tearDown(self):
        pass

    def test_repr(self):
        repr(self.obj)

    def test_attr(self):
        self.assertEqual(40.0, self.obj.pt)
        self.assertEqual(1.1, self.obj.eta)
        self.assertEqual(0.1, self.obj.phi)

    def test_attr_raise(self):
        self.assertRaises(AttributeError, self.obj.__getattr__, 'mass')

    def test_init_no_args(self):
        Object()

    def test_init_copy(self):
        obj = Object(self.obj)
        self.assertEqual(self.obj, obj)
        self.assertIsNot(self.obj, obj)
        self.assertIsNot(self.obj._attrdict, obj._attrdict)

    def test_init_copy_extra_args(self):
        obj = Object(self.obj, 1)
        self.assertEqual(self.obj, obj)
        self.assertIsNot(self.obj, obj)
        self.assertIsNot(self.obj._attrdict, obj._attrdict)

    def test_init_copy_extra_kwargs(self):
        obj = Object(self.obj, A = 10)
        self.assertEqual(self.obj, obj)
        self.assertIsNot(self.obj, obj)
        self.assertIsNot(self.obj._attrdict, obj._attrdict)

    def test_copy(self):
        obj = copy.copy(self.obj)
        self.assertEqual(self.obj, obj)
        self.assertIsNot(self.obj, obj)
        self.assertIsNot(self.obj._attrdict, obj._attrdict)

    def test_setattr_modify(self):
        self.obj.pt = 50.0
        self.assertEqual(50.0, self.obj.pt)
        self.assertEqual(
            Object([('pt', 50.0), ('eta', 1.1), ('phi', 0.1)]),
            self.obj
            )

    def test_setattr_newattr(self):
        self.obj.mass = 15.0
        self.assertEqual(15.0, self.obj.mass)
        self.assertEqual(
            Object([('pt', 40.0), ('eta', 1.1), ('phi', 0.1), ('mass', 15.0)]),
            self.obj
            )

##__________________________________________________________________||

import unittest
import math

from ..match import DeltaR
from ..obj import Object

##__________________________________________________________________||
class Test_DeltaR(unittest.TestCase):

    def setUp(self):
        self.obj = DeltaR(
            obj1_eta_phi_names = ('eta', 'phi'),
            obj2_eta_phi_names = ('eta', 'phi')
        )

    def tearDown(self):
        pass

    def test_repr(self):
        repr(self.obj)

    def test_call(self):
        o1 = Object((('eta', 0), ('phi', 0)))
        o2 = Object((('eta', 0), ('phi', 0)))
        self.assertEqual(0.0, self.obj(o1, o2))

        o1 = Object((('eta', 0.5), ('phi', 0.5)))
        o2 = Object((('eta', 0), ('phi', 0)))
        self.assertEqual(math.sqrt(0.5**2 + 0.5**2), self.obj(o1, o2))

    def test_call_exactly_multiple_2pi(self):

        o1 = Object((('eta', 0), ('phi', 0)))
        o2 = Object((('eta', 0), ('phi', 2*math.pi)))
        self.assertEqual(0.0, self.obj(o1, o2))

        o1 = Object((('eta', 0), ('phi', 0)))
        o2 = Object((('eta', 0), ('phi', 4*math.pi)))
        self.assertEqual(0.0, self.obj(o1, o2))

        o1 = Object((('eta', 0), ('phi', 2*math.pi)))
        o2 = Object((('eta', 0), ('phi', 0)))
        self.assertEqual(0.0, self.obj(o1, o2))

        o1 = Object((('eta', 0), ('phi', 4*math.pi)))
        o2 = Object((('eta', 0), ('phi', 0)))
        self.assertEqual(0.0, self.obj(o1, o2))

##__________________________________________________________________||

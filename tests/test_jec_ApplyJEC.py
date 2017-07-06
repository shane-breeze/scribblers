import unittest

from ..jec import ApplyJEC
from ..obj import Object

##__________________________________________________________________||
class MockScaleFunc(object):
    def __init__(self):
        self.ret = 1.0
        self.args = None

    def __call__(self, pt, eta):
        self.args = (pt, eta)
        return self.ret

##__________________________________________________________________||
class Test_ApplyJEC(unittest.TestCase):

    def setUp(self):
        self.scale_func = MockScaleFunc()
        self.obj = ApplyJEC(
            scale_func_pt_eta = self.scale_func
        )

    def tearDown(self):
        pass

    def test_repr(self):
        repr(self.obj)

    def test_call(self):
        self.scale_func.ret = 48.0

        jet = Object([('pt', 40.0), ('eta', 1.1), ('phi', 0.1)])
        jet_corr = self.obj(jet)

        self.assertEqual((40.0, 1.1),  self.scale_func.args)
        self.assertEqual(
            Object([('pt', 48.0), ('eta', 1.1), ('phi', 0.1)]),
            jet_corr
        )

##__________________________________________________________________||

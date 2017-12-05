# Tai Sakuma <tai.sakuma@gmail.com>

import pytest

from scribblers.jec import ApplyJEC
from scribblers.obj import Object

##__________________________________________________________________||
class MockScaleFunc(object):
    def __init__(self):
        self.ret = 1.0
        self.args = None

    def __call__(self, pt, eta):
        self.args = (pt, eta)
        return self.ret

##__________________________________________________________________||
@pytest.fixture()
def scale_func():
    return MockScaleFunc()

@pytest.fixture()
def obj(scale_func):
    return ApplyJEC(
        scale_func_pt_eta = scale_func
    )

##__________________________________________________________________||
def test_repr(obj, scale_func):
    repr(obj)

def test_call(obj, scale_func):
    scale_func.ret = 48.0

    jet = Object([('pt', 40.0), ('eta', 1.1), ('phi', 0.1)])
    jet_corr = obj(jet)

    assert scale_func.args == (40.0, 1.1)
    assert jet_corr == Object([('pt', 48.0), ('eta', 1.1), ('phi', 0.1)])

##__________________________________________________________________||

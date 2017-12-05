# Tai Sakuma <tai.sakuma@gmail.com>

import copy
import logging
import pytest

from scribblers.obj import Object

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return Object([('pt', 40.0), ('eta', 1.1), ('phi', 0.1)])

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_attr(obj):
    assert obj.pt == 40.0
    assert obj.eta == 1.1
    assert obj.phi == 0.1

def test_attr_raise(obj):
    with pytest.raises(AttributeError):
        obj.mass

def test_init_no_args():
    Object()

def test_init_copy(obj):
    obj_copy = Object(obj)
    assert obj == obj_copy
    assert obj is not obj_copy
    assert obj._attrdict is not obj_copy._attrdict

def test_init_copy_extra_args(obj, caplog):
    with caplog.at_level(logging.INFO, logger = 'scribblers.obj'):
        obj_copy = Object(obj, 1)
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'extra arguments' in caplog.records[0].msg

    assert obj == obj_copy
    assert obj is not obj_copy
    assert obj._attrdict is not obj_copy._attrdict

def test_init_copy_extra_kwargs(obj):
    obj_copy = Object(obj, A = 10)
    assert obj == obj_copy
    assert obj is not obj_copy
    assert obj._attrdict is not obj_copy._attrdict

def test_copy(obj):
    obj_copy = copy.copy(obj)
    assert obj == obj_copy
    assert obj is not obj_copy
    assert obj._attrdict is not obj_copy._attrdict

def test_setattr_modify(obj):
    obj.pt = 50.0
    assert obj.pt == 50.0
    assert obj == Object([('pt', 50.0), ('eta', 1.1), ('phi', 0.1)])

def test_setattr_newattr(obj):
    obj.mass = 15.0
    assert obj.mass == 15.0
    assert obj == Object([('pt', 40.0), ('eta', 1.1), ('phi', 0.1), ('mass', 15.0)])

##__________________________________________________________________||

# Tai Sakuma <tai.sakuma@gmail.com>

import pytest

from scribblers.heppy import SMSMass
from .mock import MockEvent

##__________________________________________________________________||
@pytest.fixture()
def obj():
    return SMSMass()

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_begin(obj):
    event = MockEvent()
    event.componentName = ['SMS_T1tttt']
    event.GenSusyMGluino = [1800]
    event.GenSusyMNeutralino = [200]
    obj.begin(event)
    assert event.smsmass1 is event.GenSusyMGluino
    assert event.smsmass2 is event.GenSusyMNeutralino

def test_begin_massdict(obj):
    massdict = {
        'SMS-T2bb': ('GenSusyMSbottom', 'GenSusyMNeutralino'),
    }
    obj = SMSMass(massdict = massdict)

    event = MockEvent()
    event.componentName = ['SMS-T2bb_mSbottom-625to1050_0to550_25ns']
    event.GenSusyMSbottom = [1000]
    event.GenSusyMNeutralino = [200]
    obj.begin(event)
    assert event.smsmass1 is event.GenSusyMSbottom
    assert event.smsmass2 is event.GenSusyMNeutralino

##__________________________________________________________________||

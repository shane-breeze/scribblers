import unittest

from scribblers.heppy import SMSMass
from .mock import MockEvent

##__________________________________________________________________||
class Test_SMSMass(unittest.TestCase):

    def setUp(self):
        self.obj = SMSMass()

    def test_repr(self):
        repr(self.obj)

    def test_begin(self):
        event = MockEvent()
        event.componentName = ['SMS_T1tttt']
        event.GenSusyMGluino = [1800]
        event.GenSusyMNeutralino = [200]
        self.obj.begin(event)
        self.assertIs(event.GenSusyMGluino, event.smsmass1)
        self.assertIs(event.GenSusyMNeutralino, event.smsmass2)

    def test_begin_massdict(self):
        massdict = {
            'SMS-T2bb': ('GenSusyMSbottom', 'GenSusyMNeutralino'),
        }
        self.obj = SMSMass(massdict = massdict)


        event = MockEvent()
        event.componentName = ['SMS-T2bb_mSbottom-625to1050_0to550_25ns']
        event.GenSusyMSbottom = [1000]
        event.GenSusyMNeutralino = [200]
        self.obj.begin(event)
        self.assertIs(event.GenSusyMSbottom, event.smsmass1)
        self.assertIs(event.GenSusyMNeutralino, event.smsmass2)

##__________________________________________________________________||

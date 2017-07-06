import unittest

from ..heppy import SMSMass
from .mock import MockEvent

##__________________________________________________________________||
class Test_SMSMass(unittest.TestCase):

    def test_begin(self):
        obj = SMSMass()
        event = MockEvent()
        event.componentName = ['SMS_T1tttt']
        event.GenSusyMGluino = [1800]
        event.GenSusyMNeutralino = [200]
        obj.begin(event)
        self.assertIs(event.GenSusyMGluino, event.smsmass1)
        self.assertIs(event.GenSusyMNeutralino, event.smsmass2)

##__________________________________________________________________||

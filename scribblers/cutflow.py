class cutflow(object):
    def begin(self, event):
        self.addr_cutflow = [ ]
        event.cutflow = self.addr_cutflow

        self.cutflow_name_dict = {
            1: 'JetMET',
            2: 'SingleMu',
            3: 'DoubleMu',
            4: 'SingleEle',
            5: 'DoubleEle',
            6: 'SingleMuEle',
            -1: 'other',
        }

    def event(self, event):
        event.cutflow = self.addr_cutflow
        self.addr_cutflow[:] = [self.cutflow_name_dict[event.cutflowId[0]]]

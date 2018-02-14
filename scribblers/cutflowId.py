class cutflowId(object):
    def begin(self, event):
        self.addr_cutflowId = [ ]
        event.cutflowId = self.addr_cutflowId

        # (nMuoV, nEleV, nPhoV, nMuoS, nEleS, nPhoS)
        self.nObjs_cutflowId_dict = {
            (0, 0, 0, 0, 0, 0) : 1, # 'JetMET'
            (1, 0, 0, 1, 0, 0) : 2, # 'SingleMu'
            (2, 0, 0, 2, 0, 0) : 3, # 'DoubleMu'
            (0, 1, 0, 0, 1, 0) : 4, # 'SingleEle'
            (0, 2, 0, 0, 2, 0) : 5, # 'DoubleEle'
            (1, 1, 0, 1, 1, 0) : 6, # 'SingleMuEle'
            }

    def event(self, event):
        event.cutflowId = self.addr_cutflowId
        key = (
            len(event.MuonVeto),
            len(event.ElectronVeto),
            len(event.PhotonVeto),
            len(event.MuonSelection),
            len(event.ElectronSelection),
            len(event.PhotonSelection),
        )

        if key in self.nObjs_cutflowId_dict:
            cutflowId = self.nObjs_cutflowId_dict[key]
        else:
            cutflowId = -1
        self.addr_cutflowId[:] = [cutflowId]

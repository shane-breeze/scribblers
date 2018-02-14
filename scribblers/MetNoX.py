import ROOT

class MetNoX(object):
    def begin(self, event):
        self.METNoX_pt = [ ]
        self.METNoX_phi = [ ]
        self._attach_to_event(event)

        self.MET_pt = event.MET_pt
        self.MET_phi = event.MET_phi

        self.objs = event.MuonSelection \
                    + event.ElectronSelection \
                    + event.PhotonSelection

    def _attach_to_event(self, event):
        event.METNoX_pt = self.METNoX_pt
        event.METNoX_phi = self.METNoX_phi

    def event(self, event):
        self._attach_to_event(event)

        v_met = ROOT.TVector2()
        v_met.SetMagPhi(self.MET_pt[0], self.MET_phi[0])

        for obj in self.objs:
            v_obj = ROOT.TVector2()
            v_obj.SetMagPhi(obj.pt, obj.phi)
            v_met += v_obj

        self.METNoX_pt[:] = [v_met.Mod()]
        self.METNoX_phi[:] = [v_met.Phi()]

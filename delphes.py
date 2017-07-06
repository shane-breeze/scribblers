# Tai Sakuma <tai.sakuma@cern.ch>
import numpy as np

## https://cp3.irmp.ucl.ac.be/projects/delphes/wiki/WorkBook/RootTreeDescription
## http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html

##__________________________________________________________________||
class LheHT(object):

    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__,
        )

    def begin(self, event):
        self.lheHT = [ ]
        self._attach_to_event(event)

    def _attach_to_event(self, event):
        event.lheHT = self.lheHT

    def event(self, event):
        self._attach_to_event(event)

        pt = np.array(event.Particle_PT)
        status = np.array(event.Particle_Status)
        mother2 = np.array(event.Particle_M2)
        pt23 = pt[(status == 23) & (mother2 > 0)]
        self.lheHT[:] = [np.sum(pt23) if pt23.size > 0 else 0.0]

##__________________________________________________________________||
class HT(object):
    def __init__(self, src_obj, out_name, obj_pt_name = 'PT'):
        self.src_obj = src_obj
        self.out_name = out_name
        self.obj_pt_name = obj_pt_name

    def __repr__(self):
        name_value_pairs = (
            ('src_obj', self.src_obj),
            ('out_name', self.out_name),
            ('obj_pt_name', self.obj_pt_name),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def begin(self, event):
        self.out = [ ]
        self._attach_to_event(event)

    def _attach_to_event(self, event):
        setattr(event, self.out_name, self.out)

    def event(self, event):
        self._attach_to_event(event)
        self.out[:] = [sum([getattr(o, self.obj_pt_name) for o in getattr(event, self.src_obj)])]

##__________________________________________________________________||
class MHT(object):
    def __init__(self, src_obj, out_name, out_phi_name = None):
        self.src_obj = src_obj
        self.out_name = out_name
        self.out_phi_name = out_phi_name

    def __repr__(self):
        name_value_pairs = (
            ('src_obj', self.src_obj),
            ('out_name', self.out_name),
            ('out_phi_name', self.out_phi_name),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def begin(self, event):
        self.out = [ ]
        self.out_phi = [ ]
        self._attach_to_event(event)

    def _attach_to_event(self, event):
        setattr(event, self.out_name, self.out)
        if self.out_phi_name is not None:
            setattr(event, self.out_phi_name, self.out_phi)

    def event(self, event):
        self._attach_to_event(event)
        pt = np.array([o.PT for o in getattr(event, self.src_obj)])

        if pt.size == 0:
            self.out[:] = [0.0]
            return

        if pt.size == 1:
            self.out[:] = [pt[0]] # make mht and pt precisely the
            return                # same for the monojet events

        phi = np.array([o.Phi for o in getattr(event, self.src_obj)])

        px = pt*np.cos(phi)
        py = pt*np.sin(phi)

        mhtx = -np.sum(px)
        mhty = -np.sum(py)

        mht = np.sqrt(mhtx**2 + mhty**2)
        mht_phi = np.arctan2(mhty, mhtx)

        self.out[:] = [mht]
        self.out_phi[:] = [mht_phi]

##__________________________________________________________________||

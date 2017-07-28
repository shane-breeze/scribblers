# Tai Sakuma <tai.sakuma@cern.ch>
import copy
import itertools
import operator
import numpy as np

import ROOT

## https://cp3.irmp.ucl.ac.be/projects/delphes/wiki/WorkBook/RootTreeDescription
## http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html

from .match import DeltaR

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
class JetAddMatchedObjects(object):
    def __init__(self, in_obj1, in_obj2,
                 out_obj1,
                 distance_func = DeltaR(),
                 max_distance = 0.4
    ):
        self.in_obj1_name = in_obj1
        self.in_obj2_name = in_obj2
        self.out_obj1_name = out_obj1
        self.distance_func = distance_func
        self.max_distance = max_distance

    def __repr__(self):
        name_value_pairs = (
            ('in_obj1_name', self.in_obj1_name),
            ('in_obj2_name', self.in_obj2_name),
            ('out_obj1_name', self.out_obj1_name),
            ('distance_func', self.distance_func),
            ('max_distance', self.max_distance),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def begin(self, event):
        self.out_obj1 = [ ]
        self._attach_to_event(event)

    def _attach_to_event(self, event):
        setattr(event, self.out_obj1_name, self.out_obj1)

    def event(self, event):
        self._attach_to_event(event)

        obj1 = getattr(event, self.in_obj1_name)
        obj2 = getattr(event, self.in_obj2_name)

        # each obj1 can be matched to multiple obj2s
        # each obj2 can be matched to at most one obj1

        distances = [[(i1, i2, self.distance_func(o1, o2)) for i1, o1 in enumerate(obj1)] for i2, o2 in enumerate(obj2)]
        # a list of lists of (index1, index2, distance) grouped by index2
        # e.g.,
        # [
        #     [(0, 0, 13.0), (1, 0, 10.0), (2, 0, 7.0), (3, 0, 4.0)],
        #     [(0, 1, 6.5), (1, 1, 3.5), (2, 1, 0.5), (3, 1, 2.5)],
        #     [(0, 2, 5.0), (1, 2, 2.0), (2, 2, 1.0), (3, 2, 4.0)],
        #     [(0, 3, 2.0), (1, 3, 1.0), (2, 3, 4.0), (3, 3, 7.0)],
        #     [(0, 4, 1.0), (1, 4, 2.0), (2, 4, 5.0), (3, 4, 8.0)]
        # ]

        distances = [l for l in distances if l]
        # remove empty sublists

        distances = (min(l, key = operator.itemgetter(2)) for l in distances)
        # select one with the minimum distance in each sublist
        # e.g., [(3, 0, 4.0), (2, 1, 0.5), (2, 2, 1.0), (1, 3, 1.0), (0, 4, 1.0)]

        distances = (l for l in distances if l[2] <= self.max_distance)
        # remove ones with distances greater than maximum distances
        # e.g., [(2, 1, 0.5), (2, 2, 1.0), (1, 3, 1.0), (0, 4, 1.0)]
        # note index1 == 2 happens twice

        distances = sorted(distances, key = operator.itemgetter(0))
        # sort by index1
        # e.g., [(0, 4, 1.0), (1, 3, 1.0), (2, 1, 0.5), (2, 2, 1.0)]

        distances = [list(g) for _, g in itertools.groupby(distances, key = operator.itemgetter(0))]
        # group by index1
        # e.g., [[(0, 4, 1.0)], [(1, 3, 1.0)], [(2, 1, 0.5), (2, 2, 1.0)]]

        distances = {e[0][0]: [ee[1] for ee in e] for e in distances}
        # convert to dict with the key index1


        out = [ ]
        for i, o1 in enumerate(obj1):

            o1_copy = copy.copy(o1)

            if not i in distances:
                out.append(o1_copy)
                continue

            p4 = ROOT.TLorentzVector()
            p4.SetPtEtaPhiM(o1.PT, o1.Eta, o1.Phi, o1.Mass)

            o2s = [obj2[j] for j in distances[i]]

            for o2 in o2s:

                # this works only for GenParticle
                p4_ = ROOT.TLorentzVector(o2.Px, o2.Py, o2.Pz, o2.E)
                p4 += p4_

            o1_copy.PT = p4.Pt()
            o1_copy.Eta = p4.Eta()
            o1_copy.Phi = p4.Phi()
            o1_copy.Mass = p4.M()
            out.append(o1_copy)

        self.out_obj1[:] = out

    def end(self):
        self.out_obj1 = None

##__________________________________________________________________||


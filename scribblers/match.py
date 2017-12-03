# Tai Sakuma <tai.sakuma@gmail.com>
import itertools
import operator
import numpy as np

##__________________________________________________________________||
class DeltaR(object):
    def __init__(self,
                 obj1_eta_phi_names = ('eta', 'phi'),
                 obj2_eta_phi_names = ('eta', 'phi')
    ):
        self.obj1_eta_phi_names = obj1_eta_phi_names
        self.obj2_eta_phi_names = obj2_eta_phi_names

    def __repr__(self):
        name_value_pairs = (
            ('obj1_eta_phi_names', self.obj1_eta_phi_names),
            ('obj2_eta_phi_names', self.obj2_eta_phi_names),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def __call__(self, obj1, obj2):
        return self._deltaR(
            getattr(obj1, self.obj1_eta_phi_names[0]),
            getattr(obj1, self.obj1_eta_phi_names[1]),
            getattr(obj2, self.obj2_eta_phi_names[0]),
            getattr(obj2, self.obj2_eta_phi_names[1]),
        )

    def _deltaR(self, eta1, phi1, eta2, phi2):
        deta = eta1 - eta2
        dphi = self._deltaPhi(phi1, phi2)
        return np.sqrt(deta*deta + dphi*dphi)

    def _deltaPhi(self, phi1, phi2):
        ret = phi1 - phi2
        while ret >= 2*np.pi:
            ret -= 2*np.pi
        while ret <= -2*np.pi:
            ret += 2*np.pi
        return ret

##__________________________________________________________________||
class ObjectMatch(object):
    def __init__(self, in_obj1, in_obj2,
                 out_obj1_matched,
                 out_obj2_matched_sorted = None,
                 out_obj1_unmatched = None,
                 out_obj2_unmatched = None,
                 distance_func = DeltaR(),
                 max_distance = 0.4
    ):
        self.obj1_name = in_obj1
        self.obj2_name = in_obj2
        self.obj1_matched_name = out_obj1_matched
        self.obj2_matched_sorted_name = out_obj2_matched_sorted
        self.obj1_unmatched_name = out_obj1_unmatched
        self.obj2_unmatched_name = out_obj2_unmatched
        self.distance_func = distance_func
        self.max_distance = max_distance


    def __repr__(self):
        name_value_pairs = (
            ('in_obj1_name', self.obj1_name),
            ('in_obj2_name', self.obj2_name),
            ('out_obj1_matched_name', self.obj1_matched_name),
            ('out_obj2_matched_sorted_name', self.obj2_matched_sorted_name),
            ('out_obj1_unmatched_name', self.obj1_unmatched_name),
            ('out_obj2_unmatched_name', self.obj2_unmatched_name),
            ('distance_func', self.distance_func),
            ('max_distance', self.max_distance),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def begin(self, event):
        self.obj1_matched = [ ]
        self.obj2_matched_sorted = [ ]
        self.obj1_unmatched = [ ]
        self.obj2_unmatched = [ ]
        self._attach_to_event(event)

    def _attach_to_event(self, event):
        setattr(event, self.obj1_matched_name, self.obj1_matched)

        if self.obj2_matched_sorted_name is not None:
            setattr(event, self.obj2_matched_sorted_name, self.obj2_matched_sorted)

        if self.obj1_unmatched_name is not None:
            setattr(event, self.obj1_unmatched_name, self.obj1_unmatched)

        if self.obj2_unmatched_name  is not None:
            setattr(event, self.obj2_unmatched_name, self.obj2_unmatched)

    def event(self, event):
        self._attach_to_event(event)
        obj1 = getattr(event, self.obj1_name)
        obj2 = getattr(event, self.obj2_name)

        self.obj1_matched[:], self.obj2_matched_sorted[:], self.obj1_unmatched[:], self.obj2_unmatched[:] = self._match(obj1, obj2)

    def _match(self, obj1, obj2):

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

        distances = [min(l, key = operator.itemgetter(2)) for l in distances]
        # select one with the minimum distance in each sublist
        # e.g., [(0, 4, 1.0), (1, 3, 1.0), (2, 1, 0.5)]

        obj1_matched = [obj1[i] for i, j, d in distances]
        obj2_matched_sorted = [obj2[j] for i, j, d in distances]

        obj1_unmatched = [o for o in obj1 if o not in obj1_matched]
        obj2_unmatched = [o for o in obj2 if o not in obj2_matched_sorted]

        return obj1_matched, obj2_matched_sorted, obj1_unmatched, obj2_unmatched

    def end(self):
        self.obj1_matched = None
        self.obj1_unmatched = None
        self.obj2_matched_sorted = None
        self.obj2_unmatched = None

##__________________________________________________________________||

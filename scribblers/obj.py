# Tai Sakuma <tai.sakuma@gmail.com>
import collections
import logging
import copy

##__________________________________________________________________||
class Object(object):
    """a simple class to represent an object in an event, e.g., a jet, muon.

    implemented as an attribute-access ordered dictionary

    """

    def __init__(self, *args, **kwargs):

        try:
            # First, assume args[0] is another instance of this class,
            # and try to copy the contents of the instance.
            attrdict = collections.OrderedDict(args[0]._attrdict)
        except (AttributeError, IndexError):
            # Otherwise, all arguments are simply given to OrderedDict
            # so that this class can be instantiated with any
            # arguments that can instantiate OrderedDict.
            attrdict = collections.OrderedDict(*args, **kwargs)
        else:
            if len(args) > 1 or kwargs:
                logger = logging.getLogger(__name__)
                logger.warning('extra arguments are given: args = {}, kwargs = {}'.format(args[1:], kwargs))

        #object.__setattr__(self, '_attrdict', attrdict)
        self.__dict__["_attrdict"] = attrdict
        # self._attrdict = attrdict # this would cause infinite
                                    # recursion as __setattr__() is
                                    # implemented

    def __copy__(self):
        return self.__class__(self)

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(k, v) for k, v in self.__dict__["_attrdict"].items()])
        )

    def __getattr__(self, attr):
        try:
            return self.__dict__["_attrdict"][attr]
        except KeyError:
            raise AttributeError('{} has no attribute "{}"'.format(self, attr))

    def __setattr__(self, name, value):
        self.__dict__["_attrdict"][name] = value

    def __eq__(self, other):
        return self.__dict__["_attrdict"] == other.__dict__["_attrdict"]

##__________________________________________________________________||
class Flatten(object):
    """flatten a list of objects into a set of arrays

    namely, do the opposite of what ArraysIntoObjectZip does
    """
    def __init__(self,
                 in_obj, in_attr_names,
                 out_array_prefix = None, out_array_names = None
    ):

        self.in_obj = in_obj
        # e.g., 'Jet'

        self.in_attr_names = in_attr_names
        # e.g., ['Pt', 'Eta', 'Phi']

        self.out_array_prefix = out_array_prefix if out_array_prefix else in_obj
        # e.g., 'jet'

        self.out_array_names = out_array_names if out_array_names else in_attr_names
        # e.g., ['pt', 'eta', 'phi']

        if not len(self.in_attr_names) == len(self.out_array_names):
            raise ValueError('in_attr_names and out_array_names must have the same length: in_attr_names = {}, out_array_names = {}'.format(in_attr_names, out_array_names))

        self.out_names = ['{}_{}'.format(self.out_array_prefix, n) for n in self.out_array_names]
        # e.g., ['jet_pt', 'jet_eta', 'jet_phi']

    def __repr__(self):
        name_value_pairs = (
            ('in_obj',           self.in_obj),
            ('in_attr_names',    self.in_attr_names),
            ('out_array_prefix', self.out_array_prefix),
            ('out_array_names',  self.out_array_names),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def begin(self, event):

        self.out_arrays = [[ ] for _ in self.out_names]
        # e.g., [[ ], [ ], [ ]] # as many empty lists as the length of self.out_names

        self.zipped_out_arrays = zip(self.out_names, self.out_arrays)
        # e.g., [('jet_pt', []), ('jet_eta', []), ('jet_phi', [])]

        self._attach_to_event(event)

    def _attach_to_event(self, event):
        for n, a in self.zipped_out_arrays:
            setattr(event, n, a)
            # e.g., event.jet_pt = []

    def event(self, event):
        self._attach_to_event(event)

        objs = getattr(event, self.in_obj)
        # e.g., [Jet[0], Jet[1], ...]

        obj_attrs = [[getattr(o, a) for a in self.in_attr_names] for o in objs]
        # e.g., [[Jet[0].Pt, Jet[0].Eta, Jet[0].Phi],
        #        [Jet[1].Pt, Jet[1].Eta, Jet[1].Phi],
        #        ...]

        out_arrays = zip(*obj_attrs) if obj_attrs else [[ ] for _ in self.in_attr_names]
        # e.g., [[Jet[0].Pt, Jet[1].Pt, ...],
        #        [Jet[0].Eta, Jet[1].Eta, ...],
        #        [Jet[0].Phi, Jet[1].Phi, ...]]
        #
        # The else clause is necessary because otherwise when
        # obj_attrs is empty out_arrays would become an empty list,
        # i.e., [ ], which would not update self.out_arrays below.
        # That is, self.out_arrays would keep the contents of the
        # previous event. obj_attrs needs to be a list of empty lists
        # instead, e.g., [[ ], [ ], [ ]].

        for event_attr, local_array in zip(self.out_arrays, out_arrays):
            event_attr[:] = local_array
            # e.g., event.jet_pt[:] = [Jet[0].Pt, Jet[1].Pt, ...]

    def end(self):
        self.out_arrays = None
        self.zipped_out_arrays = None

##__________________________________________________________________||
class Collection(object):
    """
    Scribbler to add an object collection to the event. Each element of the
    collection is an object of the Object class
    """
    def __init__(self, obj_name, attrs=[]):
        """
        :param obj_name: Name to use for the object collection with n{name} and
                         {name}_{attr} in the event
        :param attr: list of attributes to assign to each object in the
                     collection
        """
        self.obj_name = obj_name
        self.attrs = attrs

    def begin(self, event):
        self.objs = [ ]
        self._attach_to_event(event)

        self.ev_attrs = [getattr(event, self.obj_name+"_"+k) for k in self.attrs]
        self.nobjs = getattr(event, "n{}".format(self.obj_name))

    def _attach_to_event(self, event):
        setattr(event, self.obj_name, self.objs)

    def event(self, event):
        self._attach_to_event(event)
        self. objs[:] = [
            Object([
                (n, x[idx])
                for n,x in zip(self.attrs, self.ev_attrs)
            ])
            for idx in range(self.nobjs[0])
        ]


##__________________________________________________________________||

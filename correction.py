# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class ObjectCorrection(object):
    def __init__(self, in_obj, out_obj, correction):
        self.in_obj_name = in_obj
        self.out_obj_name = out_obj
        self.correction = correction

    def __repr__(self):
        name_value_pairs = (
            ('in_obj',    self.in_obj_name),
            ('out_obj',   self.out_obj_name),
            ('correction', self.correction),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def begin(self, event):
        self.out = [ ]
        self._attach_to_event(event)

        if hasattr(self.correction, 'begin'):
            self.correction.begin(event)

    def _attach_to_event(self, event):
        setattr(event, self.out_obj_name, self.out)

    def event(self, event):
        self._attach_to_event(event)

        self.out[:] = [self.correction(o) for o in getattr(event, self.in_obj_name)]

    def end(self):
        if hasattr(self.correction, 'end'):
            self.correction.end()
        self.out = None

##__________________________________________________________________||

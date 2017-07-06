# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class MockEvent(object):
    def __init__(self):

        object.__setattr__(self, 'attrdict',{ })
        # self.attrdict = { } # this would cause infinite recursion
        # https://docs.python.org/2/reference/datamodel.html
        # https://docs.python.org/3/reference/datamodel.html

    def __setattr__(self, name, value):
        if name not in self.attrdict:
            self.attrdict[name] = value
            return

        # the name has been already attached.
        # the value must be the same object as before
        if self.attrdict[name] is not value:
            raise ValueError('different objects are attached as "{}": {!r} is not {!r}.'.format(name, self.attrdict[name], value))

    def __getattr__(self, name):
        return self.attrdict[name]

##__________________________________________________________________||

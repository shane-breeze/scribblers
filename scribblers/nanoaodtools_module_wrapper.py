import sys
import os
import importlib

##__________________________________________________________________||
class EventWrapper(object):
    def __init__(self, event):
        self.event = event

    def __getattr__(self, attr):
        if attr.startswith("__"):
            raise AttributeError(attr)
        val = getattr(super(EventWrapper,self).__getattribute__("event"), attr)

        # countarray is not None for collections
        if val.countarray is None:
            if type(val[0]) == long:
                return int(val[0])
            else:
                return val[0]
        return val

    def __setattr__(self, attr, val):
        setattr(self.event, attr, val)

##__________________________________________________________________||
class TreeWrapper(object):
    def set_event(self, event):
        self.event = event

    def branch(self, name, *args, **kwargs):
        setattr(self, name, [])
        setattr(self.event, name, getattr(self, name))

    def fillBranch(self, name, val):
        setattr(self.event, name, getattr(self, name))
        if type(val) == list:
            getattr(self, name)[:] = val
        else:
            getattr(self, name)[:] = [val]

##__________________________________________________________________||
class NanoaodtoolsModuleWrapper(object):
    def __init__(self, module_path, module_name, *args, **kwargs):
        self.mc_only = kwargs.pop("mc_only") if "mc_only" in kwargs else None

        # redirect stdout
        with open(os.devnull,"w") as devNull:
            orig_stdout = sys.stdout
            sys.stdout = devNull

            # Import the nanoaod tools module
            nanoaodtools_module = importlib.import_module(module_path)
            self.nanoaodtools_module = getattr(nanoaodtools_module, module_name)(*args, **kwargs)

            sys.stdout = orig_stdout

    def begin(self, event):
        if self.mc_only is not None and self.mc_only and event.isdata[0]:
            return True

        # Setup wrappers
        self.tree = TreeWrapper()
        self.tree.set_event(event)
        self.wrapped_event = EventWrapper(event)

        # redirect stdout
        with open(os.devnull,"w") as devNull:
            orig_stdout = sys.stdout
            sys.stdout = devNull

            # Run the standard nanoaodtools module's begin sequence
            self.nanoaodtools_module.beginJob()
            self.nanoaodtools_module.beginFile(None, None, None, self.tree) # only last argument is implemented so far

            sys.stdout = orig_stdout

    def event(self, event):
        if self.mc_only is not None and self.mc_only and event.isdata[0]:
            return True

        self.tree.set_event(event)

        with open(os.devnull,"w") as devNull:
            orig_stdout = sys.stdout
            sys.stdout = devNull

            self.nanoaodtools_module.analyze(self.wrapped_event)

            sys.stdout = orig_stdout

##__________________________________________________________________||

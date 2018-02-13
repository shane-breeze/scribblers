class DatasetInfo(object):
    def begin(self, event):
        self.component = event.component

        self.isdata = [ ]
        self.name = [ ]
        self.era = [ ]
        self.nevents = [ ]
        self.nfiles = [ ]
        self.cross_section = [ ]
        self._attach_to_event(event)

        self.isdata[:] = [self.component.eventtype == "Data"]
        self.name[:] = self.component.dataset
        self.era[:] = self.component.era
        self.nevents[:] = [self.component.nevents]
        self.nfiles[:] = [self.component.nfiles]
        self.cross_section[:] = [self.component.cross_section]

    def _attach_to_event(self, event):
        event.isdata = self.isdata
        event.comp_name = self.name
        event.comp_era = self.era
        event.comp_nevents = self.nevents
        event.comp_nfiles = self.nfiles
        event.cross_section = self.cross_section

    def event(self, event):
        self._attach_to_event(event)

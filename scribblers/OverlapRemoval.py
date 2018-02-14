class OverlapRemoval(object):
    def __init__(self, collection_name=None, ref_collection=None):
        self.collection_name = collection_name
        self.ref_collection = ref_collection

    def begin(self, event):
        self.collection = getattr(event, self.collection_name)
        self.reference = getattr(event, self.ref_collection)

    def event(self, event):
        self.collection = [o for o in self.collection if o.idx in [r.jetIdx for r in self.reference]]

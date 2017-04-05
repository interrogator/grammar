
class Feature(object):
    """
    Metaclass for various kinds of feature

    Linguistic features are hierarchical, so they should retain a reference to
    the parent. The realisation is added when known.
    """

    def __init__(self, parent, realisation=None):
        self.parent = parent
        if realisation is not None:
            self.realisation = realisation
        else:
            self.realisation = self.determine()

    def __repr__(self):
        return str(self.realisation)

    def determine(feat):
        pass

class BooleanFeature(Feature):

    def __init__(self, parent, realisation=None):
        super(BooleanFeature, self).__init__(parent, realisation)

class IntFeature(Feature):

    def __init__(self, parent, realisation=None):
        super(IntFeature, self).__init__(parent, realisation)

class FloatFeature(Feature):

    def __init__(self, parent, realisation=None):
        super(FloatFeature, self).__init__(parent, realisation)

class CategoricalFeature(Feature):

    def __init__(self, parent, realisation=None):
        super(CategoricalFeature, self).__init__(parent, realisation)
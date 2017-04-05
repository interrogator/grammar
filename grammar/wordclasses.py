from grammar.features import BooleanFeature, IntFeature, CategoricalFeature, FloatFeature
from grammar.config import OPEN_CLASSES

class WordClass(object):

    def __init__(self, parent, realisation=None):
        self.parent = parent
        if realisation is not None:
            self.realisation = realisation
        else:
            self.realisation = self.determine()
        is_open = self.realisation in OPEN_CLASSES
        self.open = BooleanFeature(self, is_open)

class Noun(WordClass):

    def __init__(self, parent, realisation=None):
        super(Noun, self).__init__(self, 'noun')
        self.plural = BooleanFeature(self)
        self.mass = BooleanFeature(self)
        self.case = CategoricalFeature(self)

class Verb(WordClass):

    def __init__(self, parent, realisation=None):
        super(Verb, self).__init__(self, 'verb')
        self.finite = BooleanFeature(self)
        self.person = IntFeature(self)
        self.tense = CategoricalFeature(self)
        self.conditional = BooleanFeature(self)
        self.perfect = BooleanFeature(self)
        self.progressive = BooleanFeature(self)

class Adjective(WordClass):

    def __init__(self, parent, realisation=None):
        super(Adjective, self).__init__(self, 'adjective')
        self.comparative = IntFeature()

class Adverb(WordClass):

    def __init__(self, parent, realisation=None):
        super(Adverb, self).__init__(self, 'adverb')

class Preposition(WordClass):
    def __init__(self, parent, realisation=None):
        super(Preposition, self).__init__(self, 'preposition')

class Pronoun(WordClass):
    def __init__(self, parent, realisation=None):
        super(Pronoun, self).__init__(self, 'pronoun')
        self.referent = False
from grammar.objects import Token
from grammar.wordclasses import Preposition
TRAIN_PATH = '/Users/mahsa/work/UD_English/en-ud-train.conllu'
PICKLE = "averaged_perceptron_tagger.pickle"

class Contents(list):
    """
    Meta container for objects containing ordered sequences of other objects
    """
    def __init__(self, parent, realisation=None):
        self.parent = parent
        super(Contents, self).__init__(realisation)

class Text(Contents):

    """
    The broadest part of the model
    """
    def __init__(self, realisation=None):
        from grammar.annotators.tagger import PerceptronTagger, _load_data
        tagger = PerceptronTagger()
        training = _load_data(TRAIN_PATH, feature='wc')
        tagger.train(training, PICKLE)
        if realisation is not None and not isinstance(realisation, Contents):
            realisation = self.realise(realisation)
        super(Text, self).__init__(self.model, realisation)

    def realise(string):
        import nltk
        return nltk.sent_tokenize(s)

class Sentence(Contents):
    """
    A container of Tokens
    """
    def __init__(self, parent, realisation=None):
        
        if realisation is not None and not isinstance(realisation, Contents):
            realisation = tokenize(realisation)
        super(Sentence, self).__init__(parent, realisation)

    def realise(sent):
        import nltk
        from grammar.objects import Token
        return [Token(self.parent, t) for t in nltk.word_tokenize(sent)]

class Phrase(Contents):
    """
    Basically a Preposition + Group
    """
    def __init__(self, parent, realisation=None):
        super(Phrase, self).__init__(parent, realisation)
        self.preposition = Group([Preposition()])
        self.group = Group()

class Clause(Contents):

    def __init__(self, parent, realisation=None):
        assert(isinstance(parent, Sentence))
        super(Clause, self).__init__(parent, realisation)

class BoundClause(Clause):

    def __init__(self, parent, realisation=None):
        super(BoundClause, self).__init__(parent, realisation)

class FreeClause(Clause):

    def __init__(self, parent, realisation=None):
        assert(isinstance(parent, Sentence))
        super(FreeClause, self).__init__(parent, realisation)

class Group(Contents):
    """
    A constituent
    """
    def __init__(self, parent, realisation=None):
        super(Group, self).__init__(parent, realisation)

class NominalGroup(Group):
    def __init__(self, parent, realisation=None):
        super(NominalGroup, self).__init__(parent, realisation)

class VerbalGroup(Group):
    def __init__(self, parent, realisation=None):
        super(VerbalGroup, self).__init__(parent, realisation)
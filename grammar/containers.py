from grammar.objects import Token
from grammar.wordclasses import Preposition

class Contents(list):
    """
    Meta container for objects containing ordered sequences of other objects
    """
    def __init__(self, parent, realisation=None):
        self.parent = parent
        super(Contents, self).__init__(realisation)

class Sentence(Contents):
    """
    A container of Tokens
    """
    def __init__(self, parent, realisation=None):
        
        if realisation is not None:
            assert(all(isinstance(i, Token) for i in realisation))
        super(Sentence, self).__init__(parent, realisation)

class Group(Contents):
    """
    A constituent
    """
    def __init__(self, parent, realisation=None):
        super(Group, self).__init__(parent, realisation)


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
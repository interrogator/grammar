"""
Current limits of NLP may be caused by the fact that categories and features 
confound one another. POS tags, for example, conflate word class, person, 
number, etc., inconsistently. machine learning is learning about 3rd singular
conjugatioon for nouns, which makes no sense.

So, we need to create a feature hierarchy, keeping systems discrete.We still 
want everything to be machine learnable, though, and never rule-based
"""
#
from grammar.features import *
from grammar.wordclasses import Noun, Verb, Adjective, Adverb, Determiner, Preposition, WordClass

wcdict=dict(noun=Noun,verb=Verb,adjective=Adjective, adverb=Adverb,
            determiner=Determiner, preposition=Preposition, wordClass=WordClass)

class Token(object):
    """
    Model token in a sentence
    """
    def __init__(self, form, index, lemma=None, wordclass=None):

        self.form = form
        self.index = index
        self.lemma = CategoricalFeature(self, lemma)
        self.wordclass = wcdict.get(wordclass)(self)
        #self.regular = BooleanFeature(self)

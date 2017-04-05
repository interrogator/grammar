"""
Current limits of NLP may be caused by the fact that categories and features 
confound one another. POS tags, for example, conflate word class, person, 
number, etc., inconsistently. machine learning is learning about 3rd singular
conjugatioon for nouns, which makes no sense.

So, we need to create a feature hierarchy, keeping systems discrete.We still 
want everything to be machine learnable, though, and never rule-based
"""
#
from grammar.features import CategoricalFeature
from grammar.wordclasses import Noun, Verb, Adjective, Adverb, Determiner, Preposition, WordClass

wcdict=dict(noun=Noun, verb=Verb, adjective=Adjective, adverb=Adverb,
            determiner=Determiner, preposition=Preposition, WordClass=WordClass)

nltktag = dict(noun='n', adjective='a', adverb='r', verb='v')

from nltk.stem import WordNetLemmatizer
lemmatiser = WordNetLemmatizer()

class Token(object):
    """
    Model token in a sentence
    """
    def __init__(self, parent, realisation=None):

        self.parent = parent # Sentence
        if not realisation:
            return
        self.form = realisation
        wc, cert = self._get('wordclass', form, parent)
        self.wordclass = CategoricalFeature(self, wc, certainty=cert)
        lem = lemmatiser.lemmatize(realisation, nltktag.get(wc.lower()))
        self.lemma = CategoricalFeature(self, lem)
        self.regular = BooleanFeature(self, self.lemma == self.realisation)

    def _get(self, feature, form, parent):
        analysis = False
        certainty = 0
        #models[feature]
        return (analysis, certainty)
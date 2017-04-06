
def make_models(path='en-ud-train.conllu', just_features=False, save="word-model.p", load=False):
    import pandas as pd
    from corpkit.constants import CORENLP_COREF_CATS
    from grammar.annotators.tagger import PerceptronTagger, _load_data
    import os
    import pickle as pickle
    if load:
        if os.path.isfile(save):
            print("Loading model")
            with open(save, "rb") as fo:
                return pickle.load(fo)
        else:
            raise FileNotFoundError

    print("Generating model ... ")

    df = _load_data(os.path.expanduser(path))
    cols = list(df.columns)
    features = [i for i in ['x', 'p', 'l'] + CORENLP_COREF_CATS if i in cols]
    if just_features:
        features = [i for i in features if i in just_features]
    #sents = df.groupby(level=['file', 's'])
    sents = df
    print("Data loaded from {}".format(path))
    taggers = {}
    for feature in features:
        if feature == 'l':
            continue
        tagger = PerceptronTagger(load=False)
        tups = sents[['w', feature, 'x']].groupby(level=['file', 's'])
        #return tups
        print('Training %s' % feature)
        tagger.train(tups, feature=feature)
        taggers[feature] = tagger
    if save:
        print("Saving model as %s ..." % save)
        with open(save, 'wb') as fo:
            pickle.dump(taggers, fo)
    return taggers

def add_layer(df, feature, taggers, lemmatiser=False):
    from grammar.config import RESTRICTIONS
    if feature == 'l':
        subdf = df[df['x'].isin(['NOUN', 'VERB', 'ADJ', 'ADV'])]
        subdf['_tags'] = subdf['x'].str.replace('ADJ', 'r').str.slice(0, 1).str.lower()
        df[feature] = subdf[['w', '_tags']].apply(lambda x: lemmatiser.lemmatize(*x), raw=True, axis=1)
        df[feature] = df[feature].fillna(df['w'])
    elif feature in taggers:
        poss_labels = RESTRICTIONS.get(feature, False)
        if not poss_labels:
            df[feature] = [y for x, y in taggers[feature].tag(df['w'])]
        else:
            subdf = df[df['x'].isin(poss_labels)]
            df[feature] = pd.Series([y for x, y in taggers[feature].tag(subdf['w'])], index=subdf.index)
    return df

def process(string, taggers):
    from nltk import word_tokenize, sent_tokenize
    import pandas as pd
    from corpkit.constants import CORENLP_COREF_CATS
    
    sents = [word_tokenize(s) for s in sent_tokenize(string)]
    flat = [item for sublist in sents for item in sublist]
    lens = [len(x) for x in sents]
    ix = []
    for i, l in enumerate(lens, start=1):
        for x in range(1, l+1):
            ix.append((i, x))
    ix = pd.MultiIndex.from_tuples(ix)
    df = pd.DataFrame({'w': flat}, index=ix)
    from nltk.stem import WordNetLemmatizer
    wl_lemmer = WordNetLemmatizer()

    for feature in ['x', 'l', 'p'] + CORENLP_COREF_CATS:
        df = add_layer(df, feature, taggers, lemmatiser=wl_lemmer)

    return df

#%prun -s cumulative -l 50 taggers = make_models()
#df = process('This is the bit of my text. Here is a second sentence. The third is the last. Actually, it is not. I am going to add some more text so that hopefully I can understand the nature of the problem. London was hit by a storm. If it were the case, that would be a subjunctive. Do you like interrogatives? Why wouldn\'t you?', taggers)


class Grammar(object):

    def __init__(self):
        self._model = False

    def model(self, **kwargs):
        self._model = make_models(**kwargs)
        return self._model

    def evaluate(self, **kwargs):
        from grammar.tagger import evaluate
        if not self._model:
            self.model(**kwargs)
        return evaluate(self.model, kwargs.get('training_data', False))

    def process(self, string, **kwargs):
        if not self._model:
            self.model(**kwargs)
        return process(string, self._model)

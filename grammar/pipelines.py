
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
            pass

    df = _load_data(os.path.expanduser(path))
    cols = list(df.columns)
    features = [i for i in ['x', 'p', 'l'] + CORENLP_COREF_CATS if i in cols]
    if just_features:
        features = [i for i in features if i in just_features]
    #sents = df.groupby(level=['file', 's'])
    sents = df
    print("Data loaded from {}".format(path))
    taggers = {}
    #todo: tqdm
    for feature in features:
        if feature == 'l':
            continue
        tagger = PerceptronTagger(load=False)
        tups = sents[['w', feature, 'x', 's']].groupby('s')
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
    import pandas as pd
    if feature == 'l':
        subdf = df[df['x'].isin(['NOUN', 'VERB', 'ADJ', 'ADV'])].copy()
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
    from nltk.tokenize.punkt import PunktSentenceTokenizer
    from nltk import word_tokenize, sent_tokenize
    import pandas as pd
    from corpkit.constants import CORENLP_COREF_CATS
    

    #text = 'Rabbit say to itself "Oh dear! Oh dear! I shall be too late!"'
    sents = []
    for start, end in PunktSentenceTokenizer().span_tokenize(string):
        sents.append((word_tokenize(string[start:end]), start, end))

    offsets = dict()
    
    ix = []
    flat = []
    for i, (tokens, start, end) in enumerate(sents, start=1):
        flat += tokens
        offsets[i] = dict(start=start, end=end)
        for x in range(1, len(tokens)+1):
            ix.append((i, x))
    ix = pd.MultiIndex.from_tuples(ix)
    df = pd.DataFrame({'w': flat}, index=ix)
    df.index.names = ['s', 'i']

    offsets = pd.DataFrame(offsets).T
    offsets.index.name = 's'
    df = offsets.join(df, how='inner')

    from nltk.stem import WordNetLemmatizer
    wl_lemmer = WordNetLemmatizer()

    for feature in ['x', 'l', 'p'] + CORENLP_COREF_CATS:
        df = add_layer(df, feature, taggers, lemmatiser=wl_lemmer)

    col_order = ['w', 'l', 'x', 'p'] + [i for i in CORENLP_COREF_CATS if i in df.columns] + ['start', 'end']

    return df[col_order]

#%prun -s cumulative -l 50 taggers = make_models()
#df = g.process('This is the bit of my text. Here is a second sentence. The third is the last. Actually, it is not. I am going to add some more text so that hopefully I can understand the nature of the problem. London was hit by a storm. If it were the case, that would be a subjunctive. Do you like interrogatives? Why wouldn\'t you?', taggers)

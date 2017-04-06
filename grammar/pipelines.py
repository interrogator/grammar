TRAIN_PATH = '/Users/mahsa/work/UD_English/en-ud-train.conllu'
PICKLE = "averaged_perceptron_tagger.pickle"
#FEATURES = ['Number', 'Mood', 'Tense', 'VerbForm', 'Definite', 'PronType']

#from grammar.annotators.tagger import PerceptronTagger, _get_pretrain_model
#model = _get_pretrain_model()
#from grammar.containers import Text
#text = Text('Today is a beautiful day. The whales are singing.', model=model)

def get_tuples(df, feature):
    from corpkit.dictionaries.word_transforms import taglemma
    if feature == 'wc':
        df['wc'] = df['p'].apply(lambda x: taglemma.get(x.lower(), x).title())
    array = [y.values for x, y in df[['w', feature]].groupby(level=['file', 's'])]
    return [list(x) for x in array]

def make_models(path='/Users/mahsa/work/UD_English/en-ud-train.conllu'):
    import pandas as pd
    from corpkit.constants import CORENLP_COREF_CATS
    from grammar.annotators.tagger import PerceptronTagger, _load_data
    #TRAIN_PATH = '/Users/mahsa/work/UD_English/en-ud-train.conllu'
    PICKLE = "averaged_perceptron_tagger.pickle"
    df = _load_data(path)
    taggers = {}
    for feature in ['wc'] + CORENLP_COREF_CATS:
        tagger = PerceptronTagger(load=False)
        if feature not in df.columns and feature != 'wc':
            continue
        print(feature)
        tups = get_tuples(df, feature)
        #print(tups)
        tagger.train(tups)
        taggers[feature] = tagger
    return taggers

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
    for feature in ['wc'] + CORENLP_COREF_CATS:
        #todo: feature typology to prevent wasting time on finiteness of nouns
        #if feature not in df.columns:
        #    continue
        print(feature)
        #tups = get_tuples(df, feature)
        if feature in taggers:
            df[feature] = [y for x, y in taggers[feature].tag(df['w'])]
            print(df[feature])
    return df

taggers = make_models()
df = process('This is the bit of my text. Here is a second sentence. The third is the last. Actually, it is not. I am going to add some more text so that hopefully I can understand the nature of the problem.', taggers)
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

def process(string):
    import pandas as pd
    from nltk import word_tokenize, sent_tokenize
    from grammar.annotators.tagger import PerceptronTagger, _load_data
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
    tagger = PerceptronTagger()
    TRAIN_PATH = '/Users/mahsa/work/UD_English/en-ud-train.conllu'
    PICKLE = "averaged_perceptron_tagger.pickle"
    df = _load_data(TRAIN_PATH)
    for feature in ['wc', 'l'] + CORENLP_COREF_CATS:
        print(feature)
        tups = get_tuples(df, feature)
        tagger.train(tups, PICKLE)
        df[feature] = tagger.tag(df['w'])
    return df
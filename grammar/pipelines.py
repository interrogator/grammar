def pipeline(text):
    sents = Contents([Sentence(tokenise(s)) for s in sent_tokenise(text)])
    for sent in sents:
        model = process(sent, context=sents)


from grammar.annotators.tagger import PerceptronTagger, _get_pretrain_model
model = _get_pretrain_model()
from grammar.containers import Text
text = Text('Today is a beautiful day. The whales are singing.', model=model)
#tagger = PerceptronTagger(load=False)
#tagger.train(indata)
#tagger
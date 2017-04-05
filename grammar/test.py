def test():
    from grammar.containers import Sentence
    from grammar.objects import Token

    toks = [('the', 'the', 'determiner'),
            ('cats', 'cat', 'noun'),
            ('are', 'be', 'verb'),
            ('the', 'the', 'determiner'),
            ('best', 'good', 'adjective'),
            ('team', 'team', 'noun')]

    sent = []
    for i, (w, l, c) in enumerate(toks):
        t = Token(w, i, l, c)
        sent.append(t)

    sent = Sentence(None, sent)
    print(sent)
    for i in sent:
        print(i)
        print(i.__dict__)

if __name__ == '__main__':
    test()
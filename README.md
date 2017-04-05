# Grammar

I've been thinking a bit lately about formalising a functional grammar of English. I've also been thinking about the successes and limits of these kinds of grammars, and of current NLP.

It's uncontroversial now that state of the art results come from probablisitic/statistical, rather than rule-based methods. It also seems, however, that the data used to train the machine is misconceived. The current set of POS tags, for example, conflates word class, number, progressive, person, etc., all into one set of labels that gets applied to every word. How can statistical NLP improve if stats are derived from unmeaningful, contradictory labels?

So, I had the idea of a system that typologises features as is done in systemic grammars. Features that are known are assigned; unknown features are determined statistically, referring to a (non-existent) corpus/treebank with nice, discrete annotations. I'm not the first to think about this, but I want to try an implementation that is bidirectional between parsing and generation, and able to take context into account.

The system involves a great deal of class inheritance, based on the idea of a few primitives:

* `Container/Contents`, a holder of objects
* `Object`, a thing that is discrete and realised
* `Feature`, an attribute of ojects, which may be boolean, categorical, numerical...

Anyway, watch this space!


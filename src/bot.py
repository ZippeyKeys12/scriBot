from contextlib import closing

import spacy
from markovify import Text as MarkovText
from nltk.tokenize import word_tokenize


class ScriBot(MarkovText):
    separator: str = "::"

    def __init__(self, input_text, retain_original: bool = True):
        self.nlp = spacy.load("en", disable=["parser", "ner", "textcat"])
        MarkovText.__init__(self, input_text, retain_original=retain_original)

    def word_split(self, sentence: str, pos: bool = True) -> list:
        if pos:
            tokens = []
            for token in self.nlp(sentence):
                orth = token.orth_
                if orth.isspace() or token.like_url or orth.startswith("#"):
                    continue
                elif orth.startswith("@"):
                    tokens.append("#username#")
                else:
                    tokens.append(self.separator.join((orth, token.pos_)))
        else:
            tokens = word_tokenize(sentence)
        return tokens

    def word_join(self, words: list, pos: bool = True) -> str:
        if pos:
            sentence = " ".join(word.split(self.separator)[0] for word in words)
        else:
            sentence = " ".join(words)
        return sentence

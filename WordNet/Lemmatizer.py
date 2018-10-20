from WordNet.WordNetAdjective import WordNetAdjective
from WordNet.WordNetAdverb import WordNetAdverb
from WordNet.WordNetNoun import WordNetNoun
from WordNet.WordNetVerb import WordNetVerb

from nltk.stem import WordNetLemmatizer

import nltk
from nltk.corpus import wordnet


class Lemmatizer:
    def __init__(self, pathToWordNetDict):

        # Разделитель составных слов
        self.splitter = "-"

        # Инициализируем объекты с частям речи
        adj = WordNetAdjective(pathToWordNetDict)  # Прилагательные
        noun = WordNetNoun(pathToWordNetDict)  # Существительные
        adverb = WordNetAdverb(pathToWordNetDict)  # Наречия
        verb = WordNetVerb(pathToWordNetDict)  # Глаголы

        self.wordNet = [verb, noun, adj, adverb]

        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.lmtzr = nltk.WordNetLemmatizer().lemmatize

    def get_wordnet_pos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None


    # Метод возвращает лемму слова (возможно, составного)
    def GetLemma(self, word_w_pos):
        word = word_w_pos[0]
        pos = word_w_pos[1]
        # Если в слове есть тире, разделим слово на части, нормализуем каждую часть(каждое слово) по отдельности, а потом соединим
        wordArr = word.split(self.splitter)
        resultWord = []
        for word in wordArr:
            lemma = self.__GetLemmaWord(word, pos)
            if (lemma != None):
                resultWord.append(lemma)

        return self.splitter.join(resultWord) if resultWord != None else None

    def __GetLemmaWord(self, word, pos)->str:
        wn_pos = self.get_wordnet_pos(pos)
        # print(word, wn_pos)
        lemma = self.wordnet_lemmatizer.lemmatize(word, wn_pos)
        return lemma #if lemma != word else self.__GetLemmaWord2(word)

    # Метод возвращает лемму(нормализованную форму слова)
    def __GetLemmaWord2(self, word):
        for item in self.wordNet:
            lemma = item.GetLemma(word)
            if (lemma != None):
                return lemma
        return None

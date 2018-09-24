import re
import os
import logging

from collections import Counter
from WordNet.Lemmatizer import Lemmatizer

import nltk
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer

logging.basicConfig(level = logging.DEBUG)


from nltk.corpus import wordnet

wnl = WordNetLemmatizer()

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
        return None #''


def penn_to_wn(tag):
    return get_wordnet_pos(tag)



def penn2morphy(penntag):
    """ Converts Penn Treebank tags to WordNet. """
    morphy_tag = {'NN':'n', 'JJ':'a',
                  'VB':'v', 'RB':'r'}
    try:
        return morphy_tag[penntag[:2]]
    except:
        return 'n'

def lemmatize_sent(text):
    # Text input is string, returns lowercased strings.
    return [wnl.lemmatize(word.lower(), pos=penn2morphy(tag))
            for word, tag in pos_tag(word_tokenize(text))]



class FrequencyDict:
    def __init__(self, pathToWordNetDict, pathToStopWords):
        
# Простое слово, например "over", можно найти, используя выражение "([a-zA-Z]+)" - здесь ищется одна или более букв английского алфавита.
# Составное слово, к примеру "commander-in-chief", найти несколько сложнее, нам нужно искать идущие друг за другом 
# подвыражения вида "commander-", "in-", после которых идет слово "chief".
# Регулярное выражение примет вид "(([a-zA-Z]+-?)*[a-zA-Z]+)".
# Если в выражении присутсвует промежуточное подвыражение, оно тоже включается в результат. Так, в наш результат попадает не только слово 
# "commander-in-chief", но также и все найденные подвыражения, Чтобы их исключить, добавим в начале подвыражеения '?:' стразу после открывающейся круглой скобки.		
# Тогда регулярное выражение примет вид "((?:[a-zA-Z]+-?)*[a-zA-Z]+)".
# Нам еще осталось включить в выражения слова с апострофом вида "didn't".		
# Для этого заменим в первом подвыражении "-?" на "[-']?".
# Все, на этом закончим улучшения регулярного выражения, его можно было бы улучшать и дальше, но остановимся на таком: 
# "((?:[a-zA-Z]+[-']?)*[a-zA-Z]+)"
        # Определяем регулярное выражение для поиска английских слов
        self.wordPattern = re.compile(r"((?:[a-zA-Z]+[-'’]?)*[a-zA-Z]+)")
        
        # Частотный словарь(использум класс collections.Counter для поддержки подсчёта уникальных элементов в последовательностях) 		
        self.frequencyDict = Counter()
        self.LoadStopWords(pathToStopWords)


    def LoadStopWords(self, pathToStopWords):
        self.stopWords = set()
        with open(pathToStopWords, 'rU') as file:
          for line in file:
            self.stopWords.add(line.strip())

        
    def ParseBook(self, file):
        if file.endswith(".txt") or  file.endswith(".srt"): 
            self.__ParseTxtFile(file, self.__FindWordsFromContent)
        elif file.endswith(".srt"):
            self.__ParseStrFile(file, self.__FindWordsFromContent)


    def __ParseTxtFile(self, txtFile, contentHandler):
        try:
            with open(txtFile, 'rU') as file:
                text = file.read()
                contentHandler(text)
        except Exception as e:
            print('Error parsing "%s"' % txtFile, e)
            

    ## Метод находит в строке слова согласно своим правилам, нормализует их и затем добавляет в частотный словарь
    def __FindWordsFromContent(self, content):
        # [wnl.lemmatize(i, j[0].lower()) if j[0].lower() in ['a', 'n', 'v'] else wnl.lemmatize(i) for i, j in pos_tag(word_tokenize(txt))]
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sent_text = tokenizer.tokenize(content)
        for sentence in sent_text:
            tokenized_text = nltk.word_tokenize(sentence)
            token_list=[]
            for token in tokenized_text:
                token=token.replace("’", "'")
                token_list.append(token)
            tagged = nltk.pos_tag(token_list)
            #print(tagged)

        print(token_list[:10])
        #print(sents[:3])

        list_words = self.wordPattern.findall(content) 	# В строке найдем список английских слов
        set_words = set(list_words)
        for word in list_words:
            word = word.replace("’", "'")
            if word == 'I': continue
            if not (word[0].islower()) and (word.lower() in set_words):
                word = word.lower()

            if word in self.stopWords: continue
            #lemma = self.lemmatizer.GetLemma(word) 	# Нормализуем слово
            #if (lemma != ""):
                #pass#self.frequencyDict[lemma] += 1		# Добавляем в счетчик частотного словаря нормализованное слово
            #else:
            self.frequencyDict[word] += 1		# Добавляем в счетчик частотного словаря не нормализованное слово
                #logging.debug(word)

    
    # Метод отдает первые countWord слов частотного словаря, отсортированные по ключу и значению
    def FindMostCommonElements(self, countWord):
        # dict = list(self.frequencyDict.items())
        # dict.sort(key=lambda t: t[0])
        # dict.sort(key=lambda t: t[1], reverse = True)
        return self.frequencyDict.most_common(int(countWord))    # dict[0 : int(countWord)]

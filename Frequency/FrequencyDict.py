#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 
import re
import os
import logging

from collections import Counter
from WordNet.Lemmatizer import Lemmatizer

logging.basicConfig(level = logging.DEBUG)
     
class FrequencyDict:
    def __init__(self, pathToWordNetDict):
        
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
        self.wordPattern = re.compile("((?:[a-zA-Z]+[-'’]?)*[a-zA-Z]+)")
        
        # Частотный словарь(использум класс collections.Counter для поддержки подсчёта уникальных элементов в последовательностях) 		
        self.frequencyDict = Counter()

        # Создаем нормализатор английских слов
        self.lemmatizer = Lemmatizer(pathToWordNetDict)

        self.LoadStopWords()


    def LoadStopWords(self):
        fileName  = r"D:\Win7\lis\Documents\Dev\_DataMining\_Text\Meta\StopWord.txt"
        self.stopWords = set()
        with open(fileName, 'rU') as file:
          for line in file:
            self.stopWords.add(line.strip())

        
    # Метод парсит файл, получает из нее слова
    def ParseBook(self, file):
        if file.endswith(".txt") or  file.endswith(".srt"): 
            self.__ParseTxtFile(file, self.__FindWordsFromContent)

    # def generate_words_list(self, file):


            
    # Метод парсит файл в формате txt
    def __ParseTxtFile(self, txtFile, contentHandler):
        # try:
            with open(txtFile, 'r', encoding='UTF-8') as file:
                text = file.read()
                contentHandler(text)
                # for line in file:			# Читаем файл построчно
                #     contentHandler(line)	# Для каждой строки вызываем обработчик контента
        # except Exception as e:
        #     print('Error parsing "%s"' % txtFile, e)
            

    ## Метод находит в строке слова согласно своим правилам, нормализует их и затем добавляет в частотный словарь
    def __FindWordsFromContent(self, content):
        list_words = self.wordPattern.findall(content) 	# В строке найдем список английских слов
        set_words = set(list_words)
        for word in list_words:
            #lemma = self.lemmatizer.GetLemma(word) 	# Нормализуем слово
            #if (lemma != ""):
                #pass#self.frequencyDict[lemma] += 1		# Добавляем в счетчик частотного словаря нормализованное слово
            #else:
            # if word == 'He':
            #     isCapital = not word[0].islower()
            #     lowered = word.lower()
            #     inLowSet = lowered in set_words
            #     inSet = word in set_words
            #     if (not inLowSet) or (not inSet):
            #         print(word, isCapital, lowered, inLowSet, inSet)
            if not (word[0].islower()) and (word.lower() in set_words):
                word = word.lower()

            if word in self.stopWords: continue
            self.frequencyDict[word] += 1		# Добавляем в счетчик частотного словаря не нормализованное слово
                #logging.debug(word)

    
    # Метод отдает первые countWord слов частотного словаря, отсортированные по ключу и значению
    def FindMostCommonElements(self, countWord):
        dict = list(self.frequencyDict.items())
        dict.sort(key=lambda t: t[0])
        dict.sort(key=lambda t: t[1], reverse = True)
        return dict[0 : int(countWord)]

        
        

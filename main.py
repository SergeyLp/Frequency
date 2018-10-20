import os

from Frequency.IniParser import IniParser
from Frequency.FrequencyDict import FrequencyDict
from StarDict.StarDict import StarDict
from WordNet.Lemmatizer import Lemmatizer

ConfigFileName = "Settings.ini"
TRACE = 2


class Main:
    def __init__(self):

        self.listLanguageDict = []  # В этом массиве сохраним словари StarDict
        self.result = []  # В этом массиве сохраним результат (само слово, частота, его перевод)

        try:
            # Создаем и инициализируем конфиг-парсер
            if TRACE > 1: print('Setup...')
            config = IniParser(ConfigFileName)

            self.pathToBooks = config.GetValue(
                "PathToBooks")  # путь до файлов(книг, документов и тд), из которых будут браться слова
            self.pathResult = config.GetValue("PathToResult")  # путь для сохранения результата
            self.countWord = config.GetValue(
                "CountWord")  # количество первых слов частотного словаря, которые нужно получить
            self.pathToWordNetDict = config.GetValue("PathToWordNetDict")  # путь до словаря WordNet
            self.pathToStarDict = config.GetValue("PathToStarDict")  # путь до словарей в формате StarDict
            self.pathToStopWords = config.GetValue("PathToStopWords")

            # Отделяем пути словарей StarDict друг от друга и удаляем пробелы с начала и конца пути. Все пути заносим в список listPathToStarDict
            listPathToStarDict = [item.strip(' \\') for item in self.pathToStarDict.split(";")]

            # Для каждого из путей до словарей StarDict создаем свой языковый словарь
            if TRACE > 1: print('Prepare dict...')
            for path in listPathToStarDict:
                languageDict = StarDict(path)
                self.listLanguageDict.append(languageDict)

                # Получаем список книг, из которых будем получать слова
            if TRACE > 1: print('Get source list...')
            self.listBooks = self.__GetAllFiles(self.pathToBooks)

            # Создаем частотный словарь		
            if TRACE > 1: print('Create freq...')
            self.frequencyDict = FrequencyDict(self.pathToWordNetDict, self.pathToStopWords)

            # Создаем нормализатор английских слов
            self.lemmatizer = Lemmatizer(self.pathToWordNetDict)

            # Подготовка закончена, загружены словари StarDict и WordNet. Запускаем задачу на выполнение, то есть начинаем парсить текстовые файл, нормализовывать и считать слова			
            if TRACE > 1: print('Run...')
            self.__Run()

        except Exception as e:
            print('In main class exception: "%s"' % e)

    # Метод создает список файлов, расположенных в папке path
    def __GetAllFiles(self, path):
        try:
            return [os.path.join(path, file) for file in os.listdir(path)]
        except Exception:
            raise Exception('Path "%s" does not exists' % path)

    # Метод бежит по всем словарям, и возвращает перевод из ближайшего словаря.
    # Если перевода нет ни в одном из словарей, возвращается None
    def __GetTranslate(self, w_pos) -> str:
        word = w_pos[0]
        pos = w_pos[1]
        if pos in ('NNP', 'NNPS'):
            return None

        if pos in ('VBD'):
            return self.lemmatizer.GetLemma(w_pos)

        for dictionary in self.listLanguageDict:
            valueWord = dictionary.Translate(word)
            if valueWord:
                return valueWord
        low = word.lower()
        for dictionary in self.listLanguageDict:
            valueWord = dictionary.Translate(low)
            if valueWord:
                return valueWord
        else:
            w2 = self.lemmatizer.GetLemma(w_pos)  # Нормализуем слово
            for dictionary in self.listLanguageDict:
                valueWord = dictionary.Translate(w2)
                if valueWord:
                    return f'({w2}) {valueWord}'
            return w2

    def __Run(self):
        for book in self.listBooks:
            self.frequencyDict.ParseBook(book)

        if TRACE > 1: print('Counting...')
        # Получаем первые countWord слов из всего получившегося списка английских слов			
        mostCommonElements = self.frequencyDict.FindMostCommonElements(self.countWord)

        if TRACE > 1: print('Translating...')
        import html
        # Получаем переводы для всех слов
        for item in mostCommonElements:
            word_with_p_o_s = item[0]
            counterWord = item[1]
            valueWord = self.__GetTranslate(word_with_p_o_s)
            print(
                f"{counterWord:5} {word_with_p_o_s[1]:4} {word_with_p_o_s[0]:11} "
                f"{html.unescape(valueWord) if valueWord  else ''}")


if __name__ == "__main__":
    main = Main()

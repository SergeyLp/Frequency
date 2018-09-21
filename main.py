import os

from Frequency.IniParser import IniParser
from Frequency.FrequencyDict import FrequencyDict
from StarDict.StarDict import StarDict

ConfigFileName="Settings.ini"
TRACE = 1

class Main:
    def __init__(self):
    
        self.listLanguageDict = [] 	# В этом массиве сохраним словари StarDict
        self.result = []  			# В этом массиве сохраним результат (само слово, частота, его перевод)

        try:
            # Создаем и инициализируем конфиг-парсер
            if TRACE > 1: print('Setup...')
            config = IniParser(ConfigFileName)	

            self.pathToBooks = config.GetValue("PathToBooks") 	 			# путь до файлов(книг, документов и тд), из которых будут браться слова
            self.pathResult = config.GetValue("PathToResult") 				# путь для сохранения результата
            self.countWord = config.GetValue("CountWord") 	 				# количество первых слов частотного словаря, которые нужно получить
            self.pathToWordNetDict = config.GetValue("PathToWordNetDict") 	# путь до словаря WordNet
            self.pathToStarDict = config.GetValue("PathToStarDict") 		# путь до словарей в формате StarDict
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
    
            # Подготовка закончена, загружены словари StarDict и WordNet. Запускаем задачу на выполнение, то есть начинаем парсить текстовые файл, нормализовывать и считать слова			
            if TRACE > 1: print('Run...')
            self.__Run()
        
        except Exception as e:
            print('Main class error: "%s"' %e)


    # Метод создает список файлов, расположенных в папке path	
    def __GetAllFiles(self, path):
        try:
            return [os.path.join(path, file) for file in os.listdir(path)]
        except Exception:
            raise Exception('Path "%s" does not exists' % path)		

        
    # Метод бежит по всем словарям, и возвращает перевод из ближайшего словаря.
    # Если перевода нет ни в одном из словарей, возвращается None
    def __GetTranslate(self, word: str)-> str:
        for dict in self.listLanguageDict:
            valueWord = dict.Translate(word)
            if valueWord:
                return valueWord
        else:
            return None

        
        
        
    # Метод сохраняет результат
    # (само слово, частота, его перевод) по первым countWord словам в файл формата Excel  	
    def __SaveResultToExcel(self):	
        try:
            if not os.path.exists(self.pathResult):
                raise Exception('No such directory: "%s"' %self.pathResult)	
            
            if self.result:	
                description = 'Frequency Dictionary'
                style = xlwt.easyxf('font: name Verdana')			
                wb = xlwt.Workbook()
                ws = wb.add_sheet(description + ' ' + self.countWord)	
                nRow = 0
                for item in self.result:
                    ws.write(nRow, 0, item[0], style)
                    ws.write(nRow, 1, item[1], style)
                    ws.write(nRow, 2, item[2], style)
                    nRow +=1
                    if nRow < 35: print (item[0],item[1])##,item[2])
                wb.save(os.path.join(self.pathResult, description +'.xls'))
        except Exception as e:
            print(e)			


    def __PrintResult(self):
        import html
        if self.result:
                nRow = 0
                for item in self.result:
                    if 110 > nRow:
                        print(f"{item[0]:5} {item[1]:11} {html.unescape(item[2]) if item[2]  else '~-~'}")
                    else:
                        print(item[1])
                    nRow += 1
                    ##if nRow < 35: print(item[0], item[1])  ##,item[2])

    # Метод запускает задачу на выполнение
    def __Run(self):					
        # Отдаем частотному словарю по одной книге	
        for book in self.listBooks:
            self.frequencyDict.ParseBook(book)		

        if TRACE > 1: print('Counting...')
        # Получаем первые countWord слов из всего получившегося списка английских слов			
        mostCommonElements = self.frequencyDict.FindMostCommonElements(self.countWord)

        if TRACE > 1: print('Translating...')
        # Получаем переводы для всех слов
        for item in mostCommonElements:
            word = item[0]
            counterWord = item[1]
            valueWord = self.__GetTranslate(word)
            self.result.append([counterWord, word, valueWord])	

        self.__PrintResult()

        
        
    
if __name__ == "__main__":
    main = Main()

    


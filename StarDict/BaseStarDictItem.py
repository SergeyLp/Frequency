import os

class BaseStarDictItem:
    def __init__(self, pathToDict, exp):
        self.encoding = "utf-8"
        self.dictionaryFile = self.__PathToFileInDirByExp(pathToDict, exp)
        self.realFileSize = os.path.getsize(self.dictionaryFile)

    # Метод ищет в папке path первый попапвшийся файл с расширением exp
    def __PathToFileInDirByExp(self, path, exp):
        if not os.path.exists(path):
            raise Exception('Path "%s" does not exists' % path)

        list_f = [f for f in os.listdir(path) if f.endswith(f'.{exp}')]
        if list_f:
            return os.path.join(path, list_f[0])  # Возвращаем первый попавшийся
        else:
            raise Exception('File does not exist: "*.%s"' % exp)

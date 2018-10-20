from StarDict.BaseStarDictItem import BaseStarDictItem
import re

class Dict(BaseStarDictItem):
    def __init__(self, pathToDict):
        # Конструктор родителя (BaseStarDictItem)
        BaseStarDictItem.__init__(self, pathToDict, 'dict')
        self.tag_re = re.compile(r'</?[a-z]*>')

    def GetTranslation(self, wordDataOffset, wordDataSize):
        try:
            # Убеждаемся что смещение и размер данных неотрицательны и находятся в пределах размера файла .dict
            self.__CheckValidArguments(wordDataOffset, wordDataSize)

            with open(self.dictionaryFile, 'rb') as file:
                file.seek(wordDataOffset)
                byteArray = file.read(wordDataSize)
                article = byteArray.decode(self.encoding)  # (self.encoding определен в базовом классе BaseDictionaryItem)

                pos_k_tag = article.find('<k>')
                if pos_k_tag >= 0:
                    pos_k_tag = article.find('</k>', pos_k_tag) + len('</k>')
                    article = article[pos_k_tag:].strip().replace('<tr>', '[').replace('</tr>', ']')
                    article = re.sub(self.tag_re, '', article)
                    article = article.replace('\n', ' ')

                return article

        except Exception as e:
            return None

    def __CheckValidArguments(self, wordDataOffset, wordDataSize):
        if wordDataOffset is None or wordDataOffset < 0:
            pass
        endDataSize = wordDataOffset + wordDataSize
        if wordDataOffset < 0 or wordDataSize < 0 or endDataSize > self.realFileSize:
            raise Exception

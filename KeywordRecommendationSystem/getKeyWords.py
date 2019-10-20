import jieba
import jieba.analyse



txt = open(r"/Users/zuchebao/Downloads/全职高手【完本】.txt", "r", encoding='utf-8').read()
def getKeyWord(txt):
        keywords_textrank = jieba.analyse.extract_tags( txt, topK=5, withWeight=True, allowPOS=('n','nr','ns','a'), withFlag=False)
        return(keywords_textrank)

print(getKeyWord(txt))


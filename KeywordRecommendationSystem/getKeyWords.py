import jieba
import jieba.analyse
import datetime
import synonyms

# txt = open(r"/Users/zuchebao/Downloads/全职高手【完本】.txt", "r", encoding='utf-8').read()
def getKeyWord(txt):
        keywords_textrank = jieba.analyse.extract_tags( txt, topK=5, withWeight=True, allowPOS=('n','nr','ns','a'), withFlag = False)
        return(keywords_textrank)


# 通过同义词林获取近义词和同义词
def getSym(w,wordSet):
    # w:  input word
    # word_set: 同义词词集或相关词词集
    if len(symWords) == 0:
        getDic()
    results = []
    if len(w) == 1:
        for each in wordSet:
            for word in each:
                if w[0] == word:
                    results.append({w[0]:each})
                    break
    else:
        for each in wordSet:
            for word in each:
                    for i in w:
                        if i == word:
                                results.append({i:each})
                                break
    return results


f = open('cilin.txt', 'r', encoding = 'utf-8')
symWords = []
symClassWords = []
def getDic():
    lines = f.readlines()
    symWords = []
    symClassWords = []

    for line in lines:
        line = line.replace('\n','')
        items = line.split(' ')
        index = items[0]
        if index[-1] == '=':
            symWords.append(items[1:])
        if index[-1] == '#':
            symClassWords.append(items[1:])

input = [""]
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print('同义词')
print(getSym(input, symWords))
print('同类词')
print(getSym(input, symClassWords))

# 通过Synonyms获取同义词
print(synonyms.nearby("二极管"))
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
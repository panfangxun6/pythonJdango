import jieba
import jieba.analyse
from io import *
import synonyms
import jieba.posseg as pseg
import re
# 读入同义词林
#
# f = open('/Users/zuchebao/PycharmProjects/KeywordRecommendationSystem/dict/cilin.txt', 'r', encoding='utf-8')
f = open('dict/cilin.txt', 'r', encoding='utf-8')
# jieba.load_userdict("/Users/zuchebao/PycharmProjects/KeywordRecommendationSystem/dict/newIDF.txt")
jieba.load_userdict("dict/newWord.txt")
symWords = []
symClassWords = []



#加载停用词
stopWordFile = open("dict/stopWord",'r',encoding='utf-8')
stopWord = []
for line in stopWordFile.readline():
    stopWord.append(line.strip())
print(stopWord)
def removeStopWord(words):
    for word in words:
        if word in stopWord:
            words.remove(word)
    return words

# 加载词林词典
def getDic():
    lines = f.readlines()
    for line in lines:
        line = line.replace('\n', '')
        items = line.split(' ')
        index = items[0]
        if index[-1] == '=':
            symWords.append(items[1:])
        if index[-1] == '#':
            symClassWords.append(items[1:])
getDic()


#扩充词典
def extendDictory(keyWords):
    isOK = True
    flag = False
    IDFFlag = True
    # dic = open("/Users/zuchebao/PycharmProjects/KeywordRecommendationSystem/dict/newWord.txt", "r+", encoding='utf-8')
    dic = open("dict/newWord.txt","r+",encoding='utf-8')
    baseDic = open("venv/lib/python3.7/site-packages/jieba/dict.txt","r",encoding='utf-8')
    baseIDF = open(r'dict/newIDF.txt','r+',encoding='utf-8')
    IDFLines = baseIDF.readlines()
    lines = dic.readlines()
    for keyWord in keyWords:
        if len(lines) is not 0:
            for line in lines :

                if keyWord not in line.strip().split():

                    flag = True
                else:
                    print("匹配到相同的")

                    flag = False
                    break
        else:
            flag = True

        for line in baseIDF:
            if keyWord in line.strip()[0]:
                IDFFlag = False
        if IDFFlag:
            baseIDF.write(keyWord)
            baseIDF.write('\n')

        for line in baseDic.readlines():
            if keyWord in line.strip().split():
                flag = False
        if flag:
            try:
                dic.write(keyWord+" n")
                dic.write('\n')
            except IOError:
                print( "Error: 写入失败")
                isOK = False


            else:
                print
                "内容写入文件成功"
    # jieba.load_userdict("/Users/zuchebao/PycharmProjects/KeywordRecommendationSystem/dict/newWord.txt")
    # jieba.analyse.set_idf_path(r'/Users/zuchebao/PycharmProjects/KeywordRecommendationSystem/dict/newIDF.txt')
    jieba.load_userdict("dict/newWord.txt")
    jieba.analyse.set_idf_path(r'dict/newIDF.txt')
    baseIDF.close()
    dic.close()
    baseDic.close()
    return isOK

# txt = open(r"/Users/zuchebao/Downloads/全职高手【完本】.txt", "r", encoding='utf-8').read()
def getKeyWord(txt):
    score = []
    keyWords = []
    result = []
    keywords_textrank = jieba.analyse.extract_tags(txt, topK=5, withWeight=True, allowPOS=('n', 'nr', 'ns', 'a'), withFlag=False)
    for index,item in enumerate(keywords_textrank):
        score.append(str(keywords_textrank[index][1]))

        print(score)
        keyWords.append(keywords_textrank[index][0])
        print(keyWords)
    result.append(keyWords)
    result.append(score)


    return result

def cutWord(txt):
    words = jieba.cut_for_search(txt,HMM=True)

    uncn = re.compile(r'[\u0061-\u007a,\u0020]')
    en = "".join(uncn.findall(txt.lower()))

    enwords = []  # 建立一个空列表
    index = 0  # 遍历所有的字符
    start = 0  # 记录每个单词的开始位置
    while index < len(en):  # 当index小于p的长度
        start = index  # start来记录位置
        while en[index] != " " and en[index] not in [".", ","]:  # 若不是空格，点号，逗号
            index += 1  # index加一
            if index == len(en):  # 若遍历完成
                break  # 结束
        enwords.append(en[start:index])
        if index == len(en):
            break
        while en[index] == " " or en[index] in [".", ","]:
            index += 1
            if index == len(en):
                break

    print(enwords)
    resutltWord = enwords
    words = removeStopWord(words)
    resutltWord.append(words)


    print(resutltWord)
    return resutltWord


# 通过同义词林获取近义词和同义词
def getSym(w, wordSet):
    # wordSet: 同义词词集或相关词词集
    results = []
    if len(w) == 1:
        for each in wordSet:
            for word in each:
                if w[0] == word:
                    results.append(each)
                    print(each)
                    break
    else:
        for each in wordSet:
            for word in each:
                for i in w:
                    if i == word:
                        results.append(each)
                        print(each)
                        break

    return results


def getSynomymsByCL(keyWords):



       return getSym(keyWords,symWords) + (getSym(keyWords,symClassWords))




# 通过Synonyms获取同义词
def getSynomyms(keyWords):
    resultWords = []
    cutResult = []

    if len(keyWords) == 1:
        cutForSearchWords = jieba.cut_for_search(keyWords[0], HMM=True)
        scoreList = ['0.5']
        if cutForSearchWords:
            wordList = []
            for word in cutForSearchWords:

                scoreList.append('0.5')
                wordList.append(word)
            wordList = removeStopWord(wordList)
            cutResult.append(wordList)
            cutResult.append(scoreList)

        synonymsResult = synonyms.nearby(keyWords[0])
        if synonymsResult[0]:
            for index, score in enumerate(synonymsResult[1]):
                synonymsResult[1][index] = str(score)
                resultWords.append(synonymsResult)
        resultWords.append(cutResult)

    else:
        for word in keyWords:
            scoreList = []
            cutForSearchWords = []
            cutForSearchWords = jieba.cut_for_search(word, HMM=True)
            if cutForSearchWords:
                wordList = []
                for word in cutForSearchWords:
                    scoreList.append('0.5')
                    wordList.append(word)
                wordList = removeStopWord(wordList)
                cutResult.append(wordList)
                cutResult.append(scoreList)
            synonymsResult = []

            synonymsResult = synonyms.nearby(word)
            if synonymsResult[0]:
                for index,score in enumerate(synonymsResult[1]):
                    synonymsResult[1][index] = str(score)
                    resultWords.append(synonymsResult)
            resultWords.append(cutResult)
    return resultWords



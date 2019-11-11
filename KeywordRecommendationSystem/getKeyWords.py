import jieba
import jieba.analyse
from io import *
import synonyms
# import docx
import jieba.posseg as pseg
import re
jieba.load_userdict("dict/newWord.txt")
symWords = []
symClassWords = []
stopWord = []

jieba.analyse.set_stop_words("dict/stopWord.txt")
jieba.analyse.set_idf_path('dict/newIDF.txt')
#加载停用词
def loadStopWord():
    stopWordFile = open("dict/stopWord.txt",'r',encoding='utf-8')

    for line in stopWordFile.readlines():
        stopWord.append(line.strip())

loadStopWord()
def removeStopWords(words):
    result =[]
    for word in words:
        if word not in stopWord:

            result.append(word)

    return result


# 扩充idf，权重根据词的长度，越长的词准确输入的概率越低，所以词越长逆文本频率越高
def extendIDF(keyWords):
    isOK = True
    IDFFlag = True
    baseIDF = open(r'dict/newIDF.txt', 'r+', encoding='utf-8')
    IDFLines = baseIDF.readlines()
    for keyWord in keyWords:
        if len(IDFLines) is not 0:
            for line in IDFLines:

                if keyWord not in line.strip().split():

                    IDFFlag = True
                else:
                    print("匹配到相同的")

                    IDFFlag = False
                    break
        else:
            IDFFlag = True

        if IDFFlag:
            try:
                baseIDF.write(keyWord + " " + str(len(keyWord) * 0.5 + 13.00))
                baseIDF.write('\n')
            except IOError:
                print("Error: 写入失败")
                isOK = False
    baseIDF.close()
    jieba.analyse.set_idf_path('dict/newIDF.txt')
    return isOK


#扩充词典
def extendDictory(keyWords):
    isOK = True
    flag = False
    # dic = open("/Users/zuchebao/PycharmProjects/KeywordRecommendationSystem/dict/newWord.txt", "r+", encoding='utf-8')
    dic = open("dict/newWord.txt","r+",encoding='utf-8')
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

    dic.close()
    return isOK


def getKeyWord(txt):
    score = []
    keyWords = []
    result = []
    keywords_textrank = jieba.analyse.extract_tags(txt, topK=10, withWeight=True, allowPOS=('n', 'nr', 'ns', 'a'), withFlag=False)
    for index,item in enumerate(keywords_textrank):
        score.append(str(keywords_textrank[index][1]))
        keyWords.append(keywords_textrank[index][0])
    result.append(keyWords)
    result.append(score)


    return result

def cutWord(txt):
    words = removeStopWords(list(jieba.cut_for_search(txt,HMM=True)))
    resutltWord = []
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

    resutltWord = enwords

    resutltWord.extend(words)

    return resutltWord


# 通过Synonyms获取同义词
def getSynomyms(keyWords):
    resultWords = []
    cutResult = []

    if len(keyWords) == 1:
        cutForSearchWords = removeStopWords(list(jieba.cut_for_search(keyWords[0], HMM=True)))
        scoreList = []
        if cutForSearchWords:

            for word in cutForSearchWords:
                scoreList.append('0.5')

            cutResult.append(cutForSearchWords)
            cutResult.append(scoreList)

        synonymsResult = list(synonyms.nearby(keyWords[0]))
        if synonymsResult[0]:
            for index, score in enumerate(synonymsResult[1]):
                synonymsResult[1][index] = str(score)
                resultWords.append(synonymsResult)
        resultWords.append(cutResult)

    else:
        for word in keyWords:
            scoreList = []
            cutForSearchWords = []
            cutForSearchWords = removeStopWords(list(jieba.cut_for_search(word, HMM=True)))
            if cutForSearchWords:
                for word in cutForSearchWords:
                    print(word)
                    scoreList.append('0.5')

                cutResult.append(cutForSearchWords)
                cutResult.append(scoreList)
            synonymsResult = []

            synonymsResult = list(synonyms.nearby(word))
            if synonymsResult[0]:
                for index,score in enumerate(synonymsResult[1]):
                    synonymsResult[1][index] = str(score)


                    resultWords.append(synonymsResult)

            resultWords.append(cutResult)
    return resultWords


# 修改权重
def changeWeights(weight,start,end,word = "",):
    isSingle = len(word)
    oldidf = open(r'dict/newIDF.txt', 'r', encoding='utf-8')
    lines = oldidf.readlines()
    oldidf.close()
    newidf = open(r'dict/newIDF.txt', 'w', encoding='utf-8')

    if end is 0:
        end = len(lines)
    if isSingle:
        start = 0
    try:
        for i, line in enumerate(lines):
            if i in range(start, end):
                lineList = line.split()
                change = (float(lineList[1]) + float(weight))
                if isSingle:
                    if lineList[0] == word:
                        if change > 0:
                            newidf.write(lineList[0] + " " + str(change))
                            newidf.write('\n')
                        else:
                            continue
                    else:
                        newidf.write(line)
                    continue

                if change > 0:
                    newidf.write(lineList[0] + " " + str(change))
                    newidf.write('\n')
                else:
                    continue
            else:
                newidf.write(line)
    except IOError:
        return False

    return True

# def readDocx():
#     # category = []
#     file = docx.Document('/Users/zuchebao/Desktop/file.docx')
#     # for para in file.paragraphs:
#     #    print(para.text.split())
#     # getkey.extendDictory(category)
#     for table in file.tables:
#         rows = table.rows
#         for row in rows:
#             keyWord = []
#             key = row.cells[1].text.strip()
#             print(key)
#             keyWord.append(key)
#             if row.cells[2] is not '':
#                 for word in (row.cells[2].text.split('、')):
#                         if (word.strip()) is not '':
#                             for realWord in pseg.cut(word.strip,HMM=True):
#                                 if realWord[1] in ['n', 'nr', 'ns']:
#                                     keyWord.append(realWord[0])
#             for cutWord in (pseg.cut(key,HMM=True)):
#                 if cutWord[1] is ['n', 'nr', 'ns']:
#                     keyWord.append(cutWord[0])
#         keyWord = list(set(keyWord))
#         extendDictory(removeStopWords(keyWord))
#
#

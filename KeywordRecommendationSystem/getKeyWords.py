import jieba
import jieba.analyse
from io import *
import synonyms
import jieba.posseg as pseg
import re
# 读入同义词林
f = open('dict/cilin.txt', 'r', encoding='utf-8')
jieba.load_userdict("dict/newWord.txt")
symWords = []
symClassWords = []

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
    dic = open("dict/newWord.txt","r+",encoding='utf-8')
    baseDic = open("venv/lib/python3.7/site-packages/jieba/dict.txt","r",encoding='utf-8')
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
    jieba.load_userdict("dict/newWord.txt")
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
    for word in words:
        print(word)
        # if word.flag in ["n","nt","nsf","nz","ns","nr"]:
        #     resutltWord.append(word.word)

        resutltWord.append(word)


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
    print(keyWords)
    resultWords = []
    synonymsResult = []
    cutForSearchWordsDic = {}
    if len(keyWords) == 1:
        cutForSearchWords = jieba.cut_for_search(keyWords, HMM=True)
        scoreList =  ['0.5']*len(cutForSearchWords)
        synonymsResult = synonyms.nearby(keyWords[0])
        for index,score in enumerate(synonymsResult[1]):
            synonymsResult[1][index] = str(score)
        resultWords.append(synonymsResult)
    else:
        for word in keyWords:
            synonymsResult = []
            synonymsResult = synonyms.nearby(word)
            for index,score in enumerate(synonymsResult[1]):
                synonymsResult[1][index] = str(score)
            resultWords.append(synonymsResult)
    return resultWords


# print(getSynomyms(["老师","学生"]))
# print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

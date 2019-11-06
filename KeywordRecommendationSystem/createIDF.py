import os.path
import jieba
# 自定义idf
def updateIDF(inputPath:str,originDataCount):
    originIDF = open(r'dict/newIDF.txt','w+',encoding='utf-8')
    originIDFLInes = originIDF.readlines()
    allWordsDic = {}
    if os.path.isdir(inputPath):

        list = os.listdir(inputPath)  # 列出文件夹下所有的目录与文件
        # 所有文章数
        dataCount = len(list) + originDataCount

        for i in range(0, len(list)):
            path = os.path.join(inputPath, list[i])
            if os.path.isfile(path):
                passage = open(path, 'r', encoding='utf-8')
                lines = passage.readlines()
                for line in lines:
                    words = jieba.lcut_for_search(line)
                    for word in words:
                        currentWordValue = allWordsDic.get(word , default=0)
                        resultValue = currentWordValue + 1
                        allWordsDic.update({word: resultValue})


    else:
        passage = open(inputPath, 'r', encoding='utf-8')
        lines = passage.readlines()
        for line in lines:
            words = jieba.lcut_for_search(line)
            for word in words:
                currentWordValue = allWordsDic.get(word, default=0)
                resultValue = currentWordValue + 1
                allWordsDic.update({word: resultValue})

    for key,value in allWordsDic:
        for line in originIDFLInes:
            if key not in line.split()[0]:
                originIDF.write({key,value})


# 创建stopWord

def updateStopWord(inputPath:str):

    stopDir = inputPath
    stopDic = {}
    stopWordFile = open(r'dict/stopWord.txt', 'w+', encoding='utf-8')
    if os.path.isdir(inputPath):
        stopDirList = os.listdir(stopDir)
        for i in range(0, len(stopDirList)):
            path = os.path.join(stopDir, stopDirList[i])
            if os.path.isfile(path):
                stopWord = open(path, 'r', encoding='utf-8')
                lines = stopWord.readlines()
                for line in lines:
                    stopDic.update({line: line})
    else:
        stopWord = open(inputPath, 'r', encoding='utf-8')
        lines = stopWord.readlines()
        for line in lines:
            stopDic.update({line: line})

    for i in stopDic:
        for line in stopWordFile.readlines():
            if i in line :
                break
        stopWordFile.writelines(i)






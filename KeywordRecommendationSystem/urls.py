"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from KeywordRecommendationSystem import getKeyWords
from django.http import JsonResponse
import json


# 获取关键词
def getkey(request):
    txt = request.POST.get("txt")

    if txt is None:
        return JsonResponse({"keyWords":[]})
    else:
        key = getKeyWords.getKeyWord(txt)
        return JsonResponse({"keyWords": key})

# 获得分词结果
def getCutWords(request):
    txt = request.POST.get('text')

    if txt is None:
        return JsonResponse({"words": []})
    else:
        words = getKeyWords.cutWord(txt)
        if len(words) is 0:
            return JsonResponse({"words": txt})
        else:
            return JsonResponse({"words": words})

# 获取同义词和相关系数
def getSynonyms(request):
    keysWords = request.GET.get("keyWords")
    if keysWords is None:
        return JsonResponse({"synonymsWords": []})
    else:
        realKeyWords = keysWords.split(",")
        synonymsWords = getKeyWords.getSynomyms(realKeyWords)
        print(synonymsWords)
        return JsonResponse({"synonymsWords": synonymsWords})

#获取同义词或同类词
def getSynonymsByCL(request):
    keyWords = request.GET.get("keyWords")
    realKeyWords = keyWords.split(",")
    for i in realKeyWords:
        print(i)
    print(keyWords)

    result = getKeyWords.getSynomymsByCL(realKeyWords)
    print(result)
    return JsonResponse({"synonymsWords": result})


def extendDictory(request):
    keyWordsStr = request.POST.get("keyWords")
    realKeyWords = []
    if keyWordsStr is None:
        return JsonResponse({"status":False})
    else:
        KeyWords = keyWordsStr.split(",")
        keyWordsSet = set(KeyWords)

        for words in keyWordsSet:
            words = words.strip()
            realKeyWords.append(words)
            isExtend = getKeyWords
        result = getKeyWords.extendDictory(realKeyWords) and getKeyWords.extendIDF(realKeyWords)
        return JsonResponse({"status": result})



def changeWeight(request):
    """
    修改单个词权重时传入word
    修改多个词权重时传入 start,end ,不传默认为修改所有

    单个和多个都必须传weight 为调整的幅度（正负表示加减）
    如果修改后结果小于0，这个词会被删除
    :param request:
    :return:
    """
    word = request.GET.get("word")
    weight = request.GET.get("weight")
    start = request.GET.get("start")
    end = request.GET.get("end")
    if weight is None:
        return JsonResponse({"status": False})
    if word is not None:
        status = getKeyWords.changeWeights(float(weight),0,0,str(word))
    else:
        if start is None:
            start = 0
        if end is None:
            end = 0
        status = getKeyWords.changeWeights(float(weight),int(start),int(end))
    return JsonResponse({"status":status})





urlpatterns = [
    path('/', admin.site.urls),
    # 初始化
    path("getKeyWord", getkey),
    # 近义词
    path("getSynonyms", getSynonyms),
    # 近义词
    path("getSynonymsByCL", getSynonymsByCL),
    # 搜索切词
    path("getWords", getCutWords),
    # 扩充词典
    path("extendDictory", extendDictory),
    # 修改权重
    path("changeWeight",changeWeight)

]

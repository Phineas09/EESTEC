import lxml.html as LH
from lxml import etree
import requests
import typing
import string
from googlesearch import search
import re
import html
from utils import *

def formatString(_str) -> str:
    ret = re.sub("\[[0-9a-zA-Z]+\]", "", _str)
    ret = re.sub("\(.+\)", " ", ret)

    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, ret))

def stripHTML(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

class GenericScraper:

    @classmethod
    def getParagraphList(self, url: str,
                         paragraphsCount: int) -> typing.List[str]:
        topParagraphs = []
        try:
            r = requests.get(url, timeout=5)
            r.encoding = "iso-8859-1"
      
            if (r.status_code == 200):
                root = LH.fromstring(r.content)
                for paragraph in root.xpath('//p[not(@*)]'):
                    if (len(topParagraphs) == paragraphsCount):
                        return topParagraphs
                    paragraphText = stripHTML(etree.tostring(paragraph).decode('iso-8859-1'))
                    if (paragraphText != None):
                        paragraphText =paragraphText.replace('\r\n', " ") #
                        paragraphText =paragraphText.replace('\n', " ") #
                        paragraphText =paragraphText.replace('\t', " ") #
                        paragraphText = html.unescape(paragraphText)
                        topParagraphs.append(formatString(paragraphText).lower())
        except:
            return topParagraphs
        return topParagraphs
def corectList(responseList):
    while("" in responseList) :
        responseList.remove("")
    uniqueList = set(responseList)
    corectedList = []
    print(uniqueList)
    for i in (list(uniqueList)):
        for j in responseList:
            if i in j or i == j:
                corectedList.append(i)
    print("Corected List: ")
    print(corectedList)
    return corectedList
def most_common(lst):
    return max(set(lst), key=lst.count) or ""
def Query(question, pipeline):
    responseList = []
    pageUrl = search(question, num_results=5)
    pipeline.setQuestionToAnswer(question)
    for url in pageUrl:
        paragraphList = GenericScraper.getParagraphList(url, 10)
        #compose = ' '.join(_ for _ in paragraphList)
        #print(paragraphList)
        if (len(paragraphList) == 0):
            continue
        
        for _ in paragraphList:
            pipeline.setStringToProcess(_)
            #response = pipeline.answerWithSummarization()
            #print(_)
            try:
                response = pipeline.answerNoSummarization()
                responseList.append(response["answer"])
            except:
                continue
        text = ""
        for _ in paragraphList:
            text += _
            pipeline.setStringToProcess(text)
            try:
                response = pipeline.answerNoSummarization()
                responseList.append(response["answer"])
            except:
                continue
    responseList = corectList(responseList)
    print("Corected List: ")
    print(responseList)
    return most_common(responseList)
    
def QueryMultipleChoice(question, choices, pipeline, isNumeric):
    responseList=[]
    pageUrl = search(question, num_results=5)
    pipeline.setQuestionToAnswer(question)
    for url in pageUrl:
        paragraphList = GenericScraper.getParagraphList(url, 10)
        #compose = ' '.join(_ for _ in paragraphList)
        if (len(paragraphList) == 0):
            continue
        for _ in paragraphList:
            pipeline.setStringToProcess(_)
            #response = pipeline.answerWithSummarization()
            try:
                response = pipeline.answerNoSummarization()
                responseList.append(response["answer"])
            except:
                continue
            
        text = ""
        for _ in paragraphList:
            text += _
            pipeline.setStringToProcess(text)
            try:
                response = pipeline.answerNoSummarization()
                responseList.append(response["answer"])
            except:
                continue
    responseList = corectList(responseList)
    res = most_common(responseList)
    if(isNumeric):
        try:
            res = getNumberFromWord(res)
        except:
            pass
    return getClosestString(choices,str(res))
    
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
            if (r.status_code == 200):
                root = LH.fromstring(r.content)
                for paragraph in root.xpath('//p[not(@*)]'):
                    if (len(topParagraphs) == paragraphsCount):
                        return topParagraphs
                    paragraphText = stripHTML(etree.tostring(paragraph).decode('utf-8'))
                    if (paragraphText != None):
                        topParagraphs.append(
                            formatString(paragraphText.replace("\n", " ")))
        except:
            return topParagraphs
        return topParagraphs

def most_common(lst):
    return max(set(lst), key=lst.count) or ""
def Query(question, pipeline):
    responseList = []
    pageUrl = search(question, num_results=5)
    pipeline.setQuestionToAnswer(question)
    for url in pageUrl:
        paragraphList = GenericScraper.getParagraphList(url, 5)
        #compose = ' '.join(_ for _ in paragraphList)
        print(paragraphList)
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
    return most_common(responseList)
    
def QueryMultipleChoice(question, choices, pipeline, isNumeric):
    responseList=[]
    pageUrl = search(question, num_results=5)
    pipeline.setQuestionToAnswer(question)
    for url in pageUrl:
        paragraphList = GenericScraper.getParagraphList(url, 5)
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
    res = most_common(responseList)
    if(isNumeric):
        res = getNumberFromWord(res)
    return getClosestString(choices,str(res))
    
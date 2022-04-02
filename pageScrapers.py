import lxml.html as LH
from lxml import etree
import requests
import typing
import string
import re

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
        r = requests.get(url)
        if (r.status_code == 200):
            root = LH.fromstring(r.content)
            topParagraphs = []
            for paragraph in root.xpath('//p[not(@*)]'):
                if (len(topParagraphs) == paragraphsCount):
                    return topParagraphs
                paragraphText = stripHTML(etree.tostring(paragraph).decode('utf-8'))
                if (paragraphText != None):
                    #print(paragraphText)
                    #print("-" * 100)
                    topParagraphs.append(
                        formatString(paragraphText.replace("\n", " ")))
        return topParagraphs

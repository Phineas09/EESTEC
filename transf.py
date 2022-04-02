import neuralPipeline
from googlesearch import search
from bs4 import BeautifulSoup as bs
import requests
import wikipediaapi
import re
import string


def format_string(_str) -> str:
    ret = re.sub("\[[0-9a-zA-Z]+\]", "", _str)
    ret = re.sub("\(.+\)", " ", ret)

    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, ret))


query = '"site:en.wikipedia.org" How many planets are in our solar system?'
url = next(search(query, tld="com", num=10, stop=10, pause=2))
link = requests.get(url)
content = link.content

html = bs(content, features="lxml")

title = html.select("#firstHeading")[0].text
print("Title:", title)

try:
    infobox = html.find('table', attrs={'class': 'infobox'}).select('tr')

    print("Infobox text: ")
    infobox_text = ""
    for item in infobox:
        try:
            row = item.find('th').text + " " + item.find('td').text
            infobox_text += row + "\n"
        except:
            continue
    #print(infobox)
except:
    print("Infobox inexistent.")

wiki = wikipediaapi.Wikipedia('en')
page = wiki.page(title)

page_text = page.text
page_summ = page.summary

page_text_list = page_text.split("\n")
page_text = ""
for line in page_text_list:
    if line == "See also":
        break
    page_text += line

page_text_noref = format_string(page_text)
page_summ_noref = format_string(page_summ)
page_infobox_noref = format_string(infobox_text)

pageList = [page_text_noref, page_summ_noref, page_infobox_noref]
pipeline = neuralPipeline.NeuralPipeline()
pipeline.setQuestionToAnswer("How many planets are in our solar system?")
print("-" * 100)
for text in pageList:
    pipeline.setStringToProcess(text.replace("\n", " "))
    response = pipeline.answerWithSummarization()
    print(text) 
    print("-" * 100)
    print(response[0])
    print("-" * 100)
    print(response[1])
    print("-" * 100)

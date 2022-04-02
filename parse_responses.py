from googlesearch import search
from bs4 import BeautifulSoup as bs
import requests 
import wikipediaapi
#from transformers import pipeline

#slist = list(search("fall of constantionpole site:wikipedia.org"))
slist = list(search("how many planets are in our solar system site:wikipedia.org"))
link = requests.get(slist[0])
content = link.content

html = bs(content)
#firstp = html.body.find('div', attrs={'class':'mw-body-content mw-content-ltr'}).select("p")
#for idx, p in enumerate(firstp):
#    if idx > 5:
#        break
#    print (idx, ": ", p.text)

title = html.select("#firstHeading")[0].text
print("Title:", title)

try:
    infobox = html.find('table', attrs={'class': 'infobox'}).select('tr')
    infobox_th = html.find('table', attrs={'class': 'infobox'}).select('th')
    print("Infobox len: ", len(infobox))
    print("Infobox th len: ", len(infobox_th))

    print("Infobox text: ")
    for li in infobox:
        print(li.text)
    #print(infobox)
except:
    print("Infobox inexistent.")

wiki = wikipediaapi.Wikipedia('en')
page = wiki.page(title)
#print(page.summary)


#summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#
#summary = summarizer(page.summary, max_length=130, min_length=30, do_sample=False)
#print(summary)
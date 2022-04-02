from googlesearch import search
from bs4 import BeautifulSoup as bs
import requests 
import wikipediaapi
import re
import string
#from transformers import pipeline

def format_string(_str) -> str:
    ret = re.sub("\[[0-9a-zA-Z]+\]","", _str)
    ret = re.sub("\(.+\)", " ", ret)

    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, ret))

slist = list(search("when was the fall of constantionpole site:wikipedia.org"))
#slist = list(search("how many planets are in our solar system site:wikipedia.org"))
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
    # items in infobox are of type <tr><th>title</th><td>info about title</td></tr>
    infobox = html.find('table', attrs={'class': 'infobox'}).select('tr')

    print("Infobox text: ")
    #print(infobox[1])
    #print(infobox[1].find('th').text)
    #print(infobox[1].find('td').text)
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

with open("page_text_noref.txt", "w") as f:
    f.write(page_text_noref)

with open("page_summ_noref.txt", "w") as f:
    f.write(page_summ_noref)

with open("page_infobox_noref.txt", "w") as f:
    f.write(page_infobox_noref)
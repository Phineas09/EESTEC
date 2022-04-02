from googlesearch import search
from bs4 import BeautifulSoup as bs
import requests

# QUESTION = "Who discovered penicillin?"
QUESTION = "When did Hitler die?"
# STRING GOL LA QUESTIOn

slist = list(search(QUESTION))

for _link in slist:
    link = requests.get(_link)
    print(link.status_code)
    if link.status_code == 200:  # some sites return 403
        break

soup = bs(link.content, "html.parser")
allp = soup.find_all("p")

# content = link.content

# html = bs(content, "html.parser")
# print(html.prettify())

f = open("f.html", "w")
for p in allp:
    print(p)
    f.write(p.text + "-"*20)
#f.write(allp.text)
f.close()

# first_paragraphs = html.body.find_all("p")
# for p in first_paragraphs:
#     print(p)

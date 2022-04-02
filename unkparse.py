from googlesearch import search
from bs4 import BeautifulSoup as bs
import requests
import transformers

# QUESTION = "Who discovered penicillin?"
QUESTION = "When did Hitler die?"
# STRING GOL LA QUESTIOn

question_answerer = transformers.pipeline('question-answering')
slist = list(search(QUESTION, num_results=6, lang="en"))
print(slist)
print(len(slist))
exit(0)
for _link in slist:
    link = requests.get(_link)
    print(link.status_code)
    if link.status_code == 200:  # some sites return 403
        break

soup = bs(link.content, "html.parser")
allp = soup.find_all("p")

f = open("f.html", "w")
answer_list = []
for idx, p in enumerate(allp):
    if idx > 3:
        break
    print(p)
    try:
        print("Processing..")
        answer_list.append(question_answerer({
            'question': QUESTION,
            'context': p.text
        }))
    except:
        continue

print(answer_list)
f.close()

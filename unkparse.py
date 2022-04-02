from googlesearch import search
from bs4 import BeautifulSoup as bs
import requests
import transformers

# QUESTION = "Who discovered penicillin?"
QUESTION = "When did Hitler die?"
# QUESTION_LIST = ["Who became the first king of a united Italy in 1861?", "Who discovered penicillin?",
#                  "Where is the northernmost point of land in the world?"]
# QUESTION_LIST = ["Who discovered penicillin?"]

# STRING GOL LA QUESTION

question_answerer = transformers.pipeline('question-answering')
slist = list(search(QUESTION, num_results=6, lang="en"))
for _link in slist:
    link = requests.get(_link)
    print(_link)
    # print(link.status_code)
    if link.status_code == 200:  # some sites return 403
        break

with open("link-content.html", "w") as f:
    f.write(link.content.decode("utf-8"))
soup = bs(link.content, "html.parser")
allp = soup.find_all("p")

f = open("f.html", "w")
print(QUESTION)
answer_list = []
idx = 0
for idx, p in enumerate(allp):
    if idx > 3:
        break
    try:
        print(p)
        answer_list.append(question_answerer({
            'question': QUESTION,
            'context': p.text
        }))
    except:
        continue

print(answer_list)
f.close()

from googlesearch import search
from bs4 import BeautifulSoup as bs
import requests
import transformers

# QUESTION = "Who discovered penicillin?"
QUESTION = "What Japanese emperor reigned during World War II?"
THRESHOLD = 0.7
# QUESTION_LIST = ["Who became the first king of a united Italy in 1861?", "Who discovered penicillin?",
#                  "Where is the northernmost point of land in the world?"]
# QUESTION_LIST = ["Who discovered penicillin?"]

# STRING GOL LA QUESTION


def is_over_threshold(answer_list: list):  # if one ans is over threshold, do not check another site
    for ans in answer_list:
        if ans['score'] > THRESHOLD:
           return ans['answer']
    return ""


def answer_question(question: str) -> str:
    question_answerer = transformers.pipeline('question-answering')
    slist = list(search(QUESTION, num_results=6, lang="en"))
    for _link in slist:
        link = requests.get(_link)
        print(_link)
        # print(link.status_code)
        if link.status_code != 200:  # some sites return 403
            continue

        # with open("link-content.html", "w") as f:
        #     f.write(link.content.decode("utf-8"))
        soup = bs(link.content, "html.parser")
        allp = soup.find_all("p")

        # print(QUESTION)

        answer_list = []
        for idx, p in enumerate(allp):
            if idx > 5:
                break
            try:
                print(p)
                answer_list.append(question_answerer({
                    'question': QUESTION,
                    'context': p.text
                }))
            except:
                continue

        ans = is_over_threshold(answer_list)
        if ans != "":
            definitive_answer = ans
            return definitive_answer
            # break  # ?????????????????????/

        answer_with_max_score = answer_list[0]
        max_score = -1
        for ans in answer_list:
            if ans['score'] > max_score:
                max_score = ans['score']
                answer_with_max_score = ans['answer']
        print(answer_list)
    print(answer_list)
    # print(definitive_answer)
    return answer_with_max_score

print(answer_question(QUESTION))

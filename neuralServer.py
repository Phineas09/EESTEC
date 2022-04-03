from flask import *
import neuralPipeline
from pageScrapers import *
from utils import *
app = Flask(__name__)

pipeline = neuralPipeline.NeuralPipeline()

@app.route("/sanity", methods=['GET'])
def sanityResponse():
    return Response("", status=200, mimetype='application/json')

@app.route('/question', methods=['POST'])
def summary():
    data = request.get_json()
    question = data['question_text']
    if(question[0:2].lower() == 'who'):
        question+='"wikipedia"';
    answer_type = data['answer_type']
    question_type = data['question_type']
    answer_choices = data['answer_choices']
    result = {'Error':'Question type not recognized'}
    isWho = False
    if(question[0:3].lower() == 'who'):
        isWho = True;
    if(question_type == 'direct_answer'):
        result = Query(question, pipeline, isWho)
    elif (question_type == 'multiple_choice'):
        isNumeric = False
        if(answer_type == 'numeric'):
            isNumeric = True
        result = QueryMultipleChoice(question, answer_choices, pipeline, isNumeric, isWho)
        result = result[0]
    else:
        result = {'Error':'Question type not recognized'}
    #if(question[0:4].lower() == 'when'):
    #    result = getYear(result)
    if(answer_type == 'numeric'):
        try:
            result = getNumberFromWord(result)
        except:
            pass
    result = {"answer":result}
    return jsonify(result)

@app.errorhandler(500)
def internal_server_error():
    return jsonify({"answer" : ""})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)
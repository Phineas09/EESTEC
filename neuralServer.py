from flask import *
import neuralPipeline

app = Flask(__name__)


pipeline = neuralPipeline.NeuralPipeline()


@app.route('/summary', methods=['POST'])
def summary():
    data = request.get_json()
    #pipeline.setQuestionToAnswer(question)
    pipeline.setContext(data["context"], data["question"])
    response = pipeline.answerWithSummarization()
    return jsonify(response[1])

@app.route('/noSummary', methods=['POST'])
def noSummary():
    data = request.get_json()
    pipeline.setContext(data["context"], data["question"])
    response = pipeline.answerNoSummarization()
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)
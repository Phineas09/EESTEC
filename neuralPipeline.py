import neuralLayers

class NeuralPipeline():

    _summarizerLayer = None
    _answererLayer = None
    _stringToProcess = None
    _questionToAnswer = None

    def __init__(self):
        self._summarizerLayer = neuralLayers.Summarizer()
        self._answererLayer = neuralLayers.QuestionAnswerer()

    def setStringToProcess(self, stringToProcess: str) -> None:
        self._stringToProcess = stringToProcess

    def setQuestionToAnswer(self, questionToAnswer: str) -> None:
        self._questionToAnswer = questionToAnswer

    def setContext(self, stringToProcess: str, questionToAnswer: str) -> None:
        self.setStringToProcess(stringToProcess)
        self.setQuestionToAnswer(questionToAnswer)

    def answerWithSummarization(self):
        summarizedString = self._summarizerLayer.querryResponse(
            self._stringToProcess)
        
        response = self._answererLayer.querryResponse(summarizedString,
            self._questionToAnswer)

        return([summarizedString, response])

    def answerNoSummarization(self):
        response = self._answererLayer.querryResponse(self._stringToProcess,
            self._questionToAnswer)

        return(response)

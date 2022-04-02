from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import abc


class BaseLayer(abc.ABC):

    _model = None

    def __init__(self, model):
        self._model = model

    @abc.abstractmethod
    def querryResponse(self, stringToProcess: str) -> str:
        raise NotImplementedError()

'''

class Summarizer(BaseLayer):

    _tokenizer = None

    def __init__(self):
        super().__init__(
            AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn"))

        self._tokenizer = AutoTokenizer.from_pretrained(
            "facebook/bart-large-cnn")

    def querryResponse(self, stringToProcess: str) -> str:
        if (stringToProcess):
            inputs = self._tokenizer([stringToProcess],
                                     truncation='longest_first',
                                     return_tensors="pt")
            summary_ids = self._model.generate(inputs["input_ids"])
            finalToken = self._tokenizer.batch_decode(
                summary_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False)
            if (len(finalToken) > 0):
                return finalToken[0]
        raise Exception(
            "Something wrong happened! @Summarizer -> querryResponse")
'''

# This works better for planetary question

class Summarizer(BaseLayer):

    def __init__(self):
        super().__init__(
            pipeline("summarization",
                     model="facebook/bart-large-cnn",
                     truncation=True))

    def querryResponse(self, stringToProcess: str) -> str:
        if (stringToProcess):
            response = self._model(stringToProcess,
                                   max_length=130, # Maybe delete this
                                   min_length=30,  # Maybe delete this
                                   do_sample=False)
            return (response[0]['summary_text'])
        raise Exception(
            "Something wrong happened! @Summarizer -> querryResponse")

class QuestionAnswerer(BaseLayer):

    def __init__(self):
        super().__init__(pipeline('question-answering'))

    #def loadQuestion(self, questionString: str) -> str:
    #    self._questionString = questionString

    def querryResponse(self, stringToProcess: str, questionString: str) -> str:
        if (stringToProcess and questionString != None):
            response = self._model({
                'question': questionString,
                'context': stringToProcess
            })
            return response
        raise Exception(
            "Something wrong happened! @QuestionAnswerer -> querryResponse")

from flair.data import Sentence
from flair.models import SequenceTagger

# load the model you trained
# model = SequenceTagger.load("../research_notebooks/flair_model/best-model.pt")
model = SequenceTagger.load("research_notebooks/flair_model/best-model.pt")
# sentence = Sentence("Get my deals with September & Co. between Jan. 4th and Jan. 11th.", use_tokenizer=True)


def tag_ner(text):
    sentence = Sentence(text, use_tokenizer=True)
    model.predict(sentence)
    tagged_str = sentence.to_tagged_string()
    print(tagged_str)
    return tagged_str


def tag_sentences(sentences):
    sentences_all = [Sentence(sent, use_tokenizer=True) for sent in sentences]
    model.predict(sentences_all, mini_batch_size=32)
    return [result.to_tagged_string() for result in sentences_all]
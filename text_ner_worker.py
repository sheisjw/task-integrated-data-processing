import faust
from typing import List
import requests
import json


app = faust.App(
    'text_ner_app',
    broker='kafka://localhost:9092',
    value_serializer='raw',
)

kafka_topic = app.topic('topic_b')

url_1 = "http://0.0.0.0:3000/tag_ner"
url_2 = "http://0.0.0.0:3000/tag_sentences"
headers = {
  'Content-Type': 'application/json'
}


@app.agent(kafka_topic)
async def process(sentences):
    # async for value in sentences:
    #     value_str = value.decode("utf-8")
    #     print(value_str)
    #     payload = {"text": value_str}
    #     response = requests.request("POST", url_1, headers=headers, data=json.dumps(payload))
    #     print('ner result: ' + str(response.text))
    async for value in sentences:
        value_str = value.decode("utf-8")
        # the input for url2 is a list of sentences
        payload = {"text": [value_str]}
        response = requests.request("POST", url_2, headers=headers, data=json.dumps(payload))
        print('ner result: ' + str(response.text))

if __name__ == '__main__':    
    # run the consumer
    app.main()

from flask import Flask, jsonify, abort, request
from data_processing.tag_ner import tag_ner, tag_sentences
import time

app = Flask(__name__)


@app.route('/tag_ner', methods=['POST'])
def predict_ner():
    # example input of this endpoint is {"text": "Find customer with account name BMW"}
    raw_data = request.get_json()
    if not request.json or 'text' not in request.json:
        abort(400)
    data = raw_data.get('text')
    start = time.time()
    results = tag_ner(data)
    end = time.time()
    print('applying tagging takes', (end - start))
    return jsonify(status=200, result=results)


@app.route('/tag_sentences', methods=['POST'])
def predict_sentences():
    # example input of this endpoint is {"text": ["Find customer with account name BMW"]}
    raw_data = request.get_json()
    if not request.json or 'text' not in request.json:
        abort(400)
    data = raw_data.get('text')
    start = time.time()
    results = tag_sentences(data)
    end = time.time()
    print('applying tagging takes', (end - start))
    return jsonify(status=200, result=results)


if __name__ == '__main__':
    app.run(debug=True)

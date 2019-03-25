from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask_cors import CORS, cross_origin
import os

from determinist_autosuggest import autoSuggestor

prefix = u""

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

link_path = "./data/data_processed_fixed.txt"
stops_path = "./data/stops.txt"

data_dir = os.path.abspath(os.path.join(__file__, os.pardir))
stops_path = os.path.join(data_dir, stops_path)
link_path = os.path.join(data_dir, link_path)

auto = autoSuggestor(link_path, stops_path)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def index_post():
    text = request.form['text']
    res = auto.auto_suggest(text)
    res2 = auto.auto_suggest_fast(text)

    return render_template("index.html", prefix = text, result = res, result2 = res2)

@app.route('/api/suggest', methods=['GET'])
@cross_origin()
def suggest():
    input = request.args.get('q')
    results =  auto.auto_suggest_fast(input)
    results = [r[0] for r in results]
    return jsonify(results)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 20000)

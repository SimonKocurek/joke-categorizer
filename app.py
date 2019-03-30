import os

from flask import Flask, jsonify, request

from nn import categorize
from vision import get_words,get_words_url

HOMEDIR = "D:\memes"
JSONS = "D:\jsons"
app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/categories', methods=['GET', 'POST'])
def categories():
    img = request.files.get('file')
    words = get_words(img)
    ctg = categorize(words)
    filename = img.filename
    img.save(os.path.join(HOMEDIR, filename))
    filename = os.path.join(os.path.splitext(filename)[0], '.json')
    json = open(filename,'w+')
    json.write(jsonify(ctg))
    return jsonify(ctg)

@app.route('/categoriesUrl')
def categoriesurl():
    img = request.form.get('img')
    words = get_words_url(img)
    ctg = categorize(words)
    return jsonify(words)


if __name__ == '__main__':
    app.run(debug=True)

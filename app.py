from flask import Flask, jsonify, request
from vision import get_words
from nn import categorize

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/categories')
def categories():
    img = request.form.get('img')
    words = get_words(img)
    ctg = categorize(words)
    return jsonify(ctg)


if __name__ == '__main__':
    app.run(debug=True)

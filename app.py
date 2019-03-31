import os,pickle

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

from image import get_gallery
from nn import categorize
from vision import get_words, get_words_url

HOMEDIR = "./static/memes"
JSONS = "./static/jsons"
app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/categories', methods=['GET', 'POST'])
def categories():
    img = request.files['file']
    filename = img.filename
    img.save(os.path.join(HOMEDIR, filename))
    words = get_words(os.path.join(HOMEDIR, filename))
    ctg = categorize(words)
    filename = os.path.join(JSONS,os.path.splitext(filename)[0] + '.json')
    with open(filename,'w+') as json:
        json.write(str(ctg))
    return jsonify(ctg)


@app.route('/categoriesUrl')
def categoriesurl():
    img = request.form.get('img')
    words = get_words_url(img)
    ctg = categorize(words)
    import requests

    img_data = requests.get(img).content
    filename = secure_filename(img)
    img_data.save(os.path.join(HOMEDIR, filename) + '.jpg')
    filename = os.path.join(JSONS,filename + '.json')
    json = open(filename, 'w+')
    json.write(str(ctg))
    return jsonify(ctg)


@app.route('/image/<string:path>')
def send_image(path):
    return send_image(os.path.join(HOMEDIR, path))


@app.route('/listimages')
def list():
    list = get_gallery(HOMEDIR, JSONS)
    return jsonify(list)


if __name__ == '__main__':
    app.run(debug=True)

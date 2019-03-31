import os,pickle

from flask import Flask, jsonify, request
from flask_cors import cross_origin  # flask-Cors

from image import get_gallery
from nn import categorize
from vision import get_words, get_words_url

HOMEDIR = "./static/memes"
JSONS = "./static/jsons"
img_id = 1
app = Flask(__name__, static_url_path='/static')

try:
    os.mkdir(HOMEDIR)
    os.mkdir(JSONS)
except FileExistsError:
    pass

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
    global img_id
    img = request.form.get('img')
    words = get_words_url(img)
    ctg = categorize(words)
    import requests

    img_data = requests.get(img).content
    filename = 'image' + str(img_id)
    img.save(os.path.join(HOMEDIR, filename) + '.jpg')
    img_id += 1
    filename = os.path.join(JSONS,filename + '.json')
    json = open(filename, 'w+')
    json.write(str(ctg))
    return jsonify(ctg)


@app.route('/image/<string:path>')
def send_image(path):
    return send_image(os.path.join(HOMEDIR, path))


@app.route('/listimages')
def l():
    list = get_gallery(HOMEDIR, JSONS)
    return jsonify(list)


if __name__ == '__main__':
    app.run(debug=True)

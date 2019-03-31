import os

from flask import Flask, jsonify, request

from image import get_gallery
from nn import categorize
from vision import get_words,get_words_url

HOMEDIR = "C:\\Users\\domin\\memes"
JSONS = "C:\\Users\\domin\\jsons"
img_id = 1
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
    global img_id
    img = request.form.get('img')
    words = get_words_url(img)
    ctg = categorize(words)
    import requests

    img_data = requests.get(img).content
    filename = 'image' + str(img_id)
    img_id += 1
    with open(os.path.join(HOMEDIR,filename+'.jpg'), 'wb') as handler:
        handler.write(img_data)
    filename = os.path.join(JSONS,filename + '.json')
    json = open(filename, 'w+')
    json.write(jsonify(ctg))
    return jsonify(ctg)


@app.route('/image/<string:path>')
def send_image(path):
    return send_image(os.path.join(HOMEDIR, path))


@app.route('/listimages')
def list():
    list = get_gallery(HOMEDIR,JSONS)
    return jsonify(list)


if __name__ == '__main__':
    app.run(debug=True)

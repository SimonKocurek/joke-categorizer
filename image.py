import os

from datetime import datetime

from app import HOMEDIR, JSONS


def get_gallery():
    json = {}
    filelist = []
    for root, dirs, files in os.walk(HOMEDIR):
        for file in files:
            item = {}
            item['path'] = file
            tags = open(os.path.join(JSONS,os.path.join(os.path.splitext(file)[0], '.json')))
            filelist.append(item)

    json['files'] = filelist
    return json



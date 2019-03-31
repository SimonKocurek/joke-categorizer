import os


def get_gallery(homedir, jsons):
    json = {}
    filelist = []
    for root, dirs, files in os.walk(homedir):
        for file in files:
            item = {}
            item['path'] = file
            tags = open(f'{jsons}/{os.path.splitext(file)[0]}.json')
            item['tags'] = tags.read()
            filelist.append(item)

    json['files'] = filelist
    return json

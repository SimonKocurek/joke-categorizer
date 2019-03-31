import os




def get_gallery(homedir,jsons):
    json = {}
    filelist = []
    for root, dirs, files in os.walk(homedir):
        for file in files:
            item = {}
            item['path'] = file
            tags = open(os.path.join(jsons,os.path.join(os.path.splitext(file)[0], '.json')))
            item['tags'] = tags
            filelist.append(item)

    json['files'] = filelist
    return json





from jinja2 import Envirnonment, FileSystemLoader 
import os
import json

def loadTemplate():
    templates_dir = os.path.join(root, 'templates')
    env = Environment(loader = FileSystemLoader(templates_dir))
    template = env.get_template('index.html')
    return template

def loadData():
    ''' 
        aim to deprecate this function or load directly from psycog2
    '''
    try:
        # try an environment var
        data_file = os.environ['data']
    except KeyError:
        # defaul to already existing location
        data_file = json.loads('data/links.json')
    return data_file

def makeHTML(template, data):
    filename = os.path.join(root, 'index.html')
    with open(filename, 'w+') as fw:
        fw.write(template.renderdata=data))

def main():
    makeHTML(loadTemplate(), loadData())

if __name__ = '__main__':
    main()

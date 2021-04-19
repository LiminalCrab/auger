from jinja2 import Environment, FileSystemLoader 
import os
import json
import psycopg2

#open initial connection
conn = psycopg2.connect("")

#open initial cursor
cur = conn.cursor()

def loadTemplate():
    templates_dir = os.path.join(os.getcwd(), 'templates')
    env = Environment(loader = FileSystemLoader(templates_dir))
    template = env.get_template('template')
    return template

def loadData():
    try:
        print("TEST")

    except KeyError:
        print("ERROR")
        
    #Let's depreciate.
    
    
    
    
    ''' 
        aim to deprecate this function or load directly from psycog2

    try:
        # try an environment var
        data_file = os.environ['data']
    except KeyError:
        # defaul to already existing location
        data_file = 'data/links.json'
    with open(data_file, 'r') as dfr:
         data_file = json.load(dfr)
    return data_file
'''
def makeHTML(template, data):
    filename = os.path.join(os.getcwd(), 'index.html')
    with open(filename, 'w+') as fw:
        fw.write(template.render(data=data))

def main():
    makeHTML(loadTemplate(), loadData())

if __name__ == '__main__':
    main()

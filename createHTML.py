from jinja2 import Environment, FileSystemLoader 
import psycopg2
import os
import json

def loadTemplate():
    templates_dir = os.path.join(os.getcwd(), 'templates')
    env = Environment(loader = FileSystemLoader(templates_dir))
    template = env.get_template('template')
    return template

def loadData():
    # move this into a psycopg2 module?
    #open initial connection
    conn = psycopg2.connect("")
    #open initial cursor
    cur = conn.cursor()

    ORDER_BY_DATE_TO_JSON = '''
        SELECT 
            json_build_object(
                'id', posts.id,
                'title', posts.host_title,
                'url', posts.post_url,
                'date', posts.post_date
            ) FROM posts ORDER BY post_date DESC;
    '''
   
    print("ORDER.PY: SORTING DATES")
    cur.execute(ORDER_BY_DATE_TO_JSON)
    data = list(map(lambda x: x[0], cur.fetchall()))
    
    cur.close()
    conn.close()
    print(data)
    return data

def makeHTML(template, data):
    filename = os.path.join(os.getcwd(), 'index.html')
    with open(filename, 'w+') as fw:
        fw.write(template.render(data=data))

def main():
    makeHTML(loadTemplate(), loadData())

if __name__ == '__main__':
    main()

from jinja2 import Environment, FileSystemLoader
from datetime import datetime
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
    template = env.get_template('test_template')
    return template
    
def loadData():
# Let's grab some data from postgres
    try:
        
        q_select = '''
        SELECT host_title, post_url, to_char(post_date, 'DD Mon YYYY') 
        FROM posts ORDER BY post_date DESC;
        '''
        cur.execute(q_select)
        origin_data = [cur.fetchall()]
        
    except:
        
        print("EXCEPTION THROWN")
        print("ORIGIN DATA", origin_data)
        print("Are you connected to a database?")
        
    for row in origin_data:
        
        processed_data = [x for x in row]
        
        return processed_data
    
        
def makeHTML(template, data):
    filename = os.path.join(os.getcwd(), 'test.html')
    with open(filename, 'w+') as fw:
        fw.write(template.render(data=data))

def main():
    makeHTML(loadTemplate(), loadData())

if __name__ == '__main__':
    main()

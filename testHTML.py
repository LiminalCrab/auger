from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os
import json
import psycopg2

#open initial connection
conn = psycopg2.connect("")

#open initial cursor
cur = conn.cursor()

def get_data():
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
        
    for row in origin_data:
        
        processing_data = [x for x in row]
        print("DATA", processing_data)
    
        
#def makeHTML(template, data):
    #filename = os.path.join(os.getcwd(), 'test.html')
    #with open(filename, 'w+') as fw:
        #fw.write(template.render(data=data))

def main():
    get_data()

if __name__ == '__main__':
    main()

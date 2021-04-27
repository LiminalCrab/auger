
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import psycopg2
import math
import os

#open initial connection
conn = psycopg2.connect("")

#open initial cursor
cur = conn.cursor()

def loadTemplate():
    templates_dir = os.path.join(os.getcwd(), 'templates')
    env = Environment(loader = FileSystemLoader(templates_dir), 
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('base.html')
    return template
    
def loadData():
# Let's grab some data from postgres
    try:
        q_select = '''
        SELECT 
        article_title, 
        article_url, 
        to_char(article_date, 'DD Mon YYYY'),
        article_favicon,
        article_host
        FROM posts ORDER BY article_date DESC;
        '''
        cur.execute(q_select)
        origin_data = [cur.fetchall()]
        
    except:
        print("EXCEPTION THROWN")
        print("ORIGIN DATA", origin_data)
                
    for row in origin_data:
        processed_data = [x for x in row]
        
        return processed_data
    
    
## PAGINATION CODE BELOW ##

def pg_to_list():
    origin_data = loadData()
    page_number = 1
    entries_per_page = 100
    entries = []
    while len(origin_data) > 0:
        page_entries = origin_data[:entries_per_page]
        origin_data = origin_data[entries_per_page:]
        entries.append((page_number, page_entries))
        page_number += 1
        
    return entries

    
def makeHTML(template):
    data = pg_to_list()
    column = list(zip(*data))
    for i in range(len(data)):
        sites_list_process = [column[1]] #fuck it
        page_number = [column[0][i]]
        
    sites_single_array = []
    for x in sites_list_process:
        sites_single_array.extend(x)
        #print(sites_single_array[0])
        
    print(sites_single_array[0], page_number[0])
    
    filename = os.path.join(os.getcwd(), 'index.html')
    for x in sites_single_array[0]:
        for l in sites_single_array[x]
        with open(filename, 'w+') as fw:
            fw.write(template.render())


    #filename = os.path.join(os.getcwd(), 'index.html')
    #First we write to index.html.
    #with open(filename, 'w+') as fw:
        #fw.write(template.render(data=data))

def main():
    #pg_to_list()
    makeHTML(loadTemplate())

if __name__ == '__main__':
    main()
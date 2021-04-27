
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

def pg_to_list(data):
    origin_data = loadData()
    page_number = 0
    entries_per_page = 100
    entries = []
    while len(origin_data) > 0:
        page_entries = origin_data[:entries_per_page]
        origin_data = origin_data[entries_per_page:]
        entries.append((page_number, page_entries))
        page_number += 1
        
    for page in entries:
        page_number = page[0]
        all_entries = page[1]
        print(all_entries, page_number)
    
    
def makeHTML(template, data):
    print("this function is commented out, makeHTML")


        #for article in data: #the loop above is numbers, should ask about a better way to do this.
   
    #filename = os.path.join(os.getcwd(), 'index.html')
    #First we write to index.html.
    #with open(filename, 'w+') as fw:
        #fw.write(template.render(data=data))

def main():
    pg_to_list(loadData())
    #pgn_populate_entry()
    #pgn_get_max_numbers(loadData())
    #pgn_match_to_data(loadData())
    makeHTML(loadTemplate(), loadData())

if __name__ == '__main__':
    main()
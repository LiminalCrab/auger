
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
    
    

def makeHTML(template):
    origin_data = loadData()
    entries_per_page = 100
    filename = os.path.join(os.getcwd(), 'page/end.html')

#pagination
    entries = [origin_data[page_offset:page_offset+entries_per_page] 
               for page_offset in range(0, len(origin_data), entries_per_page)]
    pnum = []
    for page_number, page_entries in enumerate(entries):
        pnum.append(str(page_number))
    for page_number, page_entries in enumerate(entries):
        with open(filename, 'w+') as fw:
            fw.write(template.render(data=page_entries, pg=pnum))
            fw.close()
            fw = open('page/%s.html' % page_number, 'w')
            fw.write(template.render(data=page_entries, pg=pnum))
    print(pnum)
    
    #this is where I tried to create that second for loop that overwrites data
    #for page_number, page_entries in enumerate(entries):
        #with open(filename, 'w+') as fw:
            #fw = open('page/%s.html' % page_number, 'w')
            #fw.write(template.render(pg=pnum))
            #fw.close()

            

        
        
        
        
        
    
    #filename = os.path.join(os.getcwd(), 'index.html')
    #with open(filename, 'w+') as fw:
        #fw.write(template.render())


    #filename = os.path.join(os.getcwd(), 'index.html')
    #First we write to index.html.
    #with open(filename, 'w+') as fw:
        #fw.write(template.render(data=data))

def main():
    #pg_to_list()
    makeHTML(loadTemplate())

if __name__ == '__main__':
    main()
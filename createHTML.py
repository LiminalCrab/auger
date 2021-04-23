from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import psycopg2
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
    
        
def makeHTML(template, data):
    for x in range(len(data)):
        max_posts = x #1646
        
    current_post = 0 #current post number
    pg_num = 0 #page number used for file names
    page_limit = 100 #when the data reaches this number, we want to create a new file and then continue writing starting from
    #the current post?
    filename = os.path.join(os.getcwd(), 'index.html')
    with open(filename, 'w+') as fw:
        for article in data:
                current_post += 1
                pg_num += 1
                if current_post < page_limit: #if post limit is less than the length of data
                    fw = open('page/%s.html' % pg_num, 'w')
                    fw.write(template.render(data=data[:current_post]))
                
   
    #filename = os.path.join(os.getcwd(), 'index.html')
    #First we write to index.html.
    #with open(filename, 'w+') as fw:
        #fw.write(template.render(data=data))

def main():
    makeHTML(loadTemplate(), loadData())

if __name__ == '__main__':
    main()

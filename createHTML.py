
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
    

#This gets the page numbers, and the index of the corresponding item in the list.
def pgn_get_numbers(data):
    pages = 0
    item_per_page = 102
    current_page = 1
    data_length = len(data)
    pages = math.ceil((data_length) / item_per_page)
    
    #lists of staged data for return out of function.
    stg_article_range = []
    stg_current_page_data = []
    for article_r in range(data_length):
        if article_r / item_per_page >= current_page:
            current_page += 1
            stg_current_page_data.append(current_page)
            stg_article_range.append(article_r)

    return stg_current_page_data, stg_article_range

#This matches the page numbers and index returned from above to the corresponding items in string format.
def pgn_match_to_data():
    m_current_page = pgn_get_numbers(loadData())[0]
    m_article_r = pgn_get_numbers(loadData())[1]
    print(m_current_page, m_article_r)
    
    
        
def makeHTML(template, data):
    print("this function is commented out, makeHTML")


            #for article in data: #the loop above is numbers, should ask about a better way to do this.
   
    #filename = os.path.join(os.getcwd(), 'index.html')
    #First we write to index.html.
    #with open(filename, 'w+') as fw:
        #fw.write(template.render(data=data))

def main():
    pgn_match_to_data()
    makeHTML(loadTemplate(), loadData())

if __name__ == '__main__':
    main()
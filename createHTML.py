
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
def pgn_get_max_numbers(data):
    ## STUFF I MIGHT NEED IN THE FUTURE ##
    #pages = 0
    #pages = math.ceil((data_length) / item_per_page)

    max_item_per_page = 102
    current_page = 1
    data_length = len(data)
    
    #lists of staged data for return out of function.
    stg_whole_article_range = []
    stg_max_article_range = []
    stg_current_page_data = []
    for article_r in range(data_length):
        stg_whole_article_range.append(article_r)
        #here is min max we need to fill the pages.
        if article_r / max_item_per_page >= current_page:
            current_page += 1
            stg_current_page_data.append(current_page)
            stg_max_article_range.append(article_r)
                  
    return stg_current_page_data, stg_max_article_range, stg_whole_article_range

#We need data to populate whole pages now.
def pgn_populate_entry():
    max_page_count = pgn_get_max_numbers(loadData())[0]
    max_article_range = pgn_get_max_numbers(loadData())[1]
    data_gap = pgn_get_max_numbers(loadData())[2]
    max_item_per_page = 102
    for page in max_page_count:
        for data in data_gap:
            item_per_page = data % max_item_per_page
            print(page, item_per_page)
    

                            
#This matches the page numbers and index returned from above to the corresponding items in string format.
def pgn_match_to_data(db_data):
    unpack_current_page_data = pgn_get_max_numbers(loadData())[0]
    unpack_article_range = pgn_get_max_numbers(loadData())[1]
    pgn_origin_data = [loadData()]
    for article in pgn_origin_data:
        current_page = [x for x in unpack_current_page_data]
        post_number = [x for x in unpack_article_range]
        #matched_data = {"page_number": current_page, "post_number": post_number}
        #print(matched_data)
    
    

def makeHTML(template, data):
    print("this function is commented out, makeHTML")


        #for article in data: #the loop above is numbers, should ask about a better way to do this.
   
    #filename = os.path.join(os.getcwd(), 'index.html')
    #First we write to index.html.
    #with open(filename, 'w+') as fw:
        #fw.write(template.render(data=data))

def main():
    pgn_populate_entry()
    #pgn_get_max_numbers(loadData())
    #pgn_match_to_data(loadData())
    makeHTML(loadTemplate(), loadData())

if __name__ == '__main__':
    main()
import psycopg2

#open initial connection
conn = psycopg2.connect("")

#open initial cursor
cur = conn.cursor()

'''
#WHAT IS THIS#
This looks for duplicates in the database and removes them. It also removes posts that are missing vital information
such as the article date and the article url. Auger could have missed these for a variety of reasons, such as improper
XML code or it simply... just didn't figure it out I guess. 

NOTE: Dupes_del is currently unused as it as wiping the entire db, will repair someday... someday.
'''

def main():
    
    #this might be causing some problems.
    dupes_del = '''
       DELETE FROM posts
       WHERE posts.id IN (
        ELECT posts.id FROM ( SELECT posts.id, ROW_NUMBER() OVER w as rnum FROM posts 
           WINDOW w AS ( partition BY article_title, article_url
              ORDER BY posts.id)) t WHERE t.rnum > 1);
    '''

    delete_empty_dates = '''
    DELETE FROM posts WHERE article_date IS NULL;
    '''
    delete_empty_urls = '''
    DELETE FROM posts WHERE article_url IS NULL;
    '''
        
    #cur.execute(dupes_del)   
    cur.execute(delete_empty_dates)
    cur.execute(delete_empty_urls)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()  


import psycopg2

#open initial connection
conn = psycopg2.connect("")

#open initial cursor
cur = conn.cursor()

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


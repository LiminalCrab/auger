import asyncio
import psycopg2

#open initial connection
conn = psycopg2.connect("")

#open initial cursor
cur = conn.cursor()

async def main():
    
    dupes_del = '''
        DELETE FROM posts
        WHERE id IN (
        SELECT id FROM ( SELECT id, ROW_NUMBER() OVER w as rnum FROM posts 
            WINDOW w AS ( partition BY host_title, post_url
                ORDER BY id)) t WHERE t.rnum > 1);
    '''
    #Temporary fix that definitely will remain temporary, yes sir.
    delete_empty_dates = '''
    DELETE FROM posts WHERE post_date IS NULL;
    '''
    delete_empty_urls = '''
    DELETE FROM posts WHERE post_url IS NULL;
    '''
        
    cur.execute(dupes_del)   
    cur.execute(delete_empty_dates)
    cur.execute(delete_empty_urls)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    asyncio.run(main())  


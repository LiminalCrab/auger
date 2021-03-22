import asyncio
import psycopg2


async def main():
    #open initial connection
    conn = psycopg2.connect("")

    #open initial cursor
    cur = conn.cursor()
    
    dupes_del = '''
        DELETE FROM posts
        WHERE id IN (
        SELECT id FROM ( SELECT id,ROW_NUMBER() OVER w as rnum FROM posts 
            WINDOW w AS ( partition BY host_title, post_url
                ORDER BY id)) t WHERE t.rnum > 1);
    '''
    #Temporary fix
    delete_empty = '''
    DELETE FROM posts WHERE post_date IS NULL;
    '''


        
    cur.execute(dupes_del)
    cur.execute(delete_empty)
    deleted = cur.fetchall()
    for dlt in deleted:
       print(f"ID: {dlt[0]} TITLE: {dlt[1]}")
        
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    asyncio.run(main())  


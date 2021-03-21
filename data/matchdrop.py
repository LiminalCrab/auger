import asyncio
import psycopg2


async def main():
    #open initial connection
    conn = psycopg2.connect(
        host="",
        database="",
        user="",
        password="",
        port=5432 )

    #open initial cursor
    cur = conn.cursor()
    cur.execute('SELECT * FROM posts;')
    results = cur.fetchall()
    for r in results:
        print(f"{r[0]} and {r[2]}")
        
    dupes_del = '''
        DELETE FROM posts
        WHERE id IN (
        SELECT id FROM ( SELECT id,ROW_NUMBER() OVER w as rnum FROM posts 
            WINDOW w AS ( partition BY host_title, post_url, post_date 
                ORDER BY id)) t WHERE t.rnum > 1);
    '''
    cur.execute(dupes_del)
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    asyncio.run(main())  


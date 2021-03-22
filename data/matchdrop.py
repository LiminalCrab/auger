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
        SELECT id FROM ( SELECT id,ROW_NUMBER() OVER w as rnum FROM posts 
            WINDOW w AS ( partition BY host_title, post_url
                ORDER BY id)) t WHERE t.rnum > 1);
    '''
    #Temporary fix
    delete_empty = '''
    DELETE FROM posts WHERE post_date IS NULL;
    '''


        
    cur.execute(dupes_del)
    deleted_dupes = cur.fetchall()
    for dupdlt in deleted_dupes:
        print(f"DUPES: ID: {dupdlt[0]} TITLE: {dupdlt[1]}")
        
    cur.execute(delete_empty)
    deletedempt = cur.fetchall()
    for emptdlt in deletedempt:
        print(f"DELETED EMTPY: ID: {emptdlt[0]} TITLE: {emptdlt[1]}")

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    asyncio.run(main())  


import asyncio
import psycopg2

#open initial connection
conn = psycopg2.connect("")

#open initial cursor
cur = conn.cursor()

async def main():
    
    SET_DB_ORDER = '''
    SELECT post_date FROM posts ORDER BY post_date DESC;
    '''
    print("ORDER.PY: SORTING DATES")
    cur.execute(SET_DB_ORDER)
    
    
    cur.close()
    conn.close()
    print("ORDER.PY: ok")


if __name__ == '__main__':
    asyncio.run(main())  
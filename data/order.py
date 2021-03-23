import asyncio
import psycopg2
import json

#open initial connection
conn = psycopg2.connect("")

#open initial cursor
cur = conn.cursor()

async def main():
    
    SET_DB_ORDER = '''
    SELECT host_title, post_url, post_date FROM posts ORDER BY post_date DESC;
    '''
    print("ORDER.PY: SORTING DATES")
    cur.execute(SET_DB_ORDER)
    data = cur.fetchall()
    
    with open('links.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    
    #conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    asyncio.run(main())  
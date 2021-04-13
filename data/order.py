import asyncio
import psycopg2
import json

#open initial connection
conn = psycopg2.connect("")

#open initial cursor
cur = conn.cursor()

async def main():
    
    ORDER_BY_DATE_TO_JSON = '''
        SELECT 
            json_build_object(
                'id', posts.id,
                'title', posts.host_title,
                'url', posts.post_url,
                'date', posts.post_date
            ) FROM posts ORDER BY post_date DESC;
    '''
   
    print("ORDER.PY: SORTING DATES")
    cur.execute(ORDER_BY_DATE_TO_JSON)
    data = list(map(lambda x: x[0], cur.fetchall()))
    
    with open('links.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    asyncio.run(main()) 
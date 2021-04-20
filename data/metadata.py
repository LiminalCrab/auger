import asyncio
import httpx
from bs4 import BeautifulSoup
import psycopg2
from urls import URLS_HTML
import re

#[WHAT IS THIS]
#Scrapes URLS_HTML for their favicon links using beautiful soup. It's also where
#we get the host_url for the database, kind of weird I know. 

#open initial connection
conn = psycopg2.connect("")

#open initial cursor
cur = conn.cursor()

#SQL vars
extract_article_url = '''
    CREATE OR REPLACE FUNCTION public.posts(_url text)
        RETURNS text LANGUAGE sql IMMUTABLE PARALLEL SAFE AS
    $$
        SELECT string_agg(token, '' ORDER BY alias DESC)
        FROM ts_debug(_url) q
        WHERE q.alias in ('protocol', 'host');
    $$;
    
    select posts(%s);
    '''

async def main():
    async with httpx.AsyncClient() as client:
        for url in URLS_HTML:
            try:
                response = await client.get(url, timeout=30.0)
                
            except httpx.RequestError as exc:
                print(f"An error occurred while requesting {exc.request.url!r}.")
                continue
            
            try:
                root = BeautifulSoup(response.text, features="lxml")
                
            except:
                print("Exception caught after second try.")
                continue
            
            try:      
                if root.find("link", attrs=({"rel": "icon"})):
                    favi = root.find("link", attrs={"rel": "icon"}).get('href')
                elif root.find("link", attrs={"rel": "shortcut icon"}):
                    favi = root.find("link", attrs={"rel": "shortcut icon"}).get('href')
                else:
                    favi = f'{url.rstrip("/")}/favicon.ico'
                    
                if favi == "./data/favicon.png":
                    favi = f"{url}/data/favicon.png"
                if favi == "data:,":
                     favi = f"sudogami.com/assets/anon.ico"
                       
            except IndexError:
                print("Exception caught second try.")
                
        cur.execute('SELECT article_url FROM posts;')
        all_articles = [cur.fetchall()]
        for art in all_articles[0]:
            cur.execute(extract_article_url, art)
            endl = cur.fetchall()
            print(endl)
                
        cur.close()
        conn.close()
                                
if __name__ == '__main__':
    asyncio.run(main())
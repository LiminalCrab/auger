import asyncio
import httpx
from bs4 import BeautifulSoup
import psycopg2
from urls import URLS_HTML
import re
import pdb
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
                    favicon = f'{url}/{favi}'
                    print("ICON:", favicon)
                elif root.find("link", attrs={"rel": "shortcut icon"}):
                    favi = root.find("link", attrs={"rel": "shortcut icon"}).get('href')
                    favicon = f'{url}/{favi}'
                    print("SHORTCUT:", favicon)
                else:
                    favi = f'{url.rstrip("/")}/favicon.ico'
                    
                if favi == "./data/favicon.png":
                    favi = f"{url}/data/favicon.png"
                if favi == "data:,":
                     favi = f"sudogami.com/assets/anon.ico"
                
                favicons = [favi]
                print(favicons)
                       
            except IndexError:
                print("Exception caught second try.")
                
        #We need to match the favicons to the correct rows.
        #this first execute is grabbing us the list of posts we need to iterate over.
        #the query in the for loop is stripping the hyperlink and giving us the literal URL.         
        cur.execute('SELECT article_url FROM posts;')
        all_articles = [cur.fetchall()]
        for art in all_articles[0]:
            cur.execute(extract_article_url, art)
            staged_urls = cur.fetchall()
            #print(art[0])
            
            #remove unnecessary characters [0][0]
            #send back into the db in a new row.
            if art[0] and staged_urls[0][0]:
                #cur.execute('UPDATE posts SET article_host = (%s) WHERE article_url = (%s)', (staged_urls[0][0], art[0]))
                print("ADDED: {} AT: {}".format(staged_urls[0][0], art[0]))
                
            
            
            
                
        cur.close()
        conn.close()
                                
if __name__ == '__main__':
    asyncio.run(main())
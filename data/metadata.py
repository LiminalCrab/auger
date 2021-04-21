from bs4 import BeautifulSoup
import urllib.parse
import psycopg2
import asyncio
import httpx
import re


#[WHAT IS THIS]
#Scrapes URLS_HTML for their favicon links using beautiful soup. It's also where
#we get the host_url for the database. 
 

#open initial connection
conn = psycopg2.connect("")

#open initial cursor
cur = conn.cursor()

#SQL vars
sql_extract_article_url = '''
    CREATE OR REPLACE FUNCTION public.posts(_url text)
        RETURNS text LANGUAGE sql IMMUTABLE PARALLEL SAFE AS
    $$
        SELECT string_agg(token, '' ORDER BY alias DESC)
        FROM ts_debug(_url) q
        WHERE q.alias in ('protocol', 'host');
    $$;
    
    select posts(%s);
    '''

select_urls_from_post = '''
SELECT article_url FROM posts;
''' 

update_transact = """
UPDATE posts SET article_host = %s, article_favicon = %s WHERE article_url ILIKE '%' || %s || '%', 
"""

async def main():
    db_urls = row_match()
    async with httpx.AsyncClient() as client:
        for url in db_urls:
            try:
                response = await client.get(url, timeout=30.0)
                
            except httpx.RequestError as exc:
                    print(f"An error occured while making request {exc.request.url!r}.")
                    
            try:
                root = BeautifulSoup(response.text, features="lxml")
                
            except:
                print("exception caught after second try.")
                
            try:
                if root.find("link", attrs=({"rel": "icon"})):
                    favicon_path = root.find("link", attrs={"rel": "icon"}).get('href')
                elif root.find("link", attrs=({"rel": "shortcut icon"})):
                    favicon_path = root.find("link", attrs={"rel": "shortcut icon"}).get('href')
                else:
                    favicon_path = "/favicon.ico"
                    
                if favicon_path == "data:,":
                    favicon_path = None #default icon.

                if favicon_path is not None:
                    favicon_url = urllib.parse.urljoin(url, favicon_path)
                
                #let's chunk this to postgres
                print(f"ADDING TO DATABASE: HOST: {url}, FAVICON: {favicon_url}, with conditional key {url}")
                cur.execute("""UPDATE posts SET article_host = %s, article_favicon = %s WHERE article_url SIMILAR TO '%%' || %s || '%%'""", 
                            (url, favicon_url, url))
                conn.commit()
                
            except ValueError:
                print("exception", url)
        
            
def row_match():
    cur.execute(select_urls_from_post)
    all_articles = cur.fetchall()
    stg_urls = []
    
    for article in all_articles:
        cur.execute(sql_extract_article_url, article)
        staged_articles = cur.fetchall()
        if staged_articles[0][0] is not None:
            stg_urls.append(staged_articles[0][0]) #We break a list, add it to another lol
        else:
            print("else else", staged_articles[0][0])   
        
    return stg_urls
        
        
        
if __name__ == '__main__':
    asyncio.run(main())
    
cur.close()
conn.close()
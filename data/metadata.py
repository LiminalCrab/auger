from bs4 import BeautifulSoup
import urllib.parse
import psycopg2
import asyncio
import httpx



'''
#WHAT IS THIS#
This uses beautiful soup to scrape the html pages. This does not use the url.py files, instead to match the favicons and host website to their corresponding blog post in the database, 
we pull the list of all current articles in the database, use sql to remove the majority of the hyperlink and just keep the literal site url. 
This is then submitted to a list which python iterates through and beautiful soup scrapes the favicons from. 
Afterwards, we combine the host url we stripped out earlier and the directory of the favicons we scraped using urllib.

This is extremely hacky and takes about 3 minutes to complete.
'''

 

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
                    
                    #gonna have to expand this later, just getting rid of something I noticed.
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
import asyncio
import httpx
from bs4 import BeautifulSoup
import psycopg2
from urls import URLS_HTML


#[WHAT IS THIS]
#Scrapes URLS_HTML for their favicon links using beautiful soup. It's also where
#we get the host_url for the database, kind of weird I know. 

#open initial connection
conn = psycopg2.connect("")

#open initial cursor
cur = conn.cursor()

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
                        favi = f"{url}/assets/anon.ico"
                                       
                #cur.execute("UPDATE posts SET site_favicon = (%s) WHERE site_url = (%s);", (favi, url))
                #conn.commit()
                
            except IndexError:
                print("Exception caught second try.")
                
    cur.close()
    conn.close()
                
if __name__ == '__main__':
    asyncio.run(main())
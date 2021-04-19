import asyncio
import httpx
from bs4 import BeautifulSoup
import psycopg2
from urls import URLS_HTML


#[WHAT IS THIS]
#Scrapes URLS_HTML for their favicon links using beautiful soup.

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
                    
                    #hmmmm
                if favi == "./data/favicon.png":
                    favi = f"{url}/data/favicon.png"
                    
                if favi == "data:,":
                    favi = f"{url}/assets/anon.ico"
                    
                print(f"FAVICON FOUND: {favi} at {url}")
                
            except IndexError:
                print("Exception caught second try.")
                
if __name__ == '__main__':
    asyncio.run(main())
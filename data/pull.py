from urls import URLS
import xml.etree.ElementTree as ET
import psycopg2
import asyncio
import httpx




#[WHAT IS THIS]
#It scrapes the URL's list for their rss XML feeds and commits them to a postgres db.
#It also uses an exception to do this which is emphasiszed for flow control in Python. Wild right? 
# XML is handled by Element Tree, and HTML is handled by BeautifulSoup.

#open initial connection
conn = psycopg2.connect("")

#open initial cursor
cur = conn.cursor()

async def main():
    async with httpx.AsyncClient() as client:
        for url in URLS:
            try: 
                response = await client.get(url, timeout=30.0)
                
            except httpx.RequestError as exc:
                print(f"An error occurred while requesting {exc.request.url!r}.")
                continue
            
            try:
                #give root a body of XML as a string.
                root = ET.fromstring(response.text)
                                
            except:
                continue
            
            #there is a variety of XML namespaces we have to deal with, the ones that
            #are not handled in the first try will get caught in the exception and 
            #and sent to the code in the next for loops exception. They required extra
            #indexing. 
            
            try:
                links = [x for x in root if x.tag.split("}")[1] in ("entry", "item")]
            except IndexError:
                links = [x for x in root[0] if x.tag in ("entry", "item")]  

            for link in links:
                try:
                    title = [x.text for x in link if x.tag.split("}")[1] == "title"]
                    link_url = [x.attrib["href"] for x in link if x.tag.split("}")[1] == "link"]
                    
                    print("LINK_URL", link_url)
                    
                    if title and link_url:
                        print("Found {} with HREF {}".format(title, link_url))
                        
                except IndexError:
                    #NoneTypes keep fucking with this, so we needed to get rid of them. 
                    #We have to sort out which links are providing nonetypes later if I have this right.
                    
                    if link is not None:
                        title = [link[0].text]
                        link_url = [link.findtext('link')]
                    else:
                        print(f"IS NONE: {link} and {link_url} ")
                    
                #send to database.
                if title and link_url:
                    print(f"STAGED FOR DATABASE: {title[0]} {link_url[0]}")
                    print("Found {} with HREF {}".format(title, link_url))
                    cur.execute("INSERT INTO posts (article_title, article_url) VALUES (%s, %s)", 
                        (title[0], link_url[0]))
                    conn.commit()
                    print("committed")
                    print(f"{title} and {link_url} submitted to database.")
                        
    cur.close()
    conn.close()  

if __name__ == '__main__':
    asyncio.run(main())
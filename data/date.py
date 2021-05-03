from urls import URLS
import xml.etree.ElementTree as ET
import psycopg2
import asyncio
import httpx



#open initial connection
conn = psycopg2.connect("")
conn.set_session(autocommit=True)

#open initial cursor
cur = conn.cursor()

async def main():

#probably don't need two of these, should test which one works better later.
    conn = psycopg2.connect("")
    conn.set_session(autocommit=True)
    
    async with httpx.AsyncClient() as client:
        for feed in URLS:
            response = await client.get(feed, timeout=30.0)
            try:
                #get the root of the xml
                root = ET.fromstring(response.text)
            except:
                print("exception in first try")
                continue
            try:
                links = [x for x in root if x.tag.split("}")[1] in ("entry", "item")]
            except IndexError:
                links = [x for x in root[0] if x.tag in ("entry", "item")]
                
            for link in links:
                try:
                    published_date = [x.text for x in link if x.tag.split("}")[1] == "published"]
                    updated_date = [x.text for x in link if x.tag.split("}")[1] == "updated"]
                    pub_date = [x.text for x in link if x.tag.split("}")[1] == "pubDate"]
                    link_url = [x.attrib["href"] for x in link if x.tag.split("}")[1] == "link"]
                    
                except IndexError:
                        link_url = [link.findtext("link")]
                        published_date = [link.findtext("published")]
                        updated_date = [link.findtext("updated")]
                        pub_date = [link.findtext("pubDate")]
                        
                        #yeah we're gonna throw invalid dates with the NULL post at the bottom LOL
                        #fix ya' XML.
                        #Will make a list of valid dates later, if any of those fail, default to this bullshit.
                        if pub_date[0] == "Invalid Date":
                            pub_date = ['0001-01-01']
                            print(f"INVALID DATE FIXED WITH:{pub_date[0]} at {link_url[0]}")

                if published_date and link_url:
                    print("PUBLISHED DATE: published date tag found: {} at {}".format(published_date[0], link_url[0]))
                    cur.execute("UPDATE posts SET article_date = (%s) WHERE article_url = (%s);", (published_date[0], link_url[0]))
                    print(f"{link_url[0]} and {published_date[0]} added to database.")
                if updated_date and link_url:
                    print("UPDATED DATE: updated tag found: {} at {}".format(updated_date[0], link_url[0]))                   
                    cur.execute("UPDATE posts SET article_date = (%s) WHERE article_url = (%s);", (updated_date[0], link_url[0]))
                    print(f"{link_url[0]} and {updated_date[0]} added to database.")
                if pub_date and link_url:
                    print("PUBDATE: updated tag found: {} at {}".format(pub_date[0], link_url[0]))
                    cur.execute("UPDATE posts SET article_date = (%s) WHERE article_url = (%s);", (pub_date[0], link_url[0]))
                    print(f"{link_url[0]} and {pub_date[0]} added to database.")
                  
        conn.commit()
        cur.close()
        conn.close()
            
            
if __name__ == '__main__':
    asyncio.run(main())      
            
import psycopg2
import re
import httpx
import asyncio
import xml.etree.ElementTree as ET

#open initial connection
conn = psycopg2.connect("")
conn.set_session(autocommit=True)

#open initial cursor
cur = conn.cursor()

#replace this with a different file...
URLS =  [
        "http://nonmateria.com/rss.xml",
        "https://notes.neeasade.net/rss.xml",
        "https://aless.co/rss.xml",
        "https://writing.natwelch.com/feed.rss",
        "https://resevoir.net/rss.xml",
        "https://szymonkaliski.com/feed.xml",
        "https://xj-ix.luxe/feed.atom",
        "http://nonmateria.com/rss.xml",
        "https://oddworlds.org/rss.xml",
        "https://chad.is/rss.xml",
        "https://bismuth.garden/feed.xml",
        "https://xvw.github.io/atom.xml",
        "https://now.lectronice.com/feed.xml",
        "https://longest.voyage/index.xml",
        "https://kokorobot.ca/links/rss.xml",
        "https://ameyama.com/blog/rss.xml",
        "https://phse.net/post/index.xml",
        "https://rosano.ca/feed",
        "https://teknari.com/feed.xml",
        "https://serocell.com/feeds/serocell.xml",
        "https://gueorgui.net/feed.xml",
        "https://sixey.es/feed.xml",
        "https://icyphox.sh/blog/feed.xml",
        "https://royniang.com/rss.xml",
        "https://crlf.site/feed.xml",
        "https://system32.simone.computer/rss.xml",
        "https://simply.personal.jenett.org/feed/",
        "https://q.pfiffer.org/feed.xml",
        "https://www.edwinwenink.xyz/index.xml",
        "https://www.mentalnodes.com/sitemap.xml",
        "https://materialfuture.net/rss.xml",
        "https://travisshears.com/index.xml",
        "https://ix5.org/thoughts/feeds/all.atom.xml",
        "https://nor.the-rn.info/feed.xml",
        "https://inqlab.net/posts.xml",
        "https://metasyn.pw/rss.xml",
        "https://milofultz.com/atom.xml",
        "https://wolfmd.me/feed.xml",
        "https://irimi.one/atom.xml",
        "https://natehn.com/index.xml",
        "https://www.gr0k.net/blog/feed.xml",
        "https://tendigits.space/feed.xml",
        "https://wiki.xxiivv.com/links/rss.xml"]

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
                        if pub_date[0] == "Invalid Date":
                            pub_date = ['0001-01-01']
                            print(f"INVALID DATE FIXED WITH:{pub_date[0]} at {link_url[0]}")

                if published_date and link_url:
                    print("PUBLISHED DATE: published date tag found: {} at {}".format(published_date[0], link_url[0]))
                    cur.execute("UPDATE posts SET post_date = (%s) WHERE post_url = (%s);", (published_date[0], link_url[0]))
                    print(f"{link_url[0]} and {published_date[0]} added to database.")
                if updated_date and link_url:
                    print("UPDATED DATE: updated tag found: {} at {}".format(updated_date[0], link_url[0]))                   
                    cur.execute("UPDATE posts SET post_date = (%s) WHERE post_url = (%s);", (updated_date[0], link_url[0]))
                    print(f"{link_url[0]} and {updated_date[0]} added to database.")
                if pub_date and link_url:
                    print("PUBDATE: updated tag found: {} at {}".format(pub_date[0], link_url[0]))
                    cur.execute("UPDATE posts SET post_date = (%s) WHERE post_url = (%s);", (pub_date[0], link_url[0]))
                    print(f"{link_url[0]} and {pub_date[0]} added to database.")
                  
        conn.commit()
        cur.close()
        conn.close()
            
            
if __name__ == '__main__':
    asyncio.run(main())      
            
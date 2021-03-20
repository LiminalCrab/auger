import psycopg2
import re
import httpx
import asyncio
import xml.etree.ElementTree as ET
import pdb

URLS =  ["https://electro.pizza/feed.xml",
        "https://bismuth.garden/feed.xml",
        "https://xvw.github.io/atom.xml",
        "https://now.lectronice.com/feed.xml",
        "https://longest.voyage/index.xml",
        "https://kokorobot.ca/links/rss.xml",
        "https://ameyama.com/blog/rss.xml",
        "http://npisanti.com/rss.xml",
        "https://phse.net/post/index.xml",
        "https://rosano.ca/feed",
        "https://teknari.com/feed.xml",
        "https://serocell.com/feeds/serocell.xml",
        "https://eli.li/feed.rss",
        "https://gueorgui.net/feed.xml",
        "https://resevoir.net/rss.xml",
        "https://sixey.es/feed.xml",
        "https://icyphox.sh/blog/feed.xml",
        "https://royniang.com/rss.xml",
        "https://crlf.site/feed.xml",
        "https://0xff.nu/feed.xml",
        "https://system32.simone.computer/rss.xml",
        "https://xj-ix.luxe/feed.atom",
        "https://simply.personal.jenett.org/feed/",
        "https://q.pfiffer.org/feed.xml",
        "https://www.edwinwenink.xyz/index.xml",
        "https://www.mentalnodes.com/sitemap.xml",
        "https://materialfuture.net/rss.xml",
        "https://travisshears.com/index.xml",
        "https://ix5.org/thoughts/feeds/all.atom.xml",
        "https://www.juliendesrosiers.com/feed.xml",
        "https://nor.the-rn.info/feed.xml",
        "https://inqlab.net/posts.xml",
        "https://metasyn.pw/rss.xml",
        "https://milofultz.com/atom.xml",
        "https://wolfmd.me/feed.xml",
        "https://irimi.one/atom.xml",
        "https://hugo.soucy.cc/index.xml",
        "https://darch.dk/feed/page:feed.xml",
        "https://natehn.com/index.xml",
        "https://www.gr0k.net/blog/feed.xml",
        "https://tendigits.space/feed.xml",
        "https://wiki.xxiivv.com/links/rss.xml"]

async def main():
    async with httpx.AsyncClient() as client:
        for feed in URLS:
            response = await client.get(feed)
            try:
                #read response stream
                r_stream = ET.fromstring(response.text)
            except:
                print("exception in first try")
                continue
            try:
                links = [x for x in r_stream if x.tag.split("}")[1] in ("entry", "item")]
            except IndexError:
                print("URL {} is fucked up.".format(feed))
                continue
        
            for link in links:
                published_date = [x.text for x in link if x.tag.split("}")[1] == "published"]
                updated_date = [x.text for x in link if x.tag.split("}")[1] == "updated"]
                pub_date = [x.text for x in link if x.tag.split("}")[1] == "pubDate"]
                link_url = [x.attrib["href"] for x in link if x.tag.split("}")[1] == "link"]
                
                if published_date and link_url:
                    print("{} and {}".format(published_date, link_url))
                if updated_date and link_url:
                    print("updated tag found: {} at {}".format(updated_date, link_url))
                if pub_date and link_url:
                    print("pubDate tag found: {} at {}".format(pub_date, link_url))
                                    
                conn = psycopg2.connect(
                    host="",
                    database="",
                    user="",
                    password="",
                    port= )
                                
                cur = conn.cursor()
                cur.execute("SELECT * FROM posts WHERE post_url=(%s);", (link_url))
                row = cur.fetchone();
                print(f"{row} and {link_url} match.")
                cur.close()
                conn.close()

                

            
            
if __name__ == '__main__':
    asyncio.run(main())      
            
            
        





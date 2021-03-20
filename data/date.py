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
        #This is probably the worst thing I've ever written and that's saying a lot.
            for link in links:
                published_date = [x.text for x in link if x.tag.split("}")[1] == "published"]
                updated_date = [x.text for x in link if x.tag.split("}")[1] == "updated"]
                pub_date = [x.text for x in link if x.tag.split("}")[1] == "pubDate"]
                link_url = [x.attrib["href"] for x in link if x.tag.split("}")[1] == "link"]
                
                if published_date and link_url:
                    print("PUBLISHED DATE: published date tag found: {} at {}".format(published_date, link_url))
                    conn = psycopg2.connect(host="", database="", user="", password="", port=5432)
                    cur = conn.cursor()
                    cur.execute("INSERT INTO posts (host_title, post_url) VALUES (%s, %s)", 
                                (published_date[0], link_url[0]))                    
                    cur.close()
                    conn.close()
                if updated_date and link_url:
                    print("UPDATED DATE: updated tag found: {} at {}".format(updated_date, link_url))
                    conn = psycopg2.connect(host="", database="", user="", password="", port=5432)
                    cur = conn.cursor()
                    cur.execute("INSERT INTO posts (host_title, post_url) VALUES (%s, %s)", 
                                (updated_date[0], link_url[0]))
                    cur.close()
                    conn.close()
                if pub_date and link_url:
                    print("PUBDATE: pubDate tag found: {} at {}".format(pub_date, link_url))
                    conn = psycopg2.connect(host="", database="", user="", password="", port=5432)
                    cur = conn.cursor()
                    cur.execute("INSERT INTO posts (host_title, post_url) VALUES (%s, %s)", 
                                (pub_date[0], link_url[0]))
                    cur.close()
                    conn.close()
                try:
                                    
                    conn = psycopg2.connect(
                        host="",
                        database="",
                        user="",
                        password="",
                        port=5432 )
                                    
                    cur = conn.cursor()
                    cur.execute("SELECT post_url FROM posts WHERE post_url = %s;", (link_url))
                    result = cur.fetchone()
                    print("{} FROM DATABASE MATCHED {} FROM URLS.".format(result, link_url))
                    cur.close()
                    conn.close()
                except IndexError:
                    conn = psycopg2.connect(
                        host="",
                        database="",
                        user="",
                        password="",
                        port=5432)
                    cur = conn.cursor()
                    print ("FUCKED URL {} cannot be added to database.".format(feed))
                    continue
                
            
            
if __name__ == '__main__':
    asyncio.run(main())      
            
import asyncio
import httpx
import re
import xml.etree.ElementTree as ET
import psycopg2
import pdb

#open initial connection
#conn = psycopg2.connect("")

#open initial cursor
#cur = conn.cursor()

URLS =  [
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
        "https://gueorgui.net/feed.xml",
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
        for url in URLS:
            response = await client.get(url)

            try:
                root = ET.fromstring(response.text)
            except:
                continue
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
                    
                    #for x in links:
                        #print("X TEXT:{} X LINKS: {} X ROOT: {}".format(x[0].text, x.findtext('link'), links[0]))
                        #print("TRUE FALSE:{}".format(x[0].tag == "title"))
                    #print("link: {}, LINKS: {}".format(link[0], links))
                    title = [link[0].text]
                    #print("EXCEPTION TITLE:", title)
                    
                    link_url = [link.findtext('link')]
                    #print("EXCEPTION URL:", link_url)
                    
                    if title and link_url:
                        print("Found {} with HREF {}".format(title, link_url))
                    #cur.execute("INSERT INTO posts (host_title, post_url) VALUES (%s, %s)", 
                            #(title[0], link_url[0]))
                    #conn.commit()
                    #print("committed")
                    #print(f"{title} and {link_url} submitted to database.")
                    
    #cur.execute("SELECT * FROM posts;")
    #rows = cur.fetchall()
    #for r in rows:
        #print(f"{r[0]} and {r[1]}")
    #cur.close()
    #conn.close()  

if __name__ == '__main__':
    asyncio.run(main())
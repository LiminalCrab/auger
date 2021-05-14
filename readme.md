# DOCUMENTATION


# ABOUT
Hosted on www.sudogami.com/page/0.html

TO DO list at the bottom.

This is an RSS feed for the [Merveilles webring project](https://github.com/XXIIVV/Webring/), it's a static page that's updated once daily with all the recent articles written by the community. This idea was sparked from Cblgh's search engine "Lieu", and I hope it encourages everyone to post more on their blogs.

## How do I add my website to the aggregator?
You have to be an active member of the Merveilles community, and thus the Mastodon rules apply to this page. You can read them here: https://merveilles.town/about/more
Your website must meet the [criteria of the Webring project](https://github.com/XXIIVV/Webring/#webring-criteria). 

Please ensure your XML is correct, atom feeds are so far the best for parsing, but if you use your own take a look at some other feeds on the list and try your best to match them up. If your XML is incorrect it'll cause the scripts to crash and I'll have to remove your site until I can figure out how to circumvent these errors.

If you meet both of those conditions just modify url.py with your rss link, your website link, and make a code comment linking to your merveilles.town mastodon account and I'll look into it.

If your website does not meet the Webring criteria but manages to make it on their anyway, It will be removed from Auger at my discretion. If you post constructive content, it likely won't be an issue -- however; if community members complain about said content, that post will likely be removed. 


## HOW DOES IT WORK?

On the backend Auger is running a postgres database that is populated and maintained by the python scripts listed below. It's scraping from a list of urls and individual rss feeds listed on the Webring project which then is submitted to the database using psycopg2. Afterwards the html is rendered to a static page using Jinja2. Cron is used to run these scripts once a day at a certain time (08:00 ET). ***This website is only updated once per day.***

You can see the database schema [here](https://github.com/LiminalCrab/fucking-bulletproof). This is the meme way I'm storing backups of the database. It's completely unncessary.

# CODE

### data/pull.py

This is the start point for the backend. This is the first script ran by Cron. The links here are only scraped from their **titles** and **urls** and they're submitted to a postgres database.

### data/date.py 

This is the second script that Cron runs seconds after pull.py,
Scrapes the dates from each article of each website in the list of urls and submit it to the database. 

### data/matchdrop.py 

This is the third script that Cron runs seconds after date.py. 
It's job is to look for any tables/rows that might be missing data and delete them.

### metadata.py

This uses beautiful soup to scrape the html pages. This does not use the url.py files, instead to match the favicons and host website to their corresponding blog post in the database, we pull the list of all current articles in the database, use sql to remove the majority of the hyperlink and just keep the literal site url. This is then submitted to a list which python iterates through and beautiful soup scrapes the favicons from. Afterwards, we combine the host url we stripped out earlier and the directory of the favicons we scraped using urllib. 

The side effects of this so far is that the database currently has a lot of redundant information in it, hundreds of the same url are populating rows (article_host and article_favicon). My intention in the future is to make another table that holds one url and one favicon link and makes a one to many connection to the other table, that way instead of having 500 of one url connected to 500 of the same blog posts, we have one url connected to 500 blog posts, but this is something I have to learn more about so it's on the back burner until I finish my primary focuses on the to do list.

### createHTML.py 

Last script Cron runs.
Static page generator, populates index.html with all the css, html, and stuff from the database. 

It's important to note that inside the makeHTML function pagination takes place, it points to an html called end.html which is the final material on the list, and outputs the data from that onward all the way to page zero.

### urls.py

Just a python list of the xml feeds and host sites to pull from.

## Templates
### Base.html
This is the skeleton frame of the generated HTML. If something doesn't need its own template, I'll put it in here.

### Content.html 
This is where the code that populates the list is.

## Pages
This is where the createHTML.py outputs all the pages it generates.

# TO DO

## PRIMARY FOCUS
- [X] Jinja implementation
    - [X] Remove Javascript / JSON, allow the database to populate the html directly.
    - [X] make it so their website favicons show up beside their articles
    - [X] limit posts per page to ~~50~~ or 100.
    - [-] ~~add post summaries.~~
- [X] metadata.py (This will be expanded for more html related stuff in the future)
    - [X] - Get favicons.
    - [X] - Process host site url.
    - [X] - Match host site and favicons to associated articles in db
- [X] POSTGRESQL
    - [X] add row for article_host, article_favicon, article_summary.
- [X] order.py
    - [-] decouple from JSON
    - [-] direct db output to html.
    - [X] this might actually become obsolete.
- [ ] Server
    - [ ] See about replacing various CRON tabs with a single shell script.

## OTHER STUFF THAT NEEDS DOING

XXIIVV
- [ ] Need to implement date scraping for XXIIVV updates which is using Arvelie to format it's dates. These updates are no included in RSS updates, instead they're updated on the HTML page itself, and the date format is using Arvelie's format. This might prove a bit of a challenge for scraping as a DATE itself, I don't know if I'll be able to embed it into postgres and still be able to sort as I do with these regular date formats which might cause some issues for how content is output to the page. Devine says that it's sortable with alphasort so I need to look into that. This will require some research, trial, and error.

CSS
- [ ] - Hyperlinks for host sites
- [ ] - mess around with sizes and padding, no clear objective.

POSTGRES
- [ ] - Separate metadata table.
- [ ] - One to many connection article_host to article_urls 

OVERALL 
- [ ] - Provide safety nets for scraping failures.
- [ ] - Optimize the project and make sure everything runs smoothly.


# REMOVED FILES

### linkhandler.js 

Yeah this just fetches the json links and formats them before populated index.html, I also plan on replacing this, but FOR NOW IT WORKS. 

### data/order.py 

This is the last script ran by Cron, it sorts all the tables in the database by their dates in decending order and runs a postgres function that builds a json object. It then outputs this JSON data to a file called links.json. 

### data/links.json

This is where all the site json data submitted by order.py is held, and this is what is output to the frontend. I plan on replacing this in the future, but for now, it simply works.

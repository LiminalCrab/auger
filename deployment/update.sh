#!/bin/bash

echo "DROP TABLE posts;" | psql
echo "CREATE TABLE posts (
    id BIGSERIAL,
    article_url text,
    article_title text,
    article_host text,
    article_favicon text,
    article_date date
);
" | psql
wait

python3 /var/www/auger.sudogami/data/pull.py
wait

python3 /var/www/auger.sudogami/data/date.py
wait 

python3 /var/www/auger.sudogami/data/matchdrop.py
wait

python3 /var/www/auger.sudogami/data/metadata.py
wait

python3 /var/www/auger.sudogami/createHTML.py
wait

echo "Website updated."






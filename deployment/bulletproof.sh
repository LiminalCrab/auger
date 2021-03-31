  1 #!/bin/sh 
  2 export PGHOSTADDR="ADDRESS"
  3 export PGUSER="USERNAME"
  4 export PGDATABASE="DBNAME"
  5 export PGPASSWORD="PASSWORD"
  6 export PGPORT=0000
  7 
  8 
  9 hostname=`auggar`
 10 # Dump DBs
 11   date=`date +"%Y%m%d_%H%M%N"`
 12   filename="/home/USERNAME/www/fucking-bulletproof/${hostname}_${db}_${date}.sql"
 13   pg_dump rssfeeds >  $filename 2>&1
 14 
 15 cd /home/USERNAME/www/fucking-bulletproof
 16 
 17 git add -A
 18 git commit -p -m "${date}"
 19 git push
 20 
 21 
 22 exit 0
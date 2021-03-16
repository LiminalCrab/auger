import psycopg2

# db
con = psycopg2.connect(
    host="",
    database="",
    user="postgres",
    password="",
    port=
)
cur = con.cursor()
cur.execute("select id, url from sites")

rows = cur.fetchall()

for r in rows:
    print(f"id {r[0]} url {r[1]}")

# cursor close
cur.close()

# close
con.close()

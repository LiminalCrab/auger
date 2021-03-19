import psycopg2

conn = psycopg2.connect(
    host="",
    database="",
    user="",
    password="",
    port=5432)

#open initial cursor
cur = conn.cursor()

#Let's check and see if it works.
cur.execute("SELECT * FROM posts;")
rows = cur.fetchall()
for r in rows:
    print(f"ID: {r[0]} | TITLE: {r[1]} | URI: {r[2]}")
    



cur.close()
conn.close()
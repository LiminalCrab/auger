import asyncio
import psycopg2

#open initial connection
conn = psycopg2.connect(
    host="",
    database="",
    user="",
    password="",
    port=5432 )

#open initial cursor
cur = conn.cursor()
cur.close()
conn.close()



import sqlite3
conn = sqlite3.connect("mysqlite.db")
cur = conn.cursor()
for row in cur.execute("SELECT * FROM user ORDER BY sc_id DESC"):
    print(row)
conn.close()

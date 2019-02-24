import sqlite3
import requests
import time

v = "5.92"
a_token = ""
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

for cat in cursor.execute("SELECT publicid, * FROM categories"):
    ownerid = cat[0]
    print(ownerid)
    r1 = requests.get("https://api.vk.com/method/wall.get?owner_id="+ownerid+"&count=50&access_token="+a_token+"&v="+v)
    print(r1.json())
    for post in r1.json().get("response").get("items"):
        if time.time() - post["date"] > 86400 and post.get("pinned") != 1:
            break
        postid = post["id"]
        print(ownerid)
        print(postid)
        cursor.execute("INSERT INTO queue VALUES(?,?)", [ownerid, postid])

conn.commit()



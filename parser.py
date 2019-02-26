import sqlite3
import requests
import time

v = "5.92"
a_token = ""
conn = sqlite3.connect("database.db")
cursor1 = conn.cursor()
cursor2 = conn.cursor()

posts = ""
for elem in cursor1.execute("SELECT * FROM queue"):
    if time.time() - elem[2] > 86400:
        posts += elem[0] + '_' + str(elem[1]) + ','
posts = posts[:-1]
print(posts)
r = requests.get("https://api.vk.com/method/wall.getById?posts="+posts+"&access_token="+a_token+"&v="+v)
print(r.json())

for cat in cursor1.execute("SELECT publicid, * FROM categories"):
    ownerid = cat[0]
    print(ownerid)
    r = requests.get("https://api.vk.com/method/wall.get?owner_id="+ownerid+"&count=50&access_token="+a_token+"&v="+v)
    print(r.json())
    for post in r.json().get("response").get("items"):
        if time.time() - post["date"] > 86400 and post.get("pinned") != 1:
            break
        postid = post["id"]
        print(postid)
        cursor2.execute("INSERT INTO queue VALUES(?,?,?)", [ownerid, postid, post["date"]])

conn.commit()



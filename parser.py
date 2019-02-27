import sqlite3
import requests
import time
from PIL import Image
from io import BytesIO

v = "5.92"
a_token = "5d1b3c0842c3cf2b48f1b2ef5d1b2ed2911950e9b903a6ad4d91aea3b40757951fa6d8e323e836fb06cbe"
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
for post in r.json().get("response"):
    att = post.get("attachments")[0]
    if att.get("type") == "photo":
        print(requests.get(att.get("photo").get("sizes")[8].get("url")))
        pic = Image.open(BytesIO(requests.get(att.get("photo").get("sizes")[8].get("url")).content))
        print(post.get("date"))
        cursor1.execute("INSERT INTO posts VALUES(?,?,?,?,?,?)", [post.get("owner_id"), post.get("id"),
                                                                  pic, post.get("likes").get("count"),
                                                                  post.get("views").get("count"),
                                                                  post.get("date")])
'''
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
        cursor2.execute("INSERT INTO queue VALUES(?,?,?)", [ownerid, postid, post.get("date")])

'''
conn.commit()



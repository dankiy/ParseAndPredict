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
        posts += str(elem[0]) + '_' + str(elem[1]) + ','
posts = posts[:-1]
print(posts)
r = requests.get("https://api.vk.com/method/wall.getById?posts="+posts+"&access_token="+a_token+"&v="+v)
print(r)
if posts != "":
    for post in r.json().get("response"):
        att = post.get("attachments")[0]
        if att.get("type") == "photo":
            pic = requests.get(att.get("photo").get("sizes")[-1].get("url")).content
            print(str(post.get("owner_id"))+'_'+str(post.get("id"))+" added")
            cursor1.execute("INSERT INTO posts VALUES(?,?,?,?,?,?)", [post.get("owner_id"), post.get("id"),
                                                                      pic, post.get("likes").get("count"),
                                                                      post.get("views").get("count"), post.get("date")])
print()
for cat in cursor1.execute("SELECT publicid, * FROM categories"):
    ownerid = cat[0]
    print("owner id: " + str(ownerid))
    r = requests.get("https://api.vk.com/method/wall.get?owner_id="+ownerid+"&count=50&access_token="+a_token+"&v="+v)
    for post in r.json().get("response").get("items"):
        if time.time() - post["date"] > 86400 and post.get("pinned") != 1:
            break
        postid = post.get("id")
        print("    post id: " + str(postid))
        cursor2.execute("INSERT INTO queue VALUES(?,?,?)", [ownerid, postid, post.get("date")])

conn.commit()



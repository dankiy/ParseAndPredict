import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS categories (title text, publicid text)")
cursor.execute("CREATE TABLE IF NOT EXISTS posts (publicid text, postid text, pic blob, likes int, subs int, postdate text)")
cursor.execute("CREATE TABLE IF NOT EXISTS queue (publicid text, postid text)")

while True:
    str = input().split()
    if str[0] == "end":
        conn.commit()
        break
    elif str[0] == "add":
        if len(str) < 3:
            print("wrong command")
            continue
        cursor.execute("INSERT INTO categories VALUES(?,?)", [str[1], str[2]])
    elif str[0] == "del":
        if len(str) < 2:
            print("wrong command")
            continue
        cursor.execute("DELETE FROM posts WHERE publicid=?", (str[1],))
        cursor.execute("DELETE FROM categories WHERE publicid=?", (str[1],))
        cursor.execute("DELETE FROM queue WHERE publicid=?", (str[1],))
    elif str[0] == "clr":
        if len(str) < 2:
            print("wrong command")
            continue
        cursor.execute("DELETE FROM posts WHERE publicid=?", (str[1],))
        cursor.execute("DELETE FROM queue WHERE publicid=?", (str[1],))
    else:
        print("unknown command")
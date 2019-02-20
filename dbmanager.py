import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
#cursor.execute("CREATE TABLE categories (title text, url text)")

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
        cursor.execute("DELETE FROM categories WHERE title=?", (str[1],))
    elif str[0] == "clr":
        cursor.execute("DELETE FROM categories")
    else:
        print("unknown command")
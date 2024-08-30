import sqlite3,random
from models import User



user= [
    {
        # "id": "ahsnas",
        "username": "ahsnasser_23@hotmail.com",
        "password": "abc123",
        "active"  :True
    },
    {
        # "id": "arsna",
        "username": "arsalan@hotmail.com",
        "password": "abc1234",
        "active"  :True
    },
    {
        # "id": "faznas",
        "username": "faizan@hotmail.com",
        "password": "ab123",
        "active"  :True
    },
    {
        # "id": "ammarnas",
        "username": "ammar@hotmail.com",
        "password": "abaac123",
        "active"  :True
    },
    {
        # "id": "nass",
        "username": "nasser@hotmail.com",
        "password": "abc123as",
        "active"  :True
    }


]

def getNewId():
    return random.getrandbits(28)

def connect():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INT PRIMARY KEY, username TEXT, password TEXT, active BOOLEAN)")
    conn.commit()
    conn.close()
    for i in user:
        us = User(getNewId(), i["username"], i["password"], i["active"])
        insert(us)


def insert(us):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES (?,?,?,?)", (
        us.id,
        us.username,
        us.password,
        us.active
    ))
    conn.commit()
    conn.close()

def deleteAll():
    conn = sqlite3.connect("user.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM users")
    conn.commit()
    conn.close()

def delete(theId):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (theId,))
    conn.commit()
    conn.close()

def update(us):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET username=?, password=? WHERE id=?", (us.username, us.password, us.id))
    conn.commit()
    conn.close()

def viewall():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    users = []
    for i in rows:
        us = User(i[0],i[1] , i[2], True if i[3] == 1 else False)
        users.append(us)
    conn.close()
    return users

def view(theid):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?",(theid,))
    rows = cur.fetchall()
    users = rows[0] if len(rows) > 0 else None
    # for i in rows:
    #     us = User(i[0],i[1] , i[2], True if i[3] == 1 else False)
    #     users.append(User)
    conn.close()
    return users
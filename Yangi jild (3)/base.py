import sqlite3

conn= sqlite3.connect("base.db")
c= conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        login TEXT UNIQUE, 
        password TEXT, 
        name TEXT, 
        age INTEGER)''')

c.execute("INSERT INTO users (login, password, name, age) VALUES (?, ?, ?, ?)",
    ("admin", "admin", "admin", 20))

conn.commit()
conn.close()
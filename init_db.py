import sqlite3

conn = sqlite3.connect('webcommander.db')

conn.execute('''CREATE TABLE Command
         (id INTEGER PRIMARY KEY     AUTOINCREMENT,
         name           VARCHAR(200)    NOT NULL,
         last_run            timestamp     NULL,
         id_cat        INTEGER     NOT NULL,
         id_note        INTEGER     NULL);''')

conn.execute('''CREATE TABLE Category
         (id INTEGER PRIMARY KEY     AUTOINCREMENT,
         name           VARCHAR(200)    NOT NULL);''')

conn.execute('''CREATE TABLE Notes
         (id INTEGER PRIMARY KEY     AUTOINCREMENT,
         note           VARCHAR(5000)    NULL,
         id_com        INTEGER     NOT NULL);''')

conn.execute("INSERT INTO Category (name) VALUES (?)", ("Forensic",))
conn.commit()
conn.execute("INSERT INTO Category (name) VALUES (?)", ("Linux-basic",))
conn.execute("INSERT INTO Category (name) VALUES (?)", ("Python",))
conn.execute("INSERT INTO Command (name,id_cat) VALUES (?,?)", ("ll",0))
conn.commit()
conn.execute("INSERT INTO Notes (note, id_com) VALUES (?, ?)", ("# Test", 1))
conn.commit()
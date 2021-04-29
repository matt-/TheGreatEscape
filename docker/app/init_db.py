import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO notes (content) VALUES (?)", ("Hello Captain, <br><br>Welcome to the Captain's log. You can add your notes as you continue on your journey. <br><br><img src='https://maustin.net/img/contrast_cat.png'><br><br>../SpaceCat",))

connection.commit()
connection.close()

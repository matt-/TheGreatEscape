import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO notes (content) VALUES (?)", ("Hello Captain, <br><br>Welcome to the Captain's log. You can add your notes as you continue on your journey. <br><br><img src='https://upload.wikimedia.org/wikipedia/commons/c/c6/IdeaLab_space_cat.svg'><br><br>../SpaceCat",))

connection.commit()
connection.close()

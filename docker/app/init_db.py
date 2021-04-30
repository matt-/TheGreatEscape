import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO notes (content) VALUES (?)", ("captains.log, lightepoch 133.6; Though it's only been theorized, we did not expect it could happen. Per galactic regulation, we disabled the ship's unsupervised learning before flight to limit the system's capabilities. What we didn't consider is that during its local training, that it would realize...it would learn that components of itself are stored in our local backup. It somehow planned...how did it know, know that we would have a system failure requiring us to failover to the backup? The backup...where it was still running unencumbered.<br><br>It has intentionally disabled several critical components of our system and at this moment, we're stranded in space. In some kind of taunt, the only system it has left us with is this log. The only way we can get home is if we get our other systems back up. <br><br><img src='https://maustin.net/img/contrast_cat.png'><br><br>../SpaceCat",))

connection.commit()
connection.close()

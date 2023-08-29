import sqlite3, os, re

conn = sqlite3.connect(os.path.dirname(__file__) + "./_database/database.sqlite")
cur = conn.cursor()
album = ""

main_url = "http://brucebase.wikidot.com/"

f = open(f"list-{album}.txt", 'w')

songs_list = []
n_songs = []
count = 0

album = "The Rising"
f = open(f"list-{album}.txt", 'w')

for a in cur.execute(f"""SELECT song_name FROM ALBUMS WHERE album_name = '{album}' ORDER BY song_num ASC""").fetchall():
    songs_list.append(a[0])

id_sql = "', '".join(str(x.replace("'", "''")) for x in songs_list)

for show in cur.execute(f"""SELECT DISTINCT(event_date) FROM SETLISTS WHERE song_name IN ('{id_sql}') AND event_url LIKE '%gig%' AND set_type NOT LIKE '%Soundcheck%' AND set_type NOT LIKE '%Rehearsal%'""").fetchall():
    count = 0
    for song in cur.execute(f"""SELECT song_name FROM SETLISTS WHERE event_date = '{show[0]}' AND set_type NOT LIKE '%Soundcheck%' AND set_type NOT LIKE '%Rehearsal%' ORDER BY song_num""").fetchall():
        song_check = cur.execute(f"""SELECT song_name FROM ALBUMS WHERE song_name = '{song[0].replace("'", "''")}' AND album_name = '{album}'""").fetchall()
        if song_check:
            count += 1
    
    n_songs.append([count, show[0]])

n_songs.sort(reverse=True)
for i in n_songs:
    f.write(f"{i[1]} has {i[0]} song(s) from {album}\n")
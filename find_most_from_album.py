import sqlite3, os, re

conn = sqlite3.connect(os.path.dirname(__file__) + "./_database/database.sqlite")
cur = conn.cursor()
album = ""

main_url = "http://brucebase.wikidot.com/"

f = open(f"list-{album}.txt", 'w')

songs_list = []
n_songs = []
songs = []
count = 0

album = "Tunnel Of Love"
f = open(f"_albums/list-{album}.txt", 'w')

for a in cur.execute(f"""SELECT song_name FROM ALBUMS WHERE album_name = '{album}' ORDER BY song_num ASC""").fetchall():
    songs_list.append(a[0])

id_sql = "', '".join(str(x.replace("'", "''")) for x in songs_list)

for show in cur.execute(f"""SELECT DISTINCT(event_date) FROM SETLISTS WHERE song_name IN ('{id_sql}') AND event_url LIKE '%gig%' AND set_type NOT LIKE '%Soundcheck%' AND set_type NOT LIKE '%Rehearsal%'""").fetchall():
    count = 0
    songs = []
    for song in cur.execute(f"""SELECT song_name FROM SETLISTS WHERE event_date = '{show[0]}' AND set_type NOT LIKE '%Soundcheck%' AND set_type NOT LIKE '%Rehearsal%' ORDER BY song_num""").fetchall():
        song_check = cur.execute(f"""SELECT song_name FROM ALBUMS WHERE song_name = '{song[0].replace("'", "''")}' AND album_name = '{album}'""").fetchall()
        if song_check:
            count += 1
            if song[0] not in songs:
                songs.append(song[0])

    n_songs.append([count, show[0], songs])

n_songs.sort(reverse=True)

"""
below loop is to print number of shows with a count of songs from album
"""
for c in [*set(i[0] for i in n_songs)]:
    curr_count = sum(x.count(c) for x in n_songs)
    print(f"{curr_count} show(s) have {c} song(s) from {album}")

for i in n_songs:
    song_count = n_songs.count(count)
    f.write(f"{i[1]} has {i[0]} song(s) from {album}:\n")
    for s in i[2]:
        f.write(f"\t{s}\n")
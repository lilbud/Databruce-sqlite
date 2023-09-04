import os, re, sqlite3

from data_collection import conn, cur

# to update show manually
# add setlist
# update on_stage
# update all counts

url = "/gig:2023-09-03-metlife-stadium-east-rutherford-nj"
date = "2023-09-03"
setlist_file = open("setlist.txt", "r")
onstage_file = open("onstage.txt", "r")
show = []
onStage = []
count = 1

#28	1965-10-00	/gig:1965-10-00-reception-hall-monmouth-county-nj	/song:unknown	Unknown Song	Show	9	9
#id, event_date, event_url, song_url, song_name, set_type, song_num_in_set, song_num
for s in setlist_file.read().splitlines():
    song_info = cur.execute(f"""SELECT song_url, song_name FROM SONGS WHERE song_name LIKE '%{s.replace("'", "''")}%'""").fetchone()
    if len(song_info[1]) != len(s):
        song_info = cur.execute(f"""SELECT song_url, song_name FROM SONGS WHERE song_name LIKE '{s.replace("'", "''")}'""").fetchone()

    show.append([date, url, song_info[0], song_info[1], "Show", count, count])
    count += 1

cur.executemany("""INSERT OR IGNORE INTO SETLISTS VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)""", show)
conn.commit()

from data_collection import setlist_to_events
setlist_to_events()

for o in onstage_file.read().splitlines():
    b = cur.execute(f"""SELECT band_name FROM BANDS WHERE band_url LIKE '{o}'""").fetchone()
    p = cur.execute(f"""SELECT person_name FROM PERSONS WHERE person_url LIKE '{o}'""").fetchone()

    if b:
        onStage.append([url, o, b[0], "Band"])
    elif p:
        onStage.append([url, o, p[0], "Person"])

cur.executemany("""INSERT OR IGNORE INTO ON_STAGE VALUES (NULL, ?, ?, ?, ?)""", onStage)
conn.commit()

from update import update_counts
update_counts()
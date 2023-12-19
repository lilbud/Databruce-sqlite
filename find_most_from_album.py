import sqlite3, os, re
from helper_stuff import *

conn = sqlite3.connect(os.path.dirname(__file__) + "./_database/database.sqlite")
cur = conn.cursor()
album = ""

main_url = "http://brucebase.wikidot.com/"

albums_not_full = [
    "Nebraska",
    "Tunnel Of Love",
    "Human Touch",
    "Lucky Town",
    "The Ghost Of Tom Joad",
    "The Rising",
    "Devils & Dust",
    "We Shall Overcome",
    "Magic",
    "Working On A Dream",
    "Wrecking Ball",
    "High Hopes",
    "American Beauty EP",
    "Western Stars",
    "Letter To You",
    "Only The Strong Survive",
]

albums_full = [
    "Greetings From Asbury Park, N.J.",
    "The Wild, The Innocent & The E Street Shuffle",
    "Born To Run",
    "Darkness On The Edge Of Town",
    "The River",
]


def album_shows(album, year):
    songs_list = []
    n_songs = []
    songs = []
    album_year = 0
    count = 0

    # album = "working on a dream"

    for a in cur.execute(
        f"""SELECT song_url, album_year FROM ALBUMS WHERE album_name = '{album}' ORDER BY song_num ASC"""
    ).fetchall():
        songs_list.append(a[0])
        album_year = a[1]

    id_sql = "', '".join(str(x.replace("'", "''")) for x in songs_list)

    # uncomment first line and comment second to filter by year of albums release
    # for show in cur.execute(f"""SELECT DISTINCT(event_date) FROM SETLISTS WHERE song_name IN ('{id_sql}') AND event_url LIKE '%gig%' AND set_type NOT LIKE '%Soundcheck%' AND set_type NOT LIKE '%Rehearsal%' AND event_date LIKE '{year}%'""").fetchall():
    for show in cur.execute(
        f"""SELECT DISTINCT(event_url) FROM SETLISTS WHERE song_url IN ('{id_sql}') AND event_url LIKE '%gig%' AND set_type NOT LIKE '%Soundcheck%' AND set_type NOT LIKE '%Rehearsal%'"""
    ).fetchall():
        count = 0
        songs = []
        for song in cur.execute(
            f"""SELECT DISTINCT(song_url) FROM SETLISTS WHERE event_url LIKE '%{show[0]}%' AND set_type NOT LIKE '%Soundcheck%' AND set_type NOT LIKE '%Rehearsal%' ORDER BY song_num"""
        ).fetchall():
            song_check = cur.execute(
                f"""SELECT song_url FROM ALBUMS WHERE song_url = '{song[0].replace("'", "''")}' AND album_name = '{album}'"""
            ).fetchall()
            if song_check:
                count += 1
                if song[0] not in songs:
                    songs.append(song[0])

        if count > 0:
            n_songs.append([count, show[0], songs])

    n_songs.sort(reverse=True)

    """
    below loop is to print number of shows with a count of songs from album
    """
    for c in [*set(i[0] for i in n_songs)]:
        curr_count = sum(x.count(c) for x in n_songs)
        print(f"{curr_count} show(s) have {c}/{len(songs_list)} song(s) from {album}")

    f = open(f"_albums/list-{album_year}-{album}.txt", "w")

    for i in n_songs:
        if len(songs_list) > 0:
            f.write(f"{i[1]} has {i[0]}/{len(songs_list)} song(s) from {album}:\n")
            for s in i[2]:
                f.write(f"\t{s}\n")


# for a in albums_full:
#     album_shows(a, albums[a][0])
album_shows("Tunnel Of Love", 2005)

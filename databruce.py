import os
import re
import sqlite3
import datetime
from zoneinfo import ZoneInfo

conn = sqlite3.connect(os.path.dirname(__file__) + "/_database/database.sqlite")
cur = conn.cursor()
cDate = datetime.datetime.now(ZoneInfo('US/Eastern'))
main_url = "http://brucebase.wikidot.com/"

os.system('cls')

def on_this_day(date):
    if len(date) == 0:
        date = "'%-" + cDate.strftime("%m") + "-" + cDate.strftime("%d") + "'"
    else:
        date = "'%-" + date + "'"

    for i in cur.execute(f"""SELECT * FROM EVENTS WHERE event_date LIKE {date}""").fetchall():
        print("Date: " + i[1])
        print("Event Location: " + i[3])
        print("Event Link: " + main_url + i[2].strip("/") + "\n")

def song_finder(song):
    #0,  1,    2,     3,     4,     5
    #id, url, name, first, last, num_plays
    s = cur.execute(f"""SELECT * FROM SONGS WHERE song_name LIKE '%{song.replace("'", "''")}%'""").fetchone()

    if s:
        f = cur.execute(f"""SELECT event_venue, event_city, event_state, event_country, show FROM EVENTS WHERE event_date = \"{s[3]}\"""").fetchone()
        l = cur.execute(f"""SELECT event_venue, event_city, event_state, event_country, show FROM EVENTS WHERE event_date = \"{s[4]}\"""").fetchone()

        f_location = ", ".join(filter(None, f))
        l_location = ", ".join(filter(None, l))

        opener = cur.execute(f"""SELECT COUNT(song_url) FROM SETLISTS WHERE song_url = \"{s[1]}\" AND song_num=1""").fetchone()
        closer = cur.execute(f"""SELECT COUNT(event_url) FROM EVENTS WHERE setlist LIKE \"'%{song.replace("'", "''")}%'\"""").fetchone()

        print("\nSong Name: " + s[2])
        print("Song Link: " + main_url + s[1].strip("/"))
        print("Num Times Played: " + str(s[5]))
        print("First Played: " + s[3] + " - " + f_location)
        print("Last Played: " + s[4] + " - " + l_location)
        print("Number of Times as Show Opener: " + str(opener[0]))
        print("Number of Times as Show Closer: " + str(closer[0]) + "\n")

    else:
        print("\nNo Results Found For: " + song + "\n")

def setlist_finder(date):
    if cur.execute(f"""SELECT * FROM EVENTS WHERE event_date = \"{date}\"""").fetchall():
        for r in cur.execute(f"""SELECT * FROM EVENTS WHERE event_date LIKE \"{date}\"""").fetchall():
            #id, date, event_url, location_url, venue, city, state, country, show, tour, setlist

            location = ", ".join(list(filter(None, r[4:9])))
            event_url = r[2]
            header = r[1] + " - " + location
            print("-"*len(header))
            print(header)

            for s in cur.execute(f"""SELECT DISTINCT(set_type) FROM SETLISTS WHERE event_url = \"{r[2]}\" ORDER BY setlist_song_id ASC""").fetchall():
                print("\n" + s[0] + ":")
                setlist = cur.execute(f"""SELECT song_name FROM SETLISTS WHERE event_url = \"{r[2]}\" AND set_type = \"{s[0]}\" ORDER BY song_num ASC""")
                print(", ".join([x[0] for x in setlist.fetchall()]))

        print("-"*len(header))

    else:
        print("Show not found")

def setlist_matching(seq):
    sequence = []

    for song in re.split(", *", seq):
        # song_name = "'%" + song.replace("'", "''") + "%'"
        s = cur.execute(f"""SELECT song_name FROM SONGS WHERE song_name LIKE '%{song}%'""").fetchone()
        sequence.append(s[0])

    song_list = ", ".join(sequence).replace("'", "''")
    setlists = cur.execute(f"""SELECT event_date, event_venue, event_city, event_state, event_country, show, event_url from EVENTS WHERE setlist LIKE '%{song_list}%'""").fetchall()

    header = str(len(setlists)) + " Shows Where This Sequence Took Place (first 5 shown): " + ", ".join(sequence)
    print("-"*len(header))
    print(header)

    for show in setlists[0:5]:
        location = ", ".join(list(filter(None, show[1:6])))
        print("\t" + show[0] + " - " + location)
    
    print("-"*len(header))

def menu():
    cmd = ""
    print("Databruce Menu")
    print("A (kinda) frontend to interact with the Databruce db")
    print("(Note: the best I can manage with no frontend skills)")
    
    while cmd != "exit":
        print("\nOptions:\n\t[!sl or !setlist YYYY-MM-DD] Setlist Finder (Find Setlists By Date)\n\t[!song SONG NAME] Song Finder (Find Songs by Name\n\t[!otd or !onthisday MM-DD] On This Day (Find Events from this Day)\n\t[!match song1, song2...] Setlist Matching (Find Shows Where a Specific Sequence Occurred)")

        cmd = input("\nEnter Command: ")

        if re.search("!(setlist|sl)", cmd):
            setlist_finder(re.sub("!(setlist|sl) ", "", cmd))
        elif re.search("!song", cmd):
            song_finder(re.sub("!song ", "", cmd))
        elif re.search("!(onthisday|otd)", cmd):
            on_this_day(re.sub("!(onthisday|otd) *", "", cmd))
        elif re.search("!match", cmd):
            setlist_matching(re.sub("!match ", "", cmd).replace("'", "''"))
        else:
            break

menu()

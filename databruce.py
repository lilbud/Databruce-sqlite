import os, re, sqlite3, datetime
from zoneinfo import ZoneInfo

conn = sqlite3.connect(os.path.dirname(__file__) + "/_database/database.sqlite")
cur = conn.cursor()
cDate = datetime.datetime.now(ZoneInfo('US/Eastern'))
main_url = "http://brucebase.wikidot.com/"

os.system('cls')

def on_this_day(date):
    if not date:
        date = "-" + cDate.strftime("%m") + "-" + cDate.strftime("%d")
    else:
        date = "-" + date

    for i in cur.execute("""SELECT * FROM EVENTS WHERE event_date LIKE '%""" + date + "'").fetchall():
        print("Date: " + i[1])
        print("Event Location: " + i[3])
        print("Event Link: " + main_url + i[2].strip("/") + "\n")

def song_finder(song):
    #0,  1,    2,     3,     4,     5
    #id, url, name, first, last, num_plays
    s = cur.execute("""SELECT * FROM SONGS WHERE song_name LIKE '%""" + song + "%'").fetchone()

    if s:
        f = cur.execute("""SELECT event_name FROM EVENTS WHERE event_date=?""", (s[3],)).fetchone()
        l = cur.execute("""SELECT event_name FROM EVENTS WHERE event_date=?""", (s[4],)).fetchone()

        opener = cur.execute("""SELECT COUNT(song_url) FROM SETLISTS WHERE song_url=? AND song_num=1""", (s[1],)).fetchone()
        closer = cur.execute("""SELECT COUNT(event_url) FROM EVENTS WHERE setlist LIKE '%""" + song + "'").fetchone()

        print("\nSong Name: " + s[2])
        print("Song Link: " + main_url + s[1].strip("/"))
        print("Num Times Played: " + str(s[5]))
        print("First Played: " + s[3] + " - " + f[0])
        print("Last Played: " + s[4] + " - " + l[0])
        print("Number of Times as Show Opener: " + str(opener[0]))
        print("Number of Times as Show Closer: " + str(closer[0]) + "\n")


    else:
        print("\nNo Results Found For: " + song + "\n")

def setlist_finder(date): 
    if cur.execute("""SELECT * FROM EVENTS WHERE event_date LIKE '%""" + date + "'").fetchall():
        for r in cur.execute("""SELECT * FROM EVENTS WHERE event_date LIKE '%""" + date + "'").fetchall():
            #id, date, event_url, name, location, tour
            event_url = r[2]
            header = r[1] + " - " + r[3]
            print("-"*len(header))
            print(header)
            
            for s in cur.execute("""SELECT DISTINCT(set_type) FROM SETLISTS WHERE event_url=? ORDER BY setlist_song_id ASC""", (r[2],)).fetchall():
                print("\n" + s[0] + ":")
                setlist = cur.execute("""SELECT song_name FROM SETLISTS WHERE event_url=? AND set_type=? ORDER BY song_num ASC""", (r[2], s[0],))
                print(", ".join([x[0] for x in setlist.fetchall()]))
        
        print("-"*len(header))

    else:
        print("Show not found")

def setlistMatching(seq):
    sequence = []

    for song in re.split(", *", seq):
        s = cur.execute("""SELECT song_name FROM SONGS WHERE song_name LIKE '%""" + song + "%'").fetchone()
        sequence.append(s[0])

    setlists = cur.execute("""SELECT event_date, event_name, event_url from EVENTS WHERE setlist LIKE '%""" + ", ".join(sequence).replace("'", "''") + "%'").fetchall()
    
    print(str(len(setlists)) + " Shows Where This Sequence Took Place (first 10 shown): " + ", ".join(sequence))
    
    for show in setlists[:10]:
        print(show[0] + " - " + show[1])

def menu():
    print("Databruce Menu")
    print("A (kinda) frontend to interact with the Databruce db")
    print("(Note: the best I can manage with no frontend skills)\n")

    print("Options:\n\t[!sl or !setlist YYYY-MM-DD] Setlist Finder (Find Setlists By Date)\n\t[!song SONG NAME] Song Finder (Find Songs by Name\n\t[!otd or !onthisday MM-DD] On This Day (Find Events from this Day)\n\t[!match song1, song2...] Setlist Matching (Find Shows Where a Specific Sequence Occurred)")

    cmd = input("\nEnter Command: ")

    if re.search("!(setlist|sl)", cmd):
        setlist_finder(re.sub("!(setlist|sl) ", "", cmd))
    elif re.search("!song", cmd):
        song_finder(re.sub("!song ", "", cmd))
    elif re.search("!(onthisday|otd)", cmd):
        on_this_day(re.sub("!(onthisday|otd) ", "", cmd))
    elif re.search("!match", cmd):
        setlistMatching(re.sub("!match ", "", cmd).replace("'", "''"))

menu()
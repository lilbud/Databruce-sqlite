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
        print("Event Title: " + i[2])
        print("Event Link: " + main_url + i[3].strip("/") + "\n")

def song_finder(song):
    #id, url, song_name, num_performances
    s = cur.execute("""SELECT * FROM SONGS WHERE song_name LIKE '%""" + song + "%'").fetchone()

    if s:
        f = cur.execute("""SELECT event_url FROM SETLISTS where song_url=? ORDER BY setlist_song_id ASC""", (s[1],)).fetchone()
        l = cur.execute("""SELECT event_url FROM SETLISTS where song_url=? ORDER BY setlist_song_id DESC""", (s[1],)).fetchone()

        firstplayed = cur.execute("""SELECT event_date, event_name FROM EVENTS WHERE event_url=?""", (f[0],)).fetchone()
        lastplayed = cur.execute("""SELECT event_date, event_name FROM EVENTS WHERE event_url=?""", (l[0],)).fetchone()

        print("\nSong Name: " + s[2])
        print("Song Link: " + main_url + s[1].strip("/"))
        print("Num Times Played: " + str(s[3]))
        print("First Played: " + " - ".join(firstplayed))
        print("Last Played: " + " - ".join(lastplayed) + "\n")
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

def menu():
    print("Databruce Menu")
    print("A (kinda) frontend to interact with the Databruce db")
    print("(Note: the best I can manage with no frontend skills)\n")

    print("Options:\n[1] Setlist Finder (Find Setlists By Date)\n[2] Song Finder (Find Songs by Name\n[3] On This Day (Find Events from this Day)\n")

    match input("Select Option: "):
        case "1": #setlist
            setlist_finder(input("Enter Date to Find Setlist For (YYYY-MM-DD Format): "))
        case "2": #song finder
            song_finder(input("Enter Song to Find: "))
        case "3": #on this day
            on_this_day(input("Enter Date to Find Shows For (MM-DD Format) or leave blank for current day: "))

menu()
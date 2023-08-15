"""
Project Name: Databruce
Author Name: Lilbud
Name: Update
File Purpose: Updates the Database file, uses the functions in Data_Collection
"""

import time
import winsound
import datetime
from data_collection import get_bands, get_people, get_songs, get_venues, get_tours, setlist_to_events
from data_collection import get_albums, get_events_by_year, get_tour_events, get_show_info
from data_collection import conn, cur
from helper_stuff import run_time

current_year = int(datetime.datetime.now().date().strftime("%Y"))
start_time = datetime.datetime.now()

def update_counts():
    """update various play/performance counts"""
    for s in cur.execute("""SELECT song_url, song_name FROM SONGS""").fetchall():
        f = l = ''
        count = cur.execute(f"""SELECT COUNT(\"{s[0]}\") FROM SETLISTS WHERE song_url = \"{s[0]}\" AND set_type NOT IN ('Rehearsal', 'Soundcheck')""").fetchone()[0]

        if count > 0:
            f = cur.execute(f"""SELECT event_date FROM SETLISTS WHERE song_url LIKE '{s[0]}' AND set_type NOT IN ('Rehearsal', 'Soundcheck') ORDER BY event_date ASC""").fetchone()
            l = cur.execute(f"""SELECT event_date FROM SETLISTS WHERE song_url LIKE '{s[0]}' AND set_type NOT IN ('Rehearsal', 'Soundcheck') ORDER BY event_date DESC""").fetchone()

            if f and l:
                cur.execute(f"""UPDATE SONGS SET num_plays={count}, first_played=\"{f[0]}\", last_played=\"{l[0]}\" WHERE song_url=\"{s[0]}\"""")
            else:
                cur.execute(f"""UPDATE SONGS SET num_plays={count} WHERE song_url=\"{s[0]}\"""")
        else:
            cur.execute(f"""UPDATE SONGS SET num_plays='0' WHERE song_url=\"{s[0]}\"""")

        conn.commit()

    for v in cur.execute("""SELECT venue_url FROM VENUES""").fetchall():
        count = cur.execute(f"""SELECT COUNT(\"{v[0]}\") FROM EVENTS WHERE location_url=\"{v[0]}\"""").fetchone()
        cur.execute(f"""UPDATE VENUES SET num_performances={count[0]} WHERE venue_url=\"{v[0]}\"""")
        conn.commit()

    for b in cur.execute("""SELECT band_url FROM BANDS""").fetchall():
        count = cur.execute(f"""SELECT COUNT(\"{b[0]}\") FROM ON_STAGE WHERE relation_url=\"{b[0]}\"""").fetchone()
        cur.execute(f"""UPDATE BANDS SET num_performances={count[0]} WHERE band_url=\"{b[0]}\"""")
        conn.commit()

    for p in cur.execute("""SELECT person_url FROM PERSONS""").fetchall():
        count = cur.execute(f"""SELECT COUNT(\"{p[0]}\") FROM ON_STAGE WHERE relation_url=\"{p[0]}\"""").fetchone()
        cur.execute(f"""UPDATE PERSONS SET num_appearances={count[0]} WHERE person_url=\"{p[0]}\"""")
        conn.commit()

    for t in cur.execute("""SELECT tour_url, tour_name FROM TOURS""").fetchall():
        count = cur.execute(f"""SELECT COUNT(\"{t[1]}\") FROM EVENTS WHERE tour=\"{t[1]}\"""").fetchone()
        cur.execute(f"""UPDATE TOURS SET num_shows={count[0]} WHERE tour_url=\"{t[0]}\"""")
        conn.commit()

    print("Counts Updated Successfully")

def basic_update():
    """builds the database, gets the basic amount of information"""

    get_bands()
    get_people()
    get_songs()
    get_venues()
    get_tours()
    get_albums()

    for i in range(1965, current_year + 1):
        get_events_by_year(i)
        cur.execute("""vacuum;""")
        time.sleep(1)

    for t in cur.execute("""SELECT tour_url, tour_name FROM TOURS""").fetchall():
        get_tour_events(t[0], t[1])
        print(t[1])
        time.sleep(1)

    # uncomment the below lines if running both basic and full update
    # print("Sleeping for: " + str(5) + " seconds")
    # time.sleep(5)

def full_update(start, end): 
    """gets show info for all events in events table"""

    delay = 0
    for i in range(start, end+1):
        print(i)

        for u in cur.execute(f"""SELECT event_url FROM EVENTS WHERE event_date LIKE '{str(i)}%'""").fetchall():
            setcheck = cur.execute(f"""SELECT EXISTS(SELECT 1 FROM SETLISTS WHERE event_url LIKE '%{u[0]}%' LIMIT 1)""").fetchone()

            if setcheck[0] == 0:
                get_show_info(u[0])
                print(u[0])
                time.sleep(1)
                delay = 5
            else:
                delay = 0

        if delay > 0:
            print("Sleeping for: " + str(delay) + " seconds")
            time.sleep(delay)
            cur.execute("""vacuum;""")

#basic_update()
#full_update(2023, 2023)

# #usually can just be run for the current year
full_update(current_year, current_year)

setlist_to_events()
update_counts()
#run_time(start_time)

winsound.Beep(1500, 250)

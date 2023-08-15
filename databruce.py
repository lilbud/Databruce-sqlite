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
        date = f"'%-{cDate.strftime('%m')}-{cDate.strftime('%d')}'"
    else:
        date = f"'%-{date}'"

    for i in cur.execute(f"""SELECT event_date, event_url, event_venue, event_city, event_state, event_country, show FROM EVENTS WHERE event_date LIKE {date}""").fetchall():
        print(f"Date: {i[0]}")
        print(f"Event Location: {', '.join(filter(None, i[2:]))}")
        print(f"Event Link: {main_url}{i[1].strip('/')}\n")

def song_finder(song):
    #0,  1,    2,     3,     4,     5
    #id, url, name, first, last, num_plays
    header = s = ""

    if cur.execute(f"""SELECT * FROM SONGS WHERE song_name LIKE '{song}' OR song_name LIKE '%{song}%'""").fetchone():
        s = cur.execute(f"""SELECT * FROM SONGS WHERE song_name LIKE '{song}' OR song_name LIKE '%{song}%'""").fetchone()

    if s:
        f = cur.execute(f"""SELECT event_venue, event_city, event_state, event_country, show FROM EVENTS WHERE event_date = \"{s[3]}\"""").fetchone()
        l = cur.execute(f"""SELECT event_venue, event_city, event_state, event_country, show FROM EVENTS WHERE event_date = \"{s[4]}\"""").fetchone()

        f_location = ", ".join(filter(None, f))
        l_location = ", ".join(filter(None, l))

        opener = cur.execute(f"""SELECT COUNT(song_url) FROM SETLISTS WHERE song_url = \"{s[1]}\" AND song_num=1""").fetchone()
        closer = cur.execute(f"""SELECT COUNT(event_url) FROM EVENTS WHERE setlist LIKE \"'%{song.replace("'", "''")}%'\"""").fetchone()
        total = cur.execute("""SELECT COUNT(*) FROM EVENTS""").fetchone()
        frequency = f"{round((s[5] / total[0] * 100), 2)}%"
        header = f"Song Name: {s[2]}"
        
        print("-"*len(header))
        print(header)
        print(f"Song Link: {main_url}{s[1].strip('/')}")
        print(f"Num Times Played: {s[5]}")
        print(f"First Played: {s[3]} - {f_location}")
        print(f"Last Played: {s[4]} - {l_location}")
        print(f"Number of Times as Show Opener: {opener[0]}")
        print(f"Number of Times as Show Closer: {closer[0]}" + str(closer[0]))
        print(f"Frequency: {frequency}")
        print("-"*len(header))

    else:
        print("-"*len(header))
        print(f"\nNo Results Found For: {song}\n")
        print("-"*len(header))

def setlist_finder(date):
    if cur.execute(f"""SELECT * FROM EVENTS WHERE event_date = \"{date}\"""").fetchall():
        for r in cur.execute(f"""SELECT * FROM EVENTS WHERE event_date LIKE \"{date}\"""").fetchall():
            #id, date, event_url, location_url, venue, city, state, country, show, tour, setlist

            location = ", ".join(list(filter(None, r[4:9])))
            event_url = r[2]
            header = f"{r[1]} - {location}"
            print("-"*len(header))
            print(header)

            for s in cur.execute(f"""SELECT DISTINCT(set_type) FROM SETLISTS WHERE event_url = \"{r[2]}\" ORDER BY setlist_song_id ASC""").fetchall():
                print(f"\n{s[0]}:")
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
    setlists = cur.execute(f"""SELECT event_date, event_venue, event_city, event_state, event_country, show from EVENTS WHERE setlist LIKE '%{song_list}%'""").fetchall()

    header = f"{str(len(setlists))} Shows Where This Sequence Took Place (first 5 shown): {', '.join(sequence)}"
    print("-"*len(header))
    print(header)

    for show in setlists[0:5]:
        location = ", ".join(list(filter(None, show[1:6])))
        print(f"\t{show[0]} - {location}")
    
    print("-"*len(header))

def city_find(city):
    output = ""
    city_events = cur.execute(f"""SELECT event_date, event_venue, event_city, event_state, event_country, show FROM EVENTS WHERE LOWER(event_city) LIKE '%{city.lower()}%'AND setlist != '' ORDER BY event_id""").fetchall()
    
    if city_events:
        first = f"{city_events[0][0]} - {', '.join(list(filter(None, city_events[0][1:])))}"
        last = f"{city_events[-1][0]} - {', '.join(list(filter(None, city_events[-1][1:])))}"

        output = f"{len(city_events)} Shows Have Happened in {city_events[0][2]}"

        print(f"\n{'-'*len(output)}")
        print(f"Results for City: {city_events[0][2]}")
        print(f"\tNumber of Shows: {len(city_events)}")
        print(f"\tFirst Show: {first}")
        print(f"\tMost Recent Show: {last}")

        print("-"*len(output))
    else:
        print(f"\n{'-'*21}")
        print("ERROR: City Not Found")
        print("-"*21)

def state_find(state):
    state_events = cur.execute(f"""SELECT event_date, event_venue, event_city, event_state, event_country, show FROM EVENTS WHERE LOWER(event_state) LIKE '%{state.lower()}%' AND setlist != '' ORDER BY event_id""").fetchall()
    
    if state_events:
        first = f"{state_events[0][0]} - {', '.join(list(filter(None, state_events[0][1:])))}"
        last = f"{state_events[-1][0]} - {', '.join(list(filter(None, state_events[-1][1:])))}"

        output = f"{len(state_events)} Shows Have Happened in {state_events[0][2]}"

        print(f"\n{'-'*len(output)}")
        print(f"Results for State: {state_events[0][3]}")
        print(f"\tNumber of Shows: {len(state_events)}")
        print(f"\tFirst Show: {first}")
        print(f"\tMost Recent Show: {last}")

        print("-"*len(output))
    else:
        print(f"\n{'-'*21}")
        print("ERROR: State Not Found")
        print("-"*21)

def country_find(country):
    country_events = cur.execute(f"""SELECT event_date, event_venue, event_city, event_state, event_country, show FROM EVENTS WHERE LOWER(event_country) LIKE '%{country.lower()}%' AND setlist != '' ORDER BY event_id""").fetchall()
    
    if country_events:
        first = f"{country_events[0][0]} - {', '.join(list(filter(None, country_events[0][1:])))}"
        last = f"{country_events[-1][0]} - {', '.join(list(filter(None, country_events[-1][1:])))}"

        output = f"{len(country_events)} Shows Have Happened in {country_events[0][2]}"

        print(f"\n{'-'*len(output)}")
        print(f"Results for Country: {country_events[0][4]}")
        print(f"\tNumber of Shows: {len(country_events)}")
        print(f"\tFirst Show: {first}")
        print(f"\tMost Recent Show: {last}")

        print("-"*len(output))
    else:
        print(f"\n{'-'*21}")
        print("ERROR: Country Not Found")
        print("-"*21)

def song_and_year(song, year):
    #id, url, name, first, last, num_plays
    if cur.execute(f"""SELECT * FROM SONGS WHERE song_name LIKE '{song}' OR song_name LIKE '%{song}%'""").fetchone():
        s = cur.execute(f"""SELECT * FROM SONGS WHERE song_name LIKE '{song}' OR song_name LIKE '%{song}%'""").fetchone()

    if s:
        count = cur.execute(f"""SELECT COUNT(*) FROM EVENTS WHERE setlist LIKE '%{song}%' AND event_date LIKE '{year}%'""").fetchone()

        if count:
            print(f"Song Name: {s[2]}")
            print(f"Number of Times Played in {year}: {count[0]}")

def menu():
    cmd = ""
    print("Databruce Menu")
    print("A (kinda) frontend to interact with the Databruce db")
    print("(Note: the best I can manage with no frontend skills)")

    while cmd != "exit":
        print("\nOptions:")
        print("\t[!sl or !setlist YYYY-MM-DD] Setlist Finder (Find Setlists By Date)")
        print("\t[!song SONG_NAME, YEAR (optional)] Song Finder (Find Songs by Name")
        print("\t[!otd or !onthisday MM-DD] On This Day (Find Events from this Day)")
        print("\t[!match song1, song2...] Setlist Matching (Find Shows Where a Specific Sequence Occurred)")
        print("\t[!city CITY_NAME] Find shows that happened in a specific City")
        print("\t[!state STATE ABBREV.] Find shows that happened in a specific US State or Canadian Province (2 Letter Abbreviation)")
        print("\t[!country COUNTRY_NAME] Find shows that happened in a specific Country")

        cmd = input("\nEnter Command: ")

        cmd = re.split(", ", cmd)
        if len(cmd) == 3:
            cmd = [", ".join(cmd[0:1]), cmd[2]]
        elif len(cmd) == 4:
            cmd = [", ".join(cmd[0:2]), cmd[3]]

        if len(cmd) == 1:
            if re.search("!(setlist|sl)", cmd[0]):
                setlist_finder(re.sub("!(setlist|sl) ", "", cmd[0]))
            elif re.search("!song", cmd[0]):
                song_finder(re.sub("!song ", "", cmd[0]).replace("'", "''"))
            elif re.search("!(onthisday|otd)", cmd[0]):
                on_this_day(re.sub("!(onthisday|otd) *", "", cmd[0]))
            elif re.search("!match", cmd[0]):
                setlist_matching(re.sub("!match ", "", cmd[0]).replace("'", "''"))
            elif re.search("!city", cmd[0]):
                city_find(re.sub("!city ", "", cmd[0]).replace("'", "''"))
            elif re.search("!state", cmd):
                state = re.sub("!state ", "", cmd[0])
                if len(state) == 2:
                    state_find(state)
                else:
                    print("Incorrect Input")
            elif re.search("!country", cmd[0]):
                country_find(re.sub("!country ", "", cmd[0]).replace("'", "''"))
            else:
                break
        if len(cmd) == 2:
            if re.search("!song ", cmd[0]):
                song_and_year(re.sub("!song ", "", cmd[0]), cmd[1])

menu()

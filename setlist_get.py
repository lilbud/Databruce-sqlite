import re, os, sqlite3

conn = sqlite3.connect(os.path.dirname(__file__) + "/_database/database.sqlite")
cur = conn.cursor()
date_to_find = ""

while date_to_find != "0":
    date_to_find = input("\nEnter Date or 0 to quit: ")

    event_get = cur.execute(f"""SELECT event_url, location_url, show FROM EVENTS WHERE event_date='{date_to_find}'""").fetchall()

    if event_get:
        for e in event_get:
            location = cur.execute(f"""SELECT venue_name, venue_city, venue_state, venue_country FROM VENUES WHERE venue_url='{e[1]}';""").fetchone()

            if location[3] != "USA":
                print(f"\n{date_to_find} - {', '.join(list(filter(None, location)))}\n")
            else:
                print(f"\n{date_to_find} - {', '.join(list(filter(None, location[0:3])))}\n")

            setlist = cur.execute(f"""SELECT song_name, segue FROM SETLISTS WHERE event_url='{e[0]}' ORDER BY song_num ASC""").fetchall()

            for song in setlist:
                song_name = re.sub(" *(`(The Animals|Them`))", "", song[0]).replace("''", "'")
                if song[1] == 1:
                    print(f"{song_name} >")
                else:
                    print(f"{song_name}")
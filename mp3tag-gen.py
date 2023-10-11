import re, os, sqlite3

conn = sqlite3.connect(os.path.dirname(__file__) + "/_database/database.sqlite")
cur = conn.cursor()
date_to_find = ""
artist = "Bruce Springsteen"

while date_to_find != "0":
    date_to_find = input("\nEnter Folder Path with Show Date in Title or 0 to quit: ")

    event_get = cur.execute(f"""SELECT event_url, location_url, show FROM EVENTS WHERE event_date='{date_to_find}'""").fetchall()

    if event_get:
        for e in event_get:
            artist = "Bruce Springsteen"
            album = setlist = track = year = genre = comment = ""
            artist += f" & {cur.execute(f"""SELECT relation_name FROM RELATIONS WHERE relation_url IN (SELECT relation_url FROM ON_STAGE WHERE event_url='{e[0]}' AND relation_type LIKE 'Band')""").fetchone()[0]}"
            album = ", ".join(filter(None, cur.execute(f"""SELECT venue_name, venue_city, venue_state, venue_country FROM VENUES WHERE venue_url='{e[1]}';""").fetchone()))
            setlist = cur.execute(f"""SELECT song_name, segue FROM SETLISTS WHERE event_url='{e[0]}' ORDER BY song_num ASC""").fetchall()
            track = 1
            year = re.findall("(19|20)\d{2}", e[0])
            genre = ""
            comment = ""
            # %artist%  -  %album%  -  %title%  -  %track%  -  %year%  -  %genre%  -  %comment% <- MP3TAG Export/Import format

            for song in setlist:
                song_name = re.sub(" *(\(The Animals|Them)\).*", "", song[0]).replace("''", "'")
                if song[1] == 1:
                    # print(f"{song_name} >")
                    print(f"{artist}  -  {date_to_find} - {album}  -  {song_name} >  -  {0}  -  {genre}  -  {comment}")
                else:
                    print(f"{artist}  -  {date_to_find} - {album}  -  {song_name}  -  {0}  -  {genre}  -  {comment}")
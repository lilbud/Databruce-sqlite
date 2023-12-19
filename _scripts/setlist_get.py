import re, os, sqlite3

db_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..\\_database\\database.sqlite'))

conn = sqlite3.connect(db_path)
cur = conn.cursor()
path = ""

while path != "0":
    path = input("\nEnter Folder Path to Show with YYYY-MM-DD date or 0 to Exit: ")

    if path != '0':
        date_to_find = re.findall(r"\d{4}-\d{2}-\d{2}", path)[0]

        event_get = cur.execute(f"""SELECT event_url, location_url, show FROM EVENTS WHERE event_date='{date_to_find}'""").fetchall()
        
        if event_get:
            for e in event_get:
                safe_url = re.sub("/(gig|rehearsal|nobruce):", "", e[0])

                output_path = f"{path}\\{safe_url}.txt"
                f = open(output_path, 'w')

                location = cur.execute(f"""SELECT venue_name, venue_city, venue_state, venue_country FROM VENUES WHERE venue_url='{e[1]}';""").fetchone()

                if location[3] != "USA":
                    print(f"\n{date_to_find} - {', '.join(list(filter(None, location)))}\n")
                else:
                    print(f"\n{date_to_find} - {', '.join(list(filter(None, location[0:3])))}\n")

                setlist = cur.execute(f"""SELECT song_name, segue FROM SETLISTS WHERE event_url='{e[0]}' AND set_type NOT LIKE 'Soundcheck' ORDER BY song_num ASC""").fetchall()

                for song in setlist:
                    song_name = re.sub(r" *\((The Animals|Them)\)", "", song[0]).replace("''", "'")
                    if song[1] == 1:
                        f.write(f"{song_name} >\n")
                    else:
                        f.write(f"{song_name}\n")
                
                f.close()
                print(f"file saved to {output_path}")
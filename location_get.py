import re, os, sqlite3

conn = sqlite3.connect(os.path.dirname(__file__) + "/_database/database.sqlite")
cur = conn.cursor()
date_to_find = ""

while date_to_find != "0":
    date_to_find = input("\nEnter Date or 0 to quit: ")

    sql = cur.execute(f"""SELECT venue_name, venue_city, venue_state, venue_country FROM VENUES WHERE venue_url LIKE (SELECT location_url FROM EVENTS WHERE event_date='{date_to_find}');""").fetchone()

    if sql:
        if sql[3] != 'USA':
            print(f"\n{date_to_find} - {', '.join(list(filter(None, sql)))}")
        else:
            print(f"\n{date_to_find} - {', '.join(list(filter(None, sql[0:3])))}")

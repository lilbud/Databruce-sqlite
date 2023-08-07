"""
Project Name: Databruce
Author Name: Lilbud
Name: Update
File Purpose: Updates the Database file, uses the functions in Data_Collection
"""

import sqlite3, time, winsound, datetime
from bs4 import BeautifulSoup as bs4
from data_collection import *
from helper_stuff import *

current_year = int(datetime.datetime.now().date().strftime("%Y"))
start_time = datetime.datetime.now()

def update_counts():
	for s in cur.execute("""SELECT song_url, song_name FROM SONGS""").fetchall():
		count = cur.execute("""SELECT COUNT(?) FROM SETLISTS WHERE song_url=? AND set_type NOT IN ('Rehearsal', 'Soundcheck')""", (s[0], s[0],)).fetchone()

		song_name = "'%" + s[1].replace("'", "''") + "%'"
		
		f = cur.execute("""SELECT event_date FROM EVENTS WHERE setlist LIKE """ + song_name + """ ORDER BY event_date ASC""").fetchone()
		l = cur.execute("""SELECT event_date FROM EVENTS WHERE setlist LIKE """ + song_name + """ ORDER BY event_date DESC""").fetchone()

		if f and l:
			cur.execute("""UPDATE SONGS SET num_plays=?, first_played=?, last_played=? WHERE song_url=?""", (count[0], f[0], l[0], s[0],))
		else:
			cur.execute("""UPDATE SONGS SET num_plays=? WHERE song_url=?""", (count[0], s[0],))
		
		conn.commit()

	for v in cur.execute("""SELECT venue_url FROM VENUES""").fetchall():
		count = cur.execute("""SELECT COUNT(?) FROM EVENTS WHERE event_location=?""", (v[0], v[0])).fetchone()
		cur.execute("""UPDATE VENUES SET num_performances=? WHERE venue_url=?""", (count[0], v[0],))
		conn.commit()

	for b in cur.execute("""SELECT band_url FROM BANDS""").fetchall():
		count = cur.execute("""SELECT COUNT(?) FROM ON_STAGE WHERE relation_url=?""", (b[0], b[0])).fetchone()
		cur.execute("""UPDATE BANDS SET num_performances=? WHERE band_url=?""", (count[0], b[0],))
		conn.commit()

	for p in cur.execute("""SELECT person_url FROM PERSONS""").fetchall():
		count = cur.execute("""SELECT COUNT(?) FROM ON_STAGE WHERE relation_url=?""", (p[0], p[0])).fetchone()
		cur.execute("""UPDATE PERSONS SET num_appearances=? WHERE person_url=?""", (count[0], p[0],))
		conn.commit()

	for t in cur.execute("""SELECT tour_url, tour_name FROM TOURS""").fetchall():
		count = cur.execute("""SELECT COUNT(?) FROM EVENTS WHERE tour=?""", (t[1], t[1])).fetchone()
		cur.execute("""UPDATE TOURS SET num_shows=? WHERE tour_url=?""", (count[0], t[0],))
		conn.commit()

	print("Counts Updated Successfully")

# builds the database, gets the basic amount of information
def basic_update():
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

def full_update(start, end): #gets show info for all events in events table
	delay = 0
	for i in range(start, end+1):
		print(i)
		urls_by_year = cur.execute("""SELECT event_url FROM EVENTS 
			WHERE event_date LIKE """ + "'%" + str(i) + "%'").fetchall()
		
		for u in urls_by_year:
			setcheck = cur.execute("""SELECT EXISTS(SELECT 1 FROM SETLISTS WHERE event_url=? LIMIT 1)""",
				(u[0],)).fetchone()

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
#full_update(current_year, current_year)

#setlistToEvents()
update_counts()
run_time(start_time)

winsound.Beep(1500, 250)
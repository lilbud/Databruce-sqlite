"""
Project Name: Databruce
Author Name: Lilbud
Name: Update
File Purpose: Updates the Database file, uses the functions in Data_Collection
"""

import time
import datetime, re
from data_collection import get_bands, get_people, get_songs, get_venues, get_tours, setlist_to_events
from data_collection import get_albums, get_events_by_year, get_tour_events, get_show_info, jungleland_artwork
from data_collection import conn, cur
from helper_stuff import run_time
from csv_export import csv_export

current_year = int(datetime.datetime.now().date().strftime("%Y"))
start_time = datetime.datetime.now()

def update_counts():
	"""update various play/performance counts"""
	for s in cur.execute("""SELECT song_url FROM SONGS""").fetchall():
		count = cur.execute(f"""SELECT COUNT(\"{s[0]}\"), MIN(event_url), MAX(event_url) FROM SETLISTS WHERE song_url = \"{s[0]}\" AND set_type NOT IN ('Rehearsal', 'Soundcheck')""").fetchone()
		total = cur.execute("""SELECT COUNT(event_id) FROM EVENTS WHERE event_url LIKE '/gig:%'""").fetchone()

		if count[0] > 0:
			first_played = re.findall("\d{4}-\d{2}-\d{2}", count[1])
			last_played = re.findall("\d{4}-\d{2}-\d{2}", count[2])
			frequency = f"{round(((count[0] / total[0]) * 100), 2)}"
			cur.execute(f"""UPDATE SONGS SET num_plays={count[0]}, first_played=\"{first_played[0]}\", last_played=\"{last_played[0]}\", frequency='{frequency}' WHERE song_url=\"{s[0]}\"""")
		else:
			cur.execute(f"""UPDATE SONGS SET num_plays='0' WHERE song_url=\"{s[0]}\"""")

		conn.commit()

	print("Song Count Updated")

	for v in cur.execute("""SELECT venue_url FROM VENUES""").fetchall():
		count = cur.execute(f"""SELECT COUNT(\"{v[0]}\") FROM EVENTS WHERE location_url=\"{v[0]}\"""").fetchone()
		cur.execute(f"""UPDATE VENUES SET num_performances={count[0]} WHERE venue_url=\"{v[0]}\"""")
		conn.commit()

	print("Venue Count Updated")

	for r in cur.execute("""SELECT relation_url FROM RELATIONS""").fetchall():
		count = cur.execute(f"""SELECT COUNT(\"{r[0]}\") FROM ON_STAGE WHERE relation_url=\"{r[0]}\"""").fetchone()
		cur.execute(f"""UPDATE RELATIONS SET appearances={count[0]} WHERE relation_url=\"{r[0]}\"""")
		conn.commit()
	
	print("band and person count updated")

	for t in cur.execute("""SELECT tour_url, tour_name FROM TOURS""").fetchall():
		count = cur.execute(f"""SELECT COUNT(\"{t[1]}\"), MIN(event_date), MAX(event_date) FROM EVENTS WHERE tour=\"{t[1]}\" AND event_url LIKE '/gig:%'""").fetchone()

		# id_sql = "', '".join(str(x[0].replace("'", "''")) for x in cur.execute(f"""SELECT event_date FROM EVENTS WHERE tour='{t[1].replace("'", "''")}' AND event_url LIKE '/gig:%'""").fetchall())
		song_count = cur.execute(f"""SELECT COUNT(DISTINCT(song_name)) FROM SETLISTS WHERE event_url IN (SELECT event_url FROM EVENTS WHERE tour='{t[1].replace("'", "''")}' AND event_url LIKE '/gig:%')""").fetchone()[0]

		cur.execute(f"""UPDATE TOURS SET num_shows={count[0]}, first_show='{str(count[1])}', last_show='{str(count[2])}', num_songs={song_count} WHERE tour_url=\"{t[0]}\"""")
		conn.commit()

	print("Tour Event Count Updated")
	

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
	# print("Sleeping for 5 seconds")
	# time.sleep(5)

def full_update(start, end): 
	"""gets show info for all events in events table"""

	delay = 0
	for i in range(start, end+1):
		print(i)

		# for u in cur.execute(f"""SELECT event_url FROM EVENTS WHERE event_date LIKE '{str(i)}%' AND date(event_date) < date('now', '+1 days')""").fetchall():
		for u in cur.execute(f"""SELECT event_url FROM EVENTS WHERE event_date LIKE '{str(i)}%'""").fetchall():
			setcheck = cur.execute(f"""SELECT EXISTS(SELECT 1 FROM SETLISTS WHERE event_url LIKE '%{u[0]}%' LIMIT 1)""").fetchone()

			if setcheck[0] == 0:
				get_show_info(u[0])
				print(u[0])
				time.sleep(0.5)
				delay = 2

		if start != end:
			print(f"Sleeping for {delay} seconds")
			time.sleep(delay)
			cur.execute("""vacuum;""")

#basic_update()
#usually can just be run for the current year
#full_update(current_year, current_year)

#setlist_to_events()
# jungleland_artwork()
update_counts()
csv_export()
run_time(start_time)

#winsound.Beep(1500, 250)

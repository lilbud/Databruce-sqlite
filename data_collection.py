"""
Project Name: Databruce
Author Name: Lilbud
Name: Data Collection
File Purpose: Functions to get various kinds of data from Brucebase
"""

import os
import sqlite3
import re
import requests
from titlecase import titlecase
from bs4 import BeautifulSoup as bs4
import pandas as pd
from helper_stuff import albums, song_link_corrector, name_fix, show_name_split

main_url = "http://brucebase.wikidot.com/"
event_types = "/(gig|rehearsal|nobruce):"

db_path = os.path.dirname(__file__) + "/_database/database.sqlite"

if os.path.isfile("./_database/database.sqlite"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
else:
    print("Database not found, Run setup.py")
    exit()

def get_bands():
    """
    Gets all the bands that bruce has either played or recorded with
    """

    bands = []
    r = requests.get(main_url + "system:page-tags/tag/band#pages", timeout=5).text
    soup = bs4(r, 'lxml')

    for b in soup.find_all('a', href=re.compile("/relation:.*")):
        if not re.search("-([1-2])$", b.get('href')):
            band_name = b.text.strip()
            if ", The" in b.text or " (The)" in b.text:
                band_name = "The " + re.sub("(, | )(\(The\)|The)", "", b.text.strip())

            bands.append([b.get('href'), band_name, 0])

    cur.executemany("""INSERT OR IGNORE INTO BANDS VALUES (NULL, ?, ?, ?)""",
        sorted(bands, key=lambda band: band[1].replace("The ", "")))

    conn.commit()
    print("Got Bands")

def get_people():
    """
    Gets a list of all the people who have been on stage
    or have otherwise appeared with bruce
    """

    people = []
    r = requests.get(main_url + "system:page-tags/tag/person#pages", timeout=5).text
    soup = bs4(r, 'lxml')

    for p in soup.find_all('a', href=re.compile("/relation:.*")):
        curr = p.text.split(", ")
        curr.reverse()

        if "(Timepiece)" in curr[0]:
            curr[0] = curr[0].replace(" (Timepiece)", "")
            curr[1] = curr[1] + " (Timepiece)"

        people.append([p.get('href'), " ".join(curr), 0])

    cur.executemany("""INSERT OR IGNORE INTO PERSONS VALUES (NULL, ?, ?, ?)""", people)
    conn.commit()

    print("Got People")

def get_songs():
    """Gets the list of songs from the site"""

    url = requests.get(main_url + "system:page-tags/tag/song#pages", timeout=5).text
    soup = bs4(url, "lxml")
    songs = []

    for s in soup.find_all(href=re.compile("/song:.*")):
        #song_url, song_name, album_name, num_plays
        songs.append([s.get('href'), s.text.strip(), "", "", 0])

    cur.executemany("""INSERT OR IGNORE INTO SONGS VALUES (NULL, ?, ?, ?, ?, ?)""", songs)
    conn.commit()

    print("Got Songs")

def get_venues():
    """
    Gets the list of venues from the site
    using the sitemap is the only way to get ALL of the venues
    as many venue pages aren't tagged as such
    """

    url = requests.get(main_url + "system:sitemap", timeout=5).text
    soup = bs4(url, "lxml")
    venues = []

    for v in soup.find_all(href=re.compile("/venue:.*")):
        name = name_fix(venue_name_corrector(v.text.strip()))
        venues.append([v.get('href'), name, 0]) #putting into a list because source page is out of order

    cur.executemany("""INSERT OR IGNORE INTO VENUES VALUES (NULL, ?, ?, ?)""",
        sorted(venues, key=lambda venue: venue[1].replace("The ", "")))

    conn.commit()
    print("Got Venues")

def get_events_by_year(year):
    """
    Gets all the events for a year that match the list of allowed event_types
    which are: gig, rehearsal, nobruce
    these are the only events with setlists
    """

    shows = []

    url = requests.get(main_url + str(year), timeout=5).text
    soup = bs4(url, "lxml")

    for e in soup.find_all('a', href=re.compile(event_types + str(year))):
        if e.find_parent().name == "strong":
            event_url = e.get('href')
            location_url = event_venue = event_city = event_state = event_country = show = tour = setlist = ""
            event_date = e.text[0:10]

            shows.append([event_date, event_url, location_url, event_venue, event_city, event_state, event_country, show, tour, setlist])
            cur.execute("""UPDATE SETLISTS SET event_date=? WHERE event_url=?""", (event_date, event_url))
            conn.commit()

    cur.executemany("""INSERT OR IGNORE INTO EVENTS VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", shows)

    conn.commit()
    print("got events for year: " + str(year))

def get_onStage(tab, url):
    """Gets the list of musicians/people/bands on stage at a given event"""

    onStage = []
    relation_name = relation_type = ""

    for m in tab.find_all(href=re.compile("/relation:.*")):
        # 0 - id, 1 - url, 2 - name (for both)
        b = cur.execute(f"""SELECT band_name FROM BANDS WHERE band_url=\"{m.get('href')}\"""").fetchone()
        p = cur.execute(f"""SELECT person_name FROM PERSONS WHERE person_url=\"{m.get('href')}\"""").fetchone()

        if b:
            relation_name = b[0]
            relation_type = "Band"
        elif p:
            relation_name = p[0]
            relation_type = "Person"

        onStage.append([url, m.get('href'), relation_name, relation_type])

    cur.executemany("""INSERT OR IGNORE INTO ON_STAGE VALUES (NULL, ?, ?, ?, ?)""", onStage)
    conn.commit()

def get_setlist_by_url(tab, url, date):
    """Gets the Setlist for a provided event_url"""

    song_name = ""
    set_type = "Show"
    song_num = 1
    t = tab
    show = []

    if tab.find('td'):
        t = tab.find('td')

    for item in t:
        song_num_in_set = 1
        if item.name is not None:
            if "/rehearsal:" in url:
                set_type = "Rehearsal"
            elif "/nobruce:" in url:
                set_type = "No Bruce"
            else:
                if item.name == 'p' and item.next_element.name == 'strong':
                    set_type = item.next_element.text

            for s in item.find_all('li'):
                song_url = ""
                if s.find('a'):
                    temp = s.find_all('a', href=re.compile("/song:.*"))
                    for i in temp:
                        song_url = song_link_corrector(i.get('href'))
                        song_name = cur.execute("""SELECT song_name FROM SONGS WHERE song_url=?""", (song_url, )).fetchone()[0]
                        show.append([date, url, song_url, song_name, set_type, song_num_in_set, song_num])
                        song_num += 1

                        if temp.index(i) != (len(temp) - 1):
                            song_num_in_set += 1

                elif s.next_element.name != 'sup':
                    if " - " in s.text:
                        temp = s.text.split(" - ")
                        for t in temp:
                            song_name = titlecase(t)
                            show.append([date, url, song_url, song_name, set_type, song_num_in_set, song_num])
                            song_num += 1

                            if temp.index(t) != (len(temp) - 1):
                                song_num_in_set += 1

                    else:
                        song_name = titlecase(s.text)
                        show.append([date, url, song_url, song_name, set_type, song_num_in_set, song_num])
                        song_num += 1

                song_num_in_set += 1

    if show:
        cur.executemany("""INSERT OR IGNORE INTO SETLISTS VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)""", show)
        #cur.execute("""UPDATE EVENTS SET setlist=? WHERE event_url=?""", ((", ".join(x[2] for x in show)), url))
    else:
        # cur.execute("""INSERT OR IGNORE INTO SETLISTS VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)""",
        # 	(url, "", "", set_type, 0, 0, "no set details known"))
        cur.execute("""UPDATE EVENTS SET setlist=? WHERE event_url=?""", ("No set details known", url))
    conn.commit()

def get_show_info(url):
    """Gets show info for a provided URL"""

    r = requests.get(main_url + url.strip("/"), timeout=5)

    if r.status_code == 200:
        soup = bs4(r.text, "lxml")
        venue = soup.find(href=re.compile("/venue:.*"))
        name = show_name_split(soup.find(id="page-title").text.strip()[11:].strip(), url)
        nav = soup.find("ul", {"class": "yui-nav"}).find_all('li')
        date = cur.execute("""SELECT event_date FROM EVENTS WHERE event_url=?""", (url,)).fetchone()

        v = cur.execute("""SELECT venue_url FROM VENUES WHERE venue_url=?""", (venue.get('href'), )).fetchone()

        if v:
            cur.execute("""UPDATE EVENTS SET location_url=? WHERE event_url=?""", (v[0], url))
            conn.commit()

        cur.executemany("""UPDATE EVENTS SET event_venue=?, event_city=?, event_state=?, event_country=?, show=? WHERE event_url=?""", name)
        conn.commit()

        for n in nav:
            if n.text == "On Stage":
                get_onStage(soup.find(id="wiki-tab-0-" + str(nav.index(n))), url)
            if n.text == "Setlist":
                get_setlist_by_url(soup.find(id="wiki-tab-0-" + str(nav.index(n))), url, date[0])
    else:
        print(f"Show Page Not Found For: {url}")

def get_tours():
    """Gets tour names from BB"""

    tour = []
    df = pd.read_html(main_url + 'stats:tour-statistics', extract_links="all", skiprows=(0,1))

    for i in df[0][1]:
        tour_name = i[0]
        if i[1] == "/stats:shows-rvr16-tour":
            tour_name = "The River Tour '16"

        tour.append([i[1], tour_name, 0])

    cur.executemany("""INSERT OR IGNORE INTO TOURS VALUES (NULL, ?, ?, ?)""", tour)
    conn.commit()

def get_tour_events(url, name):
    """Finds the tour that an event belongs to and updates that entry in EVENTS"""

    r = requests.get(main_url + url.strip("/"), timeout=10).text
    soup = bs4(r, "lxml")

    for t in soup.find("div", {"class": "yui-content"}).find_all("li"):
        if t.find('a', href=re.compile(event_types)):
            cur.execute("""UPDATE EVENTS SET tour=? WHERE event_url=? AND tour=?""",
                (name, t.find('a').get('href'), "",))

            conn.commit()

def get_albums():
    """Gets albums and their songs, can be used to find full album shows"""

    r = requests.get(main_url + "stats:song-count-by-album", timeout=5).text
    soup = bs4(r, "lxml")
    album_num = 0
    album = []

    for s in soup.find_all(id=re.compile("wiki-tabview.*")):
        nav = s.find("ul", {"class": "yui-nav"}).find_all('li')

        for n in nav:
            count = 1
            song_url = song_name = ""

            for a in s.find(id="wiki-tab-0-" + str(nav.index(n))).find_all('td'):
                if a.find('a', href=re.compile("/song:.*")):
                    song_url = a.find('a').get('href')
                    song_name = a.find('a').text

                    album.append([n.text, albums[n.text][1], albums[n.text][0], song_url, song_name, count])
                    count += 1
            album_num += 1

    cur.executemany("""INSERT OR IGNORE INTO ALBUMS VALUES (?, ?, ?, ?, ?, ?)""",
        sorted(album, key=lambda album: album[2]))
    conn.commit()
    print("Got Albums")

# figured out afterwards that setlist matching would be much easier
# if I could just match a comma separated list as opposed to my first attempt
# which looked like the following:
# input two songs -> find all shows with those songs ->
# return id of song1 setlist entry -> check if id+1 equals song 2
def setlist_to_events():
    for e in cur.execute("""SELECT event_url FROM EVENTS""").fetchall():
        s = cur.execute("""SELECT song_name FROM SETLISTS WHERE event_url=? AND set_type NOT IN ('Soundcheck','Rehearsal','Pre-show') ORDER BY song_num ASC""", (e[0],)).fetchall()
        setlist = ", ".join(x[0] for x in s)

        cur.execute("""UPDATE EVENTS SET setlist=? WHERE event_url=?""", (setlist, e[0]))
        conn.commit()

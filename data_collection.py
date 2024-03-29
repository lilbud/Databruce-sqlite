"""
Project Name: Databruce
Author Name: Lilbud
Name: Data Collection
File Purpose: Functions to get various kinds of data from Brucebase
"""

import os
import sqlite3
import re
import time
import requests
from titlecase import titlecase
from bs4 import BeautifulSoup as bs4
import pandas as pd
from helper_stuff import (
    albums,
    song_link_corrector,
    name_fix,
    show_name_split,
    venue_name_corrector,
)

main_url = "http://brucebase.wikidot.com/"
event_types = "/(gig|rehearsal|nobruce):"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

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
    r = requests.get(
        f"{main_url}system:page-tags/tag/band#pages", headers, timeout=10
    ).text
    soup = bs4(r, "lxml")

    for b in soup.find_all("a", href=re.compile("/relation:.*")):
        if not re.search("-([1-2])$", b.get("href")):
            band_name = b.text.strip()
            if ", The" in b.text or " (The)" in b.text:
                band_name = "The " + re.sub(r"(, | )(\(The\)|The)", "", b.text.strip())

            bands.append([b.get("href"), band_name, 0, "band"])

    cur.executemany(
        """INSERT OR IGNORE INTO RELATIONS VALUES (NULL, ?, ?, ?, ?)""",
        sorted(bands, key=lambda band: band[1].replace("The ", "")),
    )

    conn.commit()
    print("Got Bands")


def get_people():
    """
    Gets a list of all the people who have been on stage
    or have otherwise appeared with bruce
    """

    people = []
    r = requests.get(
        f"{main_url}system:page-tags/tag/person#pages", headers, timeout=10
    ).text
    soup = bs4(r, "lxml")

    for p in soup.find_all("a", href=re.compile("/relation:.*")):
        curr = p.text.split(", ")  # splits names into first and last
        curr.reverse()  # reverses name to proper "first, last"
        name = " ".join(curr)

        # fixes exactly one persons name, Frank Pagano, as there are two of him, with one being part of a band called "Timepiece"
        # on the site, his name is listed as "Pagano, Frank (Timepiece)", but when reversed gives "Frank (Timepiece) Pagano"
        # this removes it from his first name, and puts it at the end with his last name
        if re.search(r"\(timepiece\)", curr[0], re.IGNORECASE):
            name = f"{curr[0].replace(' (Timepiece)', '')} {curr[1]} (Timepiece)"

        people.append([p.get("href"), name, 0, "person"])

    cur.executemany(
        """INSERT OR IGNORE INTO RELATIONS VALUES (NULL, ?, ?, ?, ?)""", people
    )
    conn.commit()

    print("Got People")


def get_songs():
    """Gets the list of songs from the site"""

    url = requests.get(
        f"{main_url}system:page-tags/tag/song#pages", headers, timeout=10
    ).text
    soup = bs4(url, "lxml")
    songs = []

    for s in soup.find_all(href=re.compile("/song:.*")):
        # song_url, song_name, first_played, last_played, num_plays, opener, closer, frequency
        songs.append([s.get("href").strip(), s.text.strip(), "", "", "", "", "", 0])

    cur.executemany(
        """INSERT OR IGNORE INTO SONGS VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)""", songs
    )
    conn.commit()

    print("Got Songs")


def get_venues():
    """
    Gets the list of venues from the site
    using the sitemap is the only way to get ALL of the venues
    as many venue pages aren't tagged as such
    """

    url = requests.get(f"{main_url}system:sitemap", headers, timeout=5).text
    soup = bs4(url, "lxml")
    venues = []

    for v in soup.find_all(href=re.compile("/venue:.*")):
        name = name_fix(venue_name_corrector(v.text.strip()))
        venue_name = show_name_split(name, v.get("href"))[0]
        venues.append(
            [
                v.get("href").strip(),
                venue_name[0],
                venue_name[1],
                venue_name[2],
                venue_name[3],
                0,
            ]
        )  # putting into a list because source page is out of order

    cur.executemany(
        """INSERT OR IGNORE INTO VENUES VALUES (NULL, ?, ?, ?, ?, ?, ?)""",
        sorted(venues, key=lambda venue: venue[1].replace("The ", "")),
    )

    conn.commit()
    print("Got Venues")


def get_events_by_year(year):
    """
    Gets all the events for a year that match the list of allowed event_types
    which are: gig, rehearsal, nobruce
    these are the only events with setlists
    """

    shows = []
    url = requests.get(f"{main_url}{str(year)}", headers, timeout=10).text
    soup = bs4(url, "lxml")

    for e in soup.find_all("a", href=re.compile(f"{event_types}{str(year)}")):
        if e.find_parent().name == "strong":
            event_url = e.get("href")
            location_url = show = tour = setlist = ""

            event_date = re.findall(r"\d{4}-\d{2}-\d{2}", e.text)[0]

            shows.append(
                [
                    event_date,
                    event_url,
                    location_url,
                    show,
                    tour,
                    setlist,
                    0,
                    0,
                ]
            )
            # cur.execute(
            #     """UPDATE SETLISTS SET event_date=? WHERE event_url=?""",
            #     (event_date, event_url),
            # )
            # conn.commit()

    cur.executemany(
        """INSERT OR IGNORE INTO EVENTS VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)""", shows
    )
    conn.commit()

    print("got events for year: " + str(year))


def get_onStage(tab, url):
    """Gets the list of musicians/people/bands on stage at a given event"""

    onStage = []

    for m in tab.find_all(href=re.compile("/relation:.*")):
        r = cur.execute(
            f"""SELECT relation_url, relation_type FROM RELATIONS WHERE relation_url LIKE '{m.get('href')}'"""
        ).fetchone()

        if r:
            if r[1] == "band":
                onStage.append([url, r[0], "Band"])
            elif r[1] == "person":
                onStage.append([url, r[0], "Person"])

    cur.executemany(
        """INSERT OR IGNORE INTO ON_STAGE VALUES (NULL, ?, ?, ?)""", onStage
    )
    conn.commit()


def get_setlist_by_url(tab, url, date):
    """Gets the Setlist for a provided event_url"""
    song_name = ""
    set_type = "Show"
    song_num = 1
    t = tab
    show = []

    if tab.find("td"):
        t = tab.find("td")

    for item in t:
        song_num_in_set = 1
        if item.name is not None:
            if "/rehearsal:" in url:
                set_type = "Rehearsal"
            elif "/nobruce:" in url:
                set_type = "No Bruce"
            else:
                if item.name == "p" and item.next_element.name == "strong":
                    set_type = item.next_element.text

            for s in item.find_all("li"):
                song_url = ""

                if s.next_element.name != "sup":
                    if s.find_all():  # gets links
                        temp = s.find_all("a", href=re.compile("/song:.*"))

                        if len(temp) > 1:  # segues
                            for i in temp:
                                segue = 0

                                if temp.index(i) != (len(temp) - 1):
                                    segue = 1

                                song_url = song_link_corrector(i.get("href"))
                                song_name = cur.execute(
                                    f"""SELECT song_name FROM SONGS WHERE song_url LIKE '{song_url}'"""
                                ).fetchone()[0]
                                show.append(
                                    [
                                        url,
                                        song_url,
                                        song_name,
                                        set_type,
                                        song_num_in_set,
                                        song_num,
                                        segue,
                                        0,
                                        0,
                                    ]
                                )
                                song_num += 1

                                if temp.index(i) != (len(temp) - 1):
                                    song_num_in_set += 1

                        else:  # no segue, single song with link
                            song_url = song_link_corrector(s.find("a").get("href"))
                            song_name = cur.execute(
                                f"""SELECT song_name FROM SONGS WHERE song_url LIKE '{song_url}'"""
                            ).fetchone()[0]
                            show.append(
                                [
                                    url,
                                    song_url,
                                    song_name,
                                    set_type,
                                    song_num_in_set,
                                    song_num,
                                    0,
                                    0,
                                    0,
                                ]
                            )
                            song_num += 1

                    else:  # no links
                        if " - " in s.text:  # segues in text
                            temp = s.text.split(" - ")
                            for i in temp:
                                segue = 0
                                song_name = titlecase(i)

                                if temp.index(i) != (len(temp) - 1):
                                    segue = 1

                                show.append(
                                    [
                                        url,
                                        song_url,
                                        song_name,
                                        set_type,
                                        song_num_in_set,
                                        song_num,
                                        segue,
                                        0,
                                        0,
                                    ]
                                )
                                song_num += 1

                                if temp.index(i) != (len(temp) - 1):
                                    song_num_in_set += 1

                        else:  # no segue
                            song_name = titlecase(s.text)
                            show.append(
                                [
                                    url,
                                    song_url,
                                    song_name,
                                    set_type,
                                    song_num_in_set,
                                    song_num,
                                    0,
                                    0,
                                    0,
                                ]
                            )
                            song_num += 1

                    song_num_in_set += 1

    if show:
        cur.executemany(
            """INSERT OR IGNORE INTO SETLISTS VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            show,
        )
        conn.commit()
    else:
        cur.execute(
            """UPDATE EVENTS SET setlist=? WHERE event_url=?""",
            ("No set details known", url),
        )
        conn.commit()


def get_show_info(url):
    """Gets show info for a provided URL"""
    r = requests.get(f"{main_url}{url.strip('/')}", headers)

    if r.status_code == 200:
        soup = bs4(r.text, "lxml")
        venue = soup.find(href=re.compile("/venue:.*"))
        nav = soup.find("ul", {"class": "yui-nav"}).find_all("li")
        date = cur.execute(
            f"""SELECT event_date FROM EVENTS WHERE event_url LIKE '{url}'"""
        ).fetchone()

        v = cur.execute(
            f"""SELECT venue_url FROM VENUES WHERE venue_url LIKE '{venue.get('href')}'"""
        ).fetchone()

        if v:
            cur.execute(
                """UPDATE EVENTS SET location_url=? WHERE event_url=?""", (v[0], url)
            )
            conn.commit()

        for n in nav:
            # if n.text == "On Stage":
            #     get_onStage(soup.find(id=f"wiki-tab-0-{nav.index(n)}"), url)
            if n.text == "Setlist":
                get_setlist_by_url(
                    soup.find(id=f"wiki-tab-0-{nav.index(n)}"), url, date[0]
                )
    else:
        print(f"Show Page Not Found For: {url}")


def get_tours():
    """Gets tour names from BB"""

    tour = []
    df = pd.read_html(
        f"{main_url}stats:tour-statistics", extract_links="all", skiprows=(0, 1)
    )

    for i in df[0][1]:
        tour_name = i[0]
        if i[1] == "/stats:shows-rvr16-tour":
            tour_name = "The River Tour '16"

        tour.append([i[1], tour_name, "", "", 0, 0])

    cur.executemany(
        """INSERT OR IGNORE INTO TOURS VALUES (NULL, ?, ?, ?, ?, ?, ?)""", tour
    )
    conn.commit()


def get_tour_events(url, name):
    """Finds the tour that an event belongs to and updates that entry in EVENTS"""

    print(name)
    r = requests.get(f"{main_url}{url.strip('/')}", headers, timeout=10).text
    soup = bs4(r, "lxml")

    for t in soup.find("div", {"class": "yui-content"}).find_all("li"):
        if t.find("a", href=re.compile(event_types)):
            print(t.find("a").get("href"))
            tour_name = name
        else:
            tour_name = ""

        cur.execute(
            """UPDATE EVENTS SET tour=? WHERE event_url=? AND tour=?""",
            (
                tour_name,
                t.find("a").get("href"),
                "",
            ),
        )

        conn.commit()


def get_albums():
    """Gets albums and their songs, can be used to find full album shows"""

    r = requests.get(f"{main_url}stats:song-count-by-album", headers).text
    soup = bs4(r, "lxml")
    album_num = 0
    album = []

    for s in soup.find_all(id=re.compile("wiki-tabview.*")):
        nav = s.find("ul", {"class": "yui-nav"}).find_all("li")

        for n in nav:
            count = 1
            song_url = song_name = ""

            for a in s.find(id=f"wiki-tab-0-{nav.index(n)}").find_all("td"):
                if a.find("a", href=re.compile("/song:.*")):
                    song_url = a.find("a").get("href")
                    song_name = a.find("a").text

                    album.append(
                        [
                            n.text,
                            albums[n.text][1],
                            albums[n.text][0],
                            song_url,
                            song_name,
                            count,
                        ]
                    )
                    count += 1
            album_num += 1

    cur.executemany(
        """INSERT OR IGNORE INTO ALBUMS VALUES (?, ?, ?, ?, ?, ?)""",
        sorted(album, key=lambda album: album[2]),
    )
    conn.commit()

    print("Got Albums")


# figured out afterwards that setlist matching would be much easier
# if I could just match a comma separated list as opposed to my first attempt
# which looked like the following:
# input two songs -> find all shows with those songs ->
# return id of song1 setlist entry -> check if id+1 equals song 2
def setlist_to_events():
    for e in cur.execute("""SELECT event_url FROM EVENTS""").fetchall():
        s = cur.execute(
            """SELECT song_name FROM SETLISTS WHERE event_url=? AND set_type NOT IN ('Soundcheck','Rehearsal') ORDER BY song_num ASC""",
            (e[0],),
        ).fetchall()

        if len(s) > 1:
            setlist = ", ".join(x[0] for x in s)

            cur.execute(
                """UPDATE EVENTS SET setlist=? WHERE event_url=?""", (setlist, e[0])
            )
            conn.commit()

    print("Updated Setlists in EVENTS table")


def jungleland_artwork():
    artwork_list = []
    event_date = ""

    r = requests.get("http://www.jungleland.it/html/list.htm", headers, timeout=10).text
    soup = bs4(r, "lxml")

    for l in soup.find_all("a", href=re.compile(r".*.htm")):
        if re.search(r"((\d{8})|(\d{4}-\d{2}-\d{2})) *.*htm", l.get("href")):
            if re.search(r"(\d{4}-\d{2}-\d{2})", l.text):
                event_date = re.search(r"(\d{4}-\d{2}-\d{2})", l.text).group(1)

            artwork_name = l.text.replace(f"({event_date})", "").strip()
            artwork_url = l.get("href").replace(" ", "%20").strip()
            artwork_list.append([artwork_url, artwork_name, event_date])

    cur.executemany(
        """INSERT OR IGNORE INTO ARTWORK VALUES (NULL, ?, ?, ?)""", artwork_list
    )
    conn.commit()
    print("Artwork Table Updated")


def get_bootlegs():
    """gets list of circulating bootlegs"""

    links = []
    events = cur.execute(
        """SELECT event_url FROM EVENTS ORDER BY event_id DESC"""
    ).fetchall()
    for i in range(1, 9):
        print(f"{main_url}stats:circulating-audio-list/p/{i}")
        r = requests.get(f"{main_url}stats:circulating-audio-list/p/{i}", headers)
        soup = bs4(r.text, "lxml")
        content = soup.find("div", {"class": "yui-content"})
        for li in content.find_all("li"):
            links.append(li.find("a").get("href"))

        for e in events:
            if e[0] in links:
                bootleg = "1"
            else:
                bootleg = "0"

            cur.execute(
                f"""UPDATE EVENTS SET bootleg='{bootleg}' WHERE event_url='{e[0]}'"""
            )
            conn.commit()

        time.sleep(0.5)

    print("got bootlegs")


def get_official_live():
    """gets list of officially released full shows"""

    links = []
    events = cur.execute(
        """SELECT event_url FROM EVENTS ORDER BY event_id DESC"""
    ).fetchall()

    r = requests.get(f"{main_url}system:page-tags/tag/retail#pages", headers)
    soup = bs4(r.text, "lxml")
    gigPages = []

    for g in soup.find_all("a", href=re.compile("/gig:.*")):
        gigPages.append(g.get("href"))

    for e in events:
        if e[0] in gigPages:
            official = "1"
        else:
            official = "0"

        cur.execute(
            f"""UPDATE EVENTS SET official='{official}' WHERE event_url='{e[0]}'"""
        )
        conn.commit()

    for i in range(1, 3):
        print(f"{main_url}stats:official-live-downloads-list/p/{i}")
        r = requests.get(f"{main_url}stats:official-live-downloads-list/p/{i}")
        soup = bs4(r.text, "lxml")
        content = soup.find("div", id="page-content")

        for li in content.find_all("li"):
            links.append(li.find("a").get("href"))

        for e in events:
            if e[0] in links:
                official = 1
            else:
                official = 0

            cur.execute(
                f"""UPDATE EVENTS SET official='{official}' WHERE event_url='{e[0]}' AND official='0'"""
            )
            conn.commit()

        time.sleep(0.5)

    print("got official live downloads")

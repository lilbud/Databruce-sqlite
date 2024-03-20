import re, os, sqlite3, requests, datetime, time, html2text, json
from titlecase import titlecase
from bs4 import BeautifulSoup as bs4

# from fuzzywuzzy import fuzz
import pandas as pd
from helper_stuff import albums, song_link_corrector, name_fix, show_name_split

# main_url = "http://brucebase.wikidot.com/"
conn = sqlite3.connect(os.path.dirname(__file__) + "/_database/database.sqlite")
cur = conn.cursor()
# event_types = "/(gig|nogig|interview|rehearsal|nobruce):"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
# }

openers = []
openerlist = []
openercount = []

setlists = cur.execute(
    """SELECT event_date, setlist FROM EVENTS WHERE tour='Darkness On The Edge Of Town Tour' AND setlist != ''"""
).fetchall()

for s in setlists:
    opener = s[1].split(",")[0]
    if opener == "Oh":
        opener = "Oh, Boy!"

    if opener != "" or opener != " ":
        openers.append(opener)

    if opener not in openerlist:
        openerlist.append(opener)


openers.sort()
# for o in openers:
#     print(o)
for i in openerlist:
    # print(f"{i}: {openers.count(i)}")
    openercount.append([openers.count(i), i])

openercount.sort()
print("---")
for c in openercount:
    print(f"{c[1]}: Opened {c[0]} Times")
    print("---")

# http://brucebase.wikidot.com/stats:circulating-audio-list/p/1
# event_url = "/gig:2017-02-14-entertainment-centre-brisbane-australia"

# bustout = cur.execute(f"""SELECT MIN(event_url) FROM EVENTS WHERE setlist LIKE '%Janey, Don''t You Lose Heart%' AND tour LIKE 'Summer ''17 Tour'""").fetchone()

# print(bustout[0] == event_url)
# invalid_sets = []

# shows = []
# count = 0

# l = cur.execute(
#     """SELECT event_url FROM SETLISTS WHERE event_url LIKE '%2005%' and song_url IN (SELECT song_url FROM ALBUMS WHERE album_name = 'Tunnel Of Love' ORDER BY song_num ASC)
#                 AND event_url LIKE '%gig%' AND set_type NOT LIKE '%Soundcheck%' AND set_type NOT LIKE '%Rehearsal%'"""
# ).fetchall()
# for u in l:
#     current = f"{l.count(u)} {u[0]}"
#     if current not in shows:
#         shows.append(current)

# shows.sort(reverse=True)
# print(shows)


# for i in cur.execute(f"""SELECT set_type FROM (SELECT DISTINCT set_type FROM SETLISTS WHERE set_type LIKE '%(Soundcheck|Rehearsal|Pre-)%')""").fetchall():
#     invalid_sets.append(i[0])

# print(invalid_sets)
# with open("circulating-audio-list.txt", "w", encoding="utf-8") as f:
#     for i in range(1,9):
#         r = requests.get(f"{main_url}stats:circulating-audio-list/p/{i}")
#         if r.ok:
#             soup = bs4(r.text, 'lxml')
#             links = soup.find('div', {'class': 'yui-content'}).find_all('a', href=re.compile(event_types))
#             for l in links:
#                 f.write(f"{l.text} - {l.get('href')}\n")


# setlist = []

# h = html2text.HTML2Text()
# h.ignore_links = False

# to handle list element
# one song link
# no links
# multiple links
# multiple songs, no links

# showpage = requests.get("http://brucebase.wikidot.com/gig:1980-10-31-memorial-sports-arena-los-angeles-ca", headers)
# soup = bs4(showpage.text, 'lxml')
# content = soup.find('div', {'id':'wiki-tab-0-1'}).find_all('li')

# for c in content:
#     setlist.append(c.find('a').get('href'))

# print(setlist)

# r = requests.get("http://brucebase.wikidot.com/gignote:1980-10-31-memorial-sports-arena-los-angeles-ca", headers)
# soup = bs4(r.text, 'lxml')
# gignote = soup.find('div', {'id':'page-content'})
# tags = ["relation", "song"]
# connections = ["snippet", "intro", "introduction"]
# types = []

# text = str(gignote).split(".")
# for t in text:
#     sentence = bs4(t, 'lxml')
#     types = []

#     if len(sentence.find_all('a')) > 1:
#         for i in sentence.find_all('a'):
#             c = str(sentence.find('body')).replace(str(i), "")

#         print(c)


# for s in sentence.find_all('a'):
#     if s.get('href') in setlist:
#         print(f"Main Song: {s.get('href')}")
#     else:
#         if "/relation:" in s.get('href'):
#             print(f"Relation: {s.get('href')}")

#         if "/song:" in s.get('href'):
#             print(f"Snippet: {s.get('href')}")


# showpage = requests.get("http://brucebase.wikidot.com/gig:1980-10-30-memorial-sports-arena-los-angeles-ca", headers)
# soup = bs4(showpage.text, 'lxml')
# content = soup.find('div', {'id':'wiki-tab-0-1'}).find_all('li')

# for i in content:
#     song_num = content.index(i)

#     if i.find('a'):
#         current = i.find_all('a')

#         if len(current) == 1:
#             setlist.append({'name': i.text, 'url': i.find('a').get('href'), 'song_num': song_num})

#         if len(current) > 1:
#             for i, c in enumerate(current):
#                 segue = "no"
#                 if i != len(current) - 1:
#                     segue = "yes"

#                 setlist.append({'name': c.text, 'url': c.get('href'), 'song_num': song_num, 'segue': segue})
#     else:
#         song = i.text.split(" - ")

#         if len(song) == 1:
#             setlist.append({'name': i.text, 'url': '', 'song_num': song_num})
#         elif len(song) > 1:
#             for i, s in enumerate(song):
#                 segue = "no"
#                 if i != len(song) - 1:
#                     segue = "yes"

#                 setlist.append({'name': s, 'url': '', 'song_num': song_num, 'segue': segue})

# print(json.dumps(setlist, indent=4))

# messing around with springsteenlyrics

# https://www.springsteenlyrics.com/bootlegs.php?filter_{filter}={date}&cmd=list&category=filter_{filter}
# filter_date, filter_title, filter_version, filter_publicinfo
# only one at a time

# filter = "date"
# boot = []
# listofboots = []
# # date = input("Enter Date: ")
# date = "1978-09-19"
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# r = requests.get(f"https://www.springsteenlyrics.com/bootlegs.php?filter_date={date}&cmd=list&category=filter_date", headers=headers)
# soup = bs4(r.text, 'lxml')
# for i in soup.find_all('div', {'class': 'blog-post'}):
#     temp = []
#     temp.append(i.find('a').find('img').get('title').strip())

#     id = re.findall(r"\d{4,}", re.sub("&.*", "", i.find('a').get('href')))[0]
#     temp.append(id)

#     for s in i.find('span').next_siblings:
#         if len(s.text) > 1 and s.name != "span":
#             temp.append(s.text.strip())

#     listofboots.append(temp)

# for b in listofboots:
#     # title, id, source/label, date, location, format, duration, artwork, info file

#     artwork = info_file = False

#     if len(b) > 8:
#         if b[7]:
#             artwork = True
#         if b[8]:
#             info_file = True

#     print(f"\nTitle: {b[0]}\nItem ID: {b[1]}\nSource/Label: {b[2]}\nDate: {b[3]}\nLocation: {b[4]}\nFormat: {b[5]}\nDuration: {b[6]}\nArtwork: {artwork}\nInfo File: {info_file}")

import re, os, sqlite3, requests, datetime, time
from titlecase import titlecase
from bs4 import BeautifulSoup as bs4
import pandas as pd
from helper_stuff import albums, song_link_corrector, name_fix, show_name_split

main_url = "http://brucebase.wikidot.com/"
conn = sqlite3.connect(os.path.dirname(__file__) + "/_database/database.sqlite")
cur = conn.cursor()
snippets = []
s = "Soundcheck"
f = open("tags.txt", "w")

r = requests.get(f"{main_url}system:page-tags")
soup = bs4(r.text, 'lxml')

for t in soup.find_all('a', {'class': 'tag'}):
    if "snip" in t.get('href'):
        song_name = ""
        # tag = re.findall("tag/.*", t.get('href'))[0].strip("tag/")
        tag = t.get('href').replace("system:page-tags/tag/", "")
        r = requests.get(f"{main_url}{t.get('href').strip("/")}")
        soup = bs4(r.text, 'lxml')

        if soup.find('a', href=re.compile("/song:")):
            song_name = soup.find('a', href=re.compile("/song:")).text

        print(f"{tag}, {song_name}")
        snippets.append([tag, song_name])
    
for s in snippets:
    f.write(f"{s[0]}, {s[1]}")

# def date_checker(date):
# 	if date is not None:
# 		try:
# 			return datetime.date.fromisoformat(date)
# 		except:
# 			return False
# 	else:
# 		return False

# date = None

# if date is None:
# 	date = cur.execute("""SELECT event_date FROM EVENTS WHERE setlist != '' ORDER BY event_id DESC LIMIT 1""").fetchone()[0]

# print(date_checker(date))



# # album = ":therising:"

# # for a in cur.execute(f"""SELECT DISTINCT(album_name) FROM ALBUMS""").fetchall():
# #     if a[0].lower() == "".join(album.strip(":").lower()):
# #         album_to_find = a[0]
# #     else:
# #         album_to_find = "".join(album)

# def get_relation(name):
#     """gets info on bands/people that have played with bruce"""

#     # check name against database
#     # if found, get num plays
#     # search on_stage for first and last performance with bruce
#     # have type in () next to name

#     toFind = cur.execute(f"""SELECT relation_name, relation_url, appearances, relation_type FROM RELATIONS WHERE LOWER(relation_name) LIKE '%{name.lower().replace("'", "''")}%'""").fetchone()

#     if toFind:
#         name = toFind[0]
#         url = toFind[1]
#         appearances = toFind[2]
#         relation_type = toFind[3]

#         if int(appearances) > 0:
#             first_last = cur.execute(f"""SELECT MIN(event_url), MAX(event_url) FROM ON_STAGE WHERE relation_url LIKE '{url}' AND event_url LIKE '/gig:%'""").fetchone()

#             first_date = cur.execute(f"""SELECT event_date FROM EVENTS WHERE event_url LIKE '{first_last[0]}'""").fetchall()[0]
#             last_date = cur.execute(f"""SELECT event_date FROM EVENTS WHERE event_url LIKE '{first_last[1]}'""").fetchall()[0]

#             print(f"Name: {name} ({relation_type.title()})")
#             print(f"Appearances: {appearances}")
#             print(f"First Performance: [{first_date[0]}]({main_url}{first_last[0].strip("/")})")
#             print(f"Last Performance: [{last_date[0]}]({main_url}{first_last[1].strip("/")})")

# # name = input("enter person to find: ")
# # get_relation(name)

# t = "<:btr:1155865010178904194>"
# print(re.findall(":.*:", t)[0])
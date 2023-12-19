"""
Snippet Tags - script I wrote to get the various tags from Brucebase. This one finds tags linked to "song snippets"
basically any show where he played a snippet of one song in another. Was trying to piece together the various snippets
that aren't in the setlists, but are mentioned in the gignote. Still a WIP
"""

import re, os, sqlite3, requests, sys
from bs4 import BeautifulSoup as bs4

main_url = "http://brucebase.wikidot.com/"

# conn = sqlite3.connect(f"{os.path.abspath('.')}\\_database\\database.sqlite")
# cur = conn.cursor()

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
    f.write(f"{s[0]}, {s[1]}\n")
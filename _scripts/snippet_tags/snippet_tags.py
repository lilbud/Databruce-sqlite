"""
Snippet Tags - script I wrote to get the various tags from Brucebase. This one finds tags linked to "song snippets"
basically any show where he played a snippet of one song in another. Was trying to piece together the various snippets
that aren't in the setlists, but are mentioned in the gignote. Still a WIP
"""

import re, os, sqlite3, requests, sys
import httpx
from bs4 import BeautifulSoup as bs4

main_url = "http://brucebase.wikidot.com/"

snippets = []
# s = "Soundcheck"
f = open("tags.txt", "w")

# r = requests.get(f"{main_url}system:page-tags")
# soup = bs4(r.text, 'lxml')

# for t in soup.find_all('a', {'class': 'tag'}):
#     if "snip" in t.get('href'):
#         song_name = ""
#         # tag = re.findall("tag/.*", t.get('href'))[0].strip("tag/")
#         tag = t.get('href').replace("system:page-tags/tag/", "")
#         r = requests.get(f"{main_url}{t.get('href').strip("/")}")
#         soup = bs4(r.text, 'lxml')

#         if soup.find('a', href=re.compile("/song:")):
#             song_name = soup.find('a', href=re.compile("/song:")).text

#         print(f"{tag}, {song_name}")
#         snippets.append([tag, song_name])

# for s in snippets:
#     f.write(f"{s[0]}, {s[1]}\n")


def snippet_tags():
    """
    Gets a list of all the snippet tags from the site

    Possibly can be used to match up to songs in setlist
    """

    with httpx.Client() as client:
        try:
            r = client.get(
                "http://brucebase.wikidot.com/system:page-tags",
            )
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}.")

        soup = bs4(r.text, "lxml")
        for tag in soup.find_all("a", {"class": "tag"}, href=re.compile("snip$")):
            f.write(f"{tag.text}\n")
            # try:
            #     r = client.get(f"{main_url}{tag.get('href').strip(" / ")}")
            # except httpx.RequestError as exc:
            #     print(f"An error occurred while requesting {exc.request.url!r}.")

            # soup = bs4(r.text, "lxml")

            # if soup.find("a", href=re.compile("/song:")):
            #     song_name = soup.find("a", href=re.compile("/song:")).text

            # print(f"{tag}, {song_name}")


snippet_tags()

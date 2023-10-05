import re, os, sqlite3, requests, datetime
from titlecase import titlecase
from bs4 import BeautifulSoup as bs4
import pandas as pd
from helper_stuff import albums, song_link_corrector, name_fix, show_name_split

main_url = "http://brucebase.wikidot.com/"
conn = sqlite3.connect(os.path.dirname(__file__) + "/_database/database.sqlite")
cur = conn.cursor()
temp = []

# #Read CSV file
# data = pd.read_csv(os.path.dirname(__file__) + "/_csv/SONGS.csv")

# # #Export as HTML file
# # df.to_html('songs.html', header=False, index=False, index_names=False)
# for index, row in data.iterrows():
#     r = row[1].strip("/")
#     #print(f"<a href='{main_url}{r}'>{row[2]}</a>")
#     temp.append([row[0], f'<a href="{main_url}{r}">{row[2]}</a>', row[3], row[4], row[5]])

# df = pd.DataFrame(temp, columns=['song_id', 'song', 'first_played', 'last_played', 'num_performances'])
# df.to_html('songs-new.html', index=False, index_names=False, render_links=True, escape=False)

def get_relations():
    relations = []
    #id, url, name, appearances, type

    for t in ['person', 'band']:
        url = f"system:page-tags/tag/{t}#pages"
        r = requests.get(f"{main_url}{url}")
        soup = (r.text, 'lxml')
        for i in soup.find_all('a', href=re.compile("/relation:.*")):
            if t == "person":
                curr = i.text.split(", ")
                name = f"{curr[1]} {curr[0]}"

                if i.get('href') == "/relation:frank-pagano-2":
                    name = f"{re.sub(' *(Timepiece) *', '', curr[1])} {curr[0]} (Timepiece)"

                relations.append([i.get('href'), name, 0, "person"])

            if t == "band":
                bands = []
                if not re.search("-([1-2])$", i.get('href')):
                    band_name = b.text.strip()
                    if ", The" in b.text or " (The)" in b.text:
                        band_name = "The " + re.sub("(, | )(\(The\)|The)", "", b.text.strip())
                    
                    bands.append([i.get('href'), band_name, 0, "band"])

		            # for s in sorted(bands, key=lambda band: band[1].replace("The ", "")):



get_relations()
"""
Project Name: Databruce
Author Name: Lilbud
Name: Jungleland Artwork
File Purpose: Gets artwork list from Jungleland
"""

import re, requests, os, sqlite3
from bs4 import BeautifulSoup
from helper_stuff import *

main_url = "http://www.jungleland.it/html/"
date = ""
start_time = datetime.datetime.now()

r = requests.get(main_url + "list.htm").text
soup = BeautifulSoup(r, "lxml")

conn = sqlite3.connect(os.path.dirname(__file__) + "/_database/artworkdatabase.sqlite")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS ARTWORK (
	artwork_id INTEGER primary key autoincrement,
	artwork_url TEXT NOT NULL,
	artwork_name TEXT NOT NULL,
	date TEXT NOT NULL,
	UNIQUE(artwork_url));"""
)

for l in soup.find_all('a', href=re.compile(".*.htm")):
	if re.search("((\d{8})|(\d{4}-\d{2}-\d{2})) *.*htm", l.get('href')):
		if re.search("(\d{4}-\d{2}-\d{2})", l.text):
			date = re.search("(\d{4}-\d{2}-\d{2})", l.text).group(1)

		artwork_name = l.text.replace("(" + date + ")", "").strip()
		artwork_url = main_url + l.get('href').replace(" ", "%20")
		cur.execute("""INSERT or IGNORE INTO ARTWORK (artwork_url, artwork_name, date) VALUES (?, ?, ?)""", (artwork_url, artwork_name, date))
		conn.commit()

run_time(start_time)
print("Artwork Table Updated")
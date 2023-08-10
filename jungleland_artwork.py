"""
Project Name: Databruce
Author Name: Lilbud
Name: Jungleland Artwork
File Purpose: Gets artwork list from Jungleland
"""

import os
import sqlite3
import re
import datetime
import requests
from bs4 import BeautifulSoup
from helper_stuff import run_time

MAIN_URL = "http://www.jungleland.it/html/"
DATE = ""
start_time = datetime.datetime.now()

r = requests.get(MAIN_URL + "list.htm", timeout=5).text
soup = BeautifulSoup(r, "lxml")

conn = sqlite3.connect(os.path.dirname(__file__) + "/_database/database.sqlite")
cur = conn.cursor()

for l in soup.find_all('a', href=re.compile(".*.htm")):
    if re.search("((\d{8})|(\d{4}-\d{2}-\d{2})) *.*htm", l.get('href')):
        if re.search("(\d{4}-\d{2}-\d{2})", l.text):
            DATE = re.search(r"(\d{4}-\d{2}-\d{2})", l.text).group(1)

        artwork_name = l.text.replace("(" + DATE + ")", "").strip()
        artwork_url = MAIN_URL + l.get('href').replace(" ", "%20")
        cur.execute(
            """INSERT or IGNORE INTO ARTWORK (artwork_url, artwork_name, date) VALUES (?, ?, ?)""",
            (artwork_url, artwork_name, DATE))
        conn.commit()

run_time(start_time)
print("Artwork Table Updated")

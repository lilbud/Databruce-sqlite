# databruce
A SQLite database of Bruce Springsteens career

## To Do:
- ~~Add full writeup~~
- ~~upload the python scripts to build/update the database~~
- add some examples of what can be done with the data
- ~~at some point, I'll work on a python script that can manipulate the database for those who aren't familiar with SQL~~

---
To easily view the data, you can use the CSV files in the `_csv` folder.

You can also use the [DB Browser for SQLite](https://sqlitebrowser.org/), this adds the ability to manipulate the data if you're familiar with SQLite. This app is available for Windows/Mac/Linux
---
An explaination:

Python libraries needed: BeautifulSoup4, Requests, lxml parser, ZoneInfo, titlecase, time, datetime

Provided in this repo are all the python files you need to create a copy of the database. 

- `setup.py` - creates the database file, and all the tables needed for the data. As well as creating the directories for the databases and the csv data files. 

- `data_collection.py` - all the functions to get the data from Brucebase.

- `update.py` - two functions within:
  - basic_update: populates the bands, persons, venues, songs, events, and tours tables. This stuff really doesn't change all that much, so it's fairly easy to grab.
  - detailed_update: gets show info for everything listed in the events table that doesn't already have info in the setlist table. For the most part, you can just run this for the current year to get up to date setlists (Brucebase usually has an update a day or so after a show happened.) Odds are, older shows aren't suddenly going to have a setlist updated unless a new tape circulates or something.
 
  Quick note about the functions in the update.py script, there are various time.sleep calls. These are here to protect the site from being overloaded (Not so much with the basic update, more for the setlists which might need to scrape upwards of 3000 pages. There are also a few checks to avoid scraping a page unless necessary. Which makes updates fairly quick.

- `csv_export.py` - exports all the data in the `database.sqlite` file out to `.csv` files. Just makes it easier to view the data without any SQL knowledge. These are also updated with the database file.

- `helper_stuff.py` - Various functions to help with data collection. Fixes some edge cases with incorrect formatting on Brucebase. As well as lists of state/provience abbreviations. And a list of Albums/Release Year/Type, this was the best solution I could come up with to the problem of "there isn't a single page with all this information".

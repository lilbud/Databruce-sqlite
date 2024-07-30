# UPDATE
As of 2024-07-30, this is now an archived repo. I've rebuilt the database basically from scratch using PostgreSQL, which definitely helps since Heroku uses it and for the past year I've used a series of workarounds to get the SQLite version -> Heroku. Plus being PGSQL from the getgo allows for much more in terms of data and features.

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

- `update.py` - multiple functions within:
  - basic_update: populates the bands, persons, venues, songs, events, and tours tables. This stuff really doesn't change all that much, so it's fairly easy to grab.
  - detailed_update: gets show info for everything listed in the events table that doesn't already have info in the setlist table. For the most part, you can just run this for the current year to get up to date setlists (Brucebase usually has an update a day or so after a show happened.) Odds are, older shows aren't suddenly going to have a setlist updated unless a new tape circulates or something.
  - setlistToEvents: This is a recent addition. At some point, I want to be able to do advanced setlist matching. However, this isn't super easy to do in standard SQLite (least not that I've found anyway.) It can be done, but is quite complicated and only works for two songs at a time. Using this function, it grabs the setlists from that table and converts them to a comma separated list, then puts that into the EVENTS table. This enables (hopefully) better setlist matching, plus the ability to find setlists that match two or more songs (like finding shows that had full album performances.)
  - update_counts: this updates the various counts in the tables. Getting the number of performances for songs, number of times at a venues, and number of performances or appearances per musician/band. Also populates the `first_played` & `last_played` fields in the SONGS table
 
  Quick note about the functions in the update.py script, there are various time.sleep calls. These are here to protect the site from being overloaded (Not so much with the basic update, more for the setlists which might need to scrape upwards of 3000 pages). There are also a few checks to avoid scraping a page unless necessary. Which makes updates fairly quick.

- `csv_export.py` - exports all the data in the `database.sqlite` file out to `.csv` files. Just makes it easier to view the data without any SQL knowledge. These are also updated with the database file.

- `helper_stuff.py` - Various functions to help with data collection. Fixes some edge cases with incorrect formatting on Brucebase. As well as lists of state/provience abbreviations. And a list of Albums/Release Year/Type, this was the best solution I could come up with to the problem of "there isn't a single page with all this information, and this is preferable to looking at several different pages per album."

- `databruce.py` - a script that replicates the functions of the discord bot to an extent. Currenly can get Setlists by date, songs by name, and list of events on this day

### Instructions
First, run `pip -r requirements.txt` in your terminal. This should get all the modules needed to run the various scripts provided. 

To update the database. Uncomment the following lines in `update.py`

```
basic_update()
full_update(current_year, current_year)
setlistToEvents()
update_counts()
```

See above for the descriptions of what each function does. These scripts will update the provided database file. `basic_update()` will get the basic amount of info for a new database. `full_update(start, end)` will get setlists and show info for events between the two provided years. In most cases, just needs to be run for the current year. But the range can be specified as needed.

The database on github will be updated regularly, usually I'll update and push a change after a show happens (which as of writing, isn't happening until August 9th). I'm working on a way to have scheduled updates, which will run at certain intervals (every day or two, just checking for latest events and setlists). This is TBD as of now. 

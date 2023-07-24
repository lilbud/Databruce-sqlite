## Intro:

This repository is for the "Databruce" project. The name is from combining "Database" and "Bruce" (clever I know). This project originally started as an extension of my [Brucebase Scraper](https://github.com/lilbud/brucebase-scraper) project, as well as my ongoing BruceBot project (a discord bot that gets information from Brucebase, a website containing information about Bruce Springsteens performing/recording career). 

Below I'll explain those two projects as they provide some background to this project (and most of my ramblings/WIP stuff is buried in a discord server).

But first, some credits:
* Superzann - original concept
* [Brucebase](http://brucebase.wikidot.com/) - Source of the data
* a million and one StackOverflow threads

---
### Brucebase Scraper (March 2023):

The original concept comes from Superzann, who created a scraper that worked in Google Sheets. That got me started in dabbling with web scraping. 

Sheets is very limiting, the regex just to fix the capitalization issues (As Brucebase has all song titles in all caps by default) was a nightmare, see below:

`=IFERROR(TRANSPOSE(ARRAYFORMULA(REGEXREPLACE(REGEXREPLACE(REGEXREPLACE(REGEXREPLACE(SPLIT(PROPER(JOIN(" / ",IMPORTXML("http://brucebase.wikidot.com"&B1, "//div[@id='wiki-tab-0-1']//descendant::ol")))," / ", false), "'Ll", "'ll"), "'S", "'s"), "Nd", "nd"), "Th[ ]", "th "))))`

Eventually (read: I was bored at work), I started looking into using Python to do something similar. Using `BeautifulSoup` made it real easy to scrape the site. The code to get the setlist was only around 20 lines.

This expanded to 124 lines as I added the option to export these setlists to text files. As well as some fixes to get around weird headers on the gig pages and what not. The text file export was really just because I had nothing to actually *do* with the data once I got it. Other than displaying in the terminal window that is. 

After some cleanup, I published the code and figured that was it. I also published a version on [Repl.it](https://replit.com/@lilbud/Brucebase-Scraper?v=1). Which is a ton more accessible to like 90% of people, as the Github version requires having Python installed, as well as all the modules I used. 

That was a good place to end it, as it had all the features I could think of and did what it set out to do. I did some more clean up and posted the final update to date at 1am on 3/27/23. Figured if I had any other good ideas, I'd go back and add them.

Little did I know that would only be about 12hrs later.

---
### Brucebot (March 2023 - Ongoing)

Once or twice I've dabbled with creating a discord bot, never getting very far due to not having the skills necessary.

Not even sure how I ended up down this particular rabbit hole, most likely scenario is that I was looking at repl.it help docs and saw the page on how to code a discord bot in Python and host it on repl.it.

The code was all written, all I had to do was set up the bot and implement the code correctly, this took about an hour, and I had a basic bot up and running. Pretty much just responding to a command with a date, and returning the setlist for that date. 

After a couple hours, I got the scraper "ported" over to a Discord bot and it went live. Currently it can be accessed by DM or in the r/brucespringsteen Discord server. 

Making this project into a discord bot means its a ton more accessible to people than even the Repl.it version. Just type in the commands and it returns the info. 

At first, all the bot was able to do was get setlists for a date. Though overtime I added more features (usually preceded by: "oh, that can't be done, too difficult" and "oh that wasn't so hard"):

---
- "Bootleg" (added 3/28/23) - returns a list of bootlegs from [SpringsteenLyrics](https://www.springsteenlyrics.com/index.php) Just returns their search URL with the date appended in. Doesn't do anything fancy.
#
- "On This Day" (added 3/29/23) - Will return a list of all the events that happened on the current day, or if provided with a date in `MM-DD` format, returns the events that happened on that day.
#
- "Get Cover" (added 3/29/23) - takes date in `YYYY-MM-DD` format, and searches my Github repo of covers I've made and returns them if found. This was mainly because I was too lazy to upload manually to Discord. So, I'd push an update to the repo, and use the command.
#
- "Jungleland" (added around 4/8/23) - takes date in `YYYY-MM-DD` format, returns URL to Jungleland Torrents with that date. Like the `Bootleg` command above, just returns a URL, doesn't scrape the site or anything.
#
- "Song Finder" (added 6/6/23) - by far the most difficult feature to implement. Takes the user inputted song name, and attempts to find that song on Brucebase, and returns how many times its been played. Difficulty came down to actually returning the right result for an input, and dealing with all the possible shorthand titles and weird typos people might input. Still not "just exactly perfect", but good enough
---

I worked on the bot on and off for the next few months, fixing different edge cases with weird formatting. In June, I worked on getting the bot to display info in Discord embeds as compared to code blocks. The embeds look nicer, see here: [Imgur](https://imgur.com/NZKW0zr)

At this point, I was pretty much just adding any dumb idea I could think of to the bot. When starting, I had a mental list of features I wanted to try and get around to adding. Stuff like Song Finder and what not. 

From creation until now, the bot relies on Brucebase to get the event and setlist data from. This isn't a major issue, as it works no problem. And the bot is only ever getting one or two setlists per user command. The `on this day` command probably got the most data from BB, and that initially just got the links from a javascript element on the front page. Nothing too strenuous.

Most ideas I thought of could be done just by scraping different pages. The `song finder` was when it became really difficult. As the site has nearly 1600 songs, so scraping through those took a while. I eventually decided to grab the list of song urls and put that in a text file. Then, the song finder would just search that list rather than the website. This got to be quite ridiculous, and I started looking for a better solution.

---

### Adventures in SQLite and Web Scraping

Scraping Brucebase served me well enough for all this time. But really it would make it easier if I *had* all of the data in an easily accessible format. This is kind of what the text file setlists from the original Scraper project were trying to accomplish. Although much less sophisticated, and dealing with their own formatting issues and what not. 

Only issue being that there is no public repository of the Brucebase data, except for the site itself (which is almost entirely HTML). They might have some kind of private SQL database, but that doesn't do me any good.

Actually, there is one: https://github.com/obrienjoey/spRingsteen

That project is based on R, and can analyze the database in different ways.

Originally, I was just going to use his project and incorporate it into the bot. It provides an SQLite database with the Brucebase data, and it automatically updates every night, so the setlists will be up to date. Plus when I run the bot I can easily run `git clone` to update my copy. 

Only issue with that project is that it doesn't have all the data I need. And it would actually be a step backwards as compared to scraping. That project has: Songs, Concerts, Tours, and Setlists. This is perfectly suitable for the intended goals of the project. Just the essential data for different forms of analysis. 

In addition, that project only has data for actual gigs, and of those, only the main setlists. Which again, is perfectly fine. But, my scraper/bot gets rehearsals, and even gets the soundchecks for a show if there was a known one. 

So while I could have just used that db, it wouldn't have been a perfect replacement. It wouldn't have all the data I currently have access to. 

At first, I tried modifying the existing code to attempt to implement some features like getting rehearsals and soundchecks, but my knowledge of R is basically non-existent. I probably could've chipped away at it and hacked together something vaguely functional, or I could just not do that (very difficult choice).

Seeing as the original scraper was written in PYTHON, and by extension, the Discord bot was also written in PYTHON. I decided to go with Java for this project, as that was the most logical option.

After that fell through, I begrudgingly went back to Python. It was better to just stick with what I knew and go from there. As I had the basis of the code already written, I just had to relearn SQL (or Lite, in this case) and figure out how to get the two to connect. 

Some stuff came easy enough (like Songs and Events). Venues were slightly trickier as there are a few venues where the name of them is incorrect. Missing commas or having other typos. Though the fixes were simple. I saved Setlists for the end as I knew that would be the most difficult part (plus requiring scraping a few thousand pages, which was daunting).

As the project went it kinda snowballed. Leading to me getting more data than I thought I would. Like a list of all the On Stage members, all of the tours, or even the albums and their songs.

Now that the data is in a proper database, it can be manipulated much easier now. Plus it makes it possible to attempt some features I've been unable to do, like setlist searching (finding shows where he did a certain sequence of songs). Or even some crazy stuff like finding all the times he played Thundercrack in Philly, or Wrecking Ball in a city that boos the Giants line (Philly and Boston, among others). Or even find how many times he played a song with Clarence vs Jake. I'm just spitballing, but all of those are technically possible with the right SQL Queries.

At some point, I'm going to write a python frontend to manipulate this data. As there really isn't a place to host an SQLite db where it doesn't cost me an arm and a leg. It'll allow for these more advanced features to be accessible to those who aren't super knowledgeable (likely hosted on Repl, time is a circle I guess).

Might even write up a fuller guide on the finer points of this db at some point, TBD

---
# Fin

That about sums it up in far too many words. This project is almost always a work in progress, so things might change as time goes on. 

Lilbud (July 2023)

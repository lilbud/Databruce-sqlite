"""
Project Name: Databruce
Author Name: Lilbud
Name: Helper Stuff
File Purpose: Various functions and items to help in data collection
"""

import re
import datetime

states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

provinces = ['AB', 'BC', 'NB', 'ON', 'QC']

albums = {"Greetings From Asbury Park, N.J.": [1973, "studio"],
"The Wild, The Innocent & The E Street Shuffle": [1973, "studio"],
"Born To Run": [1975, "studio"],
"Darkness On The Edge Of Town": [1978, "studio"],
"The River": [1980, "studio"],
"Nebraska": [1982, "studio"],
"Born In The U.S.A.": [1984, "studio"],
"Tunnel Of Love": [1988, "studio"],
"Human Touch": [1992, "studio"],
"Lucky Town": [1992, "studio"],
"The Ghost Of Tom Joad": [1995, "studio"],
"The Rising": [2002, "studio"],
"Devils & Dust": [2005, "studio"],
"We Shall Overcome": [2006, "studio"],
"Magic": [2007, "studio"],
"Working On A Dream": [2009, "studio"],
"Wrecking Ball": [2012, "studio"],
"High Hopes": [2014, "studio"],
"American Beauty EP": [2014, "studio"],
"Western Stars": [2019, "studio"],
"Letter To You": [2020, "studio"],
"Only The Strong Survive": [2022, "studio"],
"Greatest Hits": [1995, "compilation"],
"Blood Brothers EP": [1996, "compilation"],
"Tracks": [1998, "compilation"],
"18 Tracks": [1999, "compilation"],
"The Essential": [2003, "compilation"],
"Greatest Hits '09": [2009, "compilation"],
"The Promise": [2010, "studio"],
"Collection: 1973-2012": [2012, "compilation"],
"The Ties That Bind": [2015, "compilation"],
"Chapter And Verse": [2016, "compilation"],
"Spare Parts": [2018, "compilation"],
"Live 1975–85": [1986, "compilation"],
"Chimes Of Freedom EP": [1988, "compilation"],
"In Concert/MTV Plugged": [1992, "live"],
"Live In New York City": [2001, "live"],
"Hammersmith Odeon, London '75": [2006, "live"],
"Live In Dublin": [2007, "live"],
"Magic Tour Highlights": [2008, "live"],
"Springsteen On Broadway": [2018, "live"],
"Western Stars (Songs From The Film)": [2019, "live"],
"The Legendary 1979 No Nukes Concerts": [2021, "live"]}

def venue_name_corrector(venue_name):
    # fixes a few venue names that are incorrect
    # usually missing commas or spaces
    match(venue_name):
        case "Alvin Theatre New York City Ny":
            return "Alvin Theatre, New York City, NY"
        case "Gwinnett Civic Center Arena Duluth Ga":
            return "Gwinnett Civic Center Arena, Duluth, GA"
        case "John F. Kennedy Memorial Center For The Performing Arts,Washington, DC":
            return "John F. Kennedy Memorial Center For The Performing Arts, Washington, DC"
        case _:
            return venue_name

def song_link_corrector(url):
    #fixes a single link that doesn't match up to songs table
    match(url):
        case "/song:rainy-day-women#12%20&%2035":
            return "/song:rainy-day-women"
        case "/song:rainy-day-women#12 & 35":
            return "/song:rainy-day-women"
        case _:
            return url

def name_fix(name):
    # corrects the name of venues
    # some venues have text like "The" and "New" in the middle of the name
    # they should be at the beginning
    # ex. "The Upstage, Asbury Park, NJ" vs "Upstage (The), Asbury Park, NJ"

    for n in ['The', 'Le', 'De', 'New']:
        if "(" + n + ")" in name:
            try:
                name = n + " " + re.sub(" *\(" + n + "\) *", "", name)
            except:
                name = n + " " + re.sub(" *\(" + n + "\),", ", ", name)

    return name

def run_time(start_time):
    end_time = datetime.datetime.now()
    print("Start Time: " + str(start_time))
    print("End Time: " + str(end_time))
    print("Runtime: " + str(end_time - start_time).split(".", maxsplit=1)[0])

def show_name_split(show_name, url):
    venues = []
    city = state = country = show = ""
    vn = show_name.split(", ")
    name = vn[0]

    if re.match("[A-Z]{2} \(.*\)", vn[-1]):
        state = vn[-1][0:2]
        show = vn[-1][3:].strip("()")
    elif len(vn[-1]) == 2:
        state = vn[-1]
    else:
        state = ""

    if len(vn) == 4:
        name = ", ".join(vn[0:1])

    if len(vn) >= 3:
        city = vn[-2].strip()

    if state in states:
        country = "USA"
    elif state in provinces:
        country = "Canada"
    else:
        country = vn[-1].strip()

    venues.append([name, city, state, country, show, url])
    return venues
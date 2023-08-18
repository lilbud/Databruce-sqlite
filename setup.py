"""
Project Name: Databruce
Author Name: Lilbud
Name: Setup
File Purpose: Sets up directories and the main database
"""

import os
import sqlite3

os.makedirs("_csv", exist_ok=True)
os.makedirs("_database", exist_ok=True)

conn = sqlite3.connect(os.path.dirname(__file__) + "/_database/database.sqlite")
cur = conn.cursor()

#events table
cur.execute("""CREATE TABLE IF NOT EXISTS EVENTS (
	event_id INTEGER primary key autoincrement,
	event_date TEXT NOT NULL,
	event_url TEXT NOT NULL,
	location_url TEXT NOT NULL,
	event_venue TEXT NOT NULL,
	event_city TEXT NOT NULL,
	event_state TEXT NOT NULL,
	event_country TEXT NOT NULL,
	show TEXT NOT NULL,
	tour TEXT NOT NULL,
	setlist TEXT NOT NULL,
	UNIQUE(event_url));""")

#venues
#num_performances - count events table for venue
#maybe leave name as is with (The)
cur.execute("""CREATE TABLE IF NOT EXISTS VENUES (
	venue_id INTEGER primary key autoincrement,
	venue_url TEXT NOT NULL,
	venue_name TEXT NOT NULL,
	num_performances INT NOT NULL,
	UNIQUE(venue_url));""")

#songs
#num_plays - count setlists db
cur.execute("""CREATE TABLE IF NOT EXISTS SONGS (
	song_id INTEGER primary key autoincrement,
	song_url TEXT NOT NULL,
	song_name TEXT NOT NULL,
	first_played TEXT NOT NULL,
	last_played TEXT NOT NULL,
	num_plays INT NOT NULL,
	UNIQUE(song_url));""")

#Setlists
cur.execute("""CREATE TABLE IF NOT EXISTS SETLISTS (
	setlist_song_id INTEGER primary key autoincrement,
	event_date TEXT NOT NULL,
	event_url TEXT NOT NULL,
	song_url TEXT NOT NULL,
	song_name TEXT NOT NULL,
	set_type TEXT NOT NULL,
	song_num_in_set INT NOT NULL,
	song_num INT NOT NULL,
	UNIQUE(date, event_url, song_url, song_name, set_type, song_num_in_set, song_num));""")

#on_stage
cur.execute("""CREATE TABLE IF NOT EXISTS ON_STAGE (
	id INTEGER primary key autoincrement,
	event_url TEXT NOT NULL,
	relation_url TEXT NOT NULL,
	relation_name TEXT NOT NULL,
	relation_type TEXT NOT NULL,
	UNIQUE(event_url, relation_name));""")

#bands
#performances - count events table
cur.execute("""CREATE TABLE IF NOT EXISTS BANDS (
	band_id INTEGER primary key autoincrement,
	band_url TEXT NOT NULL,
	band_name TEXT NOT NULL,
	num_performances INT NOT NULL,
	UNIQUE(band_url));""")

#persons
cur.execute("""CREATE TABLE IF NOT EXISTS PERSONS (
	person_id INTEGER primary key autoincrement,
	person_url TEXT NOT NULL,
	person_name TEXT NOT NULL,
	num_appearances TEXT NOT NULL,
	UNIQUE(person_url));""")

#tours
cur.execute("""CREATE TABLE IF NOT EXISTS TOURS (
	tour_id INTEGER primary key autoincrement,
	tour_url TEXT NOT NULL,
	tour_name TEXT NOT NULL,
	num_shows INT NOT NULL,
	unique(tour_url));""")

#albums
cur.execute("""CREATE TABLE IF NOT EXISTS ALBUMS (
	album_name TEXT NOT NULL,
	album_type TEXT NOT NULL,
	album_year INT NOT NULL,
	song_url TEXT NOT NULL,
	song_name TEXT NOT NULL,
	song_num INT NOT NULL,
	UNIQUE(album_name, song_url));""")

#artwork table:
cur.execute("""CREATE TABLE IF NOT EXISTS ARTWORK (
	artwork_id INTEGER primary key autoincrement,
	artwork_url TEXT NOT NULL,
	artwork_name TEXT NOT NULL,
	date TEXT NOT NULL,
	UNIQUE(artwork_url));"""
)

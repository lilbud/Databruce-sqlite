import re, os, sqlite3
from unidecode import unidecode

db_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..\\_database\\database.sqlite")
)

conn = sqlite3.connect(db_path)
cur = conn.cursor()
# G:\Music\Bootlegs\Bruce_Springsteen\1984\_untagged
artist = "Bruce Springsteen"
year = "1972"


def loop(artist, year):
    # path = f"G:\Media\Music\Bootlegs\{artist}\{year}\_untagged"
    # path = f"G:\Media\Music\Bootlegs\{artist}\{year}"
    path = f"G:\\Media\\Music\\Bootlegs\\{artist}\\_tosort"

    # loop dirs, in each get the date and pass to mp3tag gen

    for i in os.listdir(path):
        date = re.findall(r"\d{4}-\d{2}-\d{2}", i)[0]

        event_get = cur.execute(
            f"""SELECT event_url, location_url, show FROM EVENTS WHERE event_date='{date}'"""
        ).fetchall()

        if event_get:
            for e in event_get:
                output_path = f"{path}\{i}\mp3tag.txt"
                with open(output_path, "w") as my_file:
                    try:
                        band = cur.execute(
                            f"""SELECT relation_name FROM RELATIONS WHERE relation_url IN (SELECT relation_url FROM ON_STAGE WHERE event_url='{e[0]}' AND relation_type LIKE 'Band')"""
                        ).fetchone()[0]
                        artist = f"Bruce Springsteen & {band}"
                    except:
                        artist = f"Bruce Springsteen"

                    album = ", ".join(
                        filter(
                            None,
                            cur.execute(
                                f"""SELECT venue_name, venue_city, venue_state, venue_country FROM VENUES WHERE venue_url='{e[1]}';"""
                            ).fetchone(),
                        )
                    )
                    setlist = cur.execute(
                        f"""SELECT song_name, segue FROM SETLISTS WHERE event_url='{e[0]}' AND set_type='Show' ORDER BY song_num ASC"""
                    ).fetchall()

                    for song in setlist:
                        segue = genre = comment = ""
                        song_name = re.sub(
                            r" *(\(The Animals|Them)\).*", "", song[0]
                        ).replace("''", "'")

                        if song[1] == 1:
                            segue = " >"

                        line = f"{artist}  -  {date} - {album}  -  {song_name}{segue}  -    -  {date[0:4]}  -  {genre}  -  {comment}"
                        print(line)
                        my_file.write(unidecode(f"{line}\n"))

                print(f"file saved to {output_path}")


loop(artist, year)

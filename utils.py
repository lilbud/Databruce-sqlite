import re, datetime

states = [
    "AK",
    "AL",
    "AR",
    "AZ",
    "CA",
    "CO",
    "CT",
    "DC",
    "DE",
    "FL",
    "GA",
    "HI",
    "IA",
    "ID",
    "IL",
    "IN",
    "KS",
    "KY",
    "LA",
    "MA",
    "MD",
    "ME",
    "MI",
    "MN",
    "MO",
    "MS",
    "MT",
    "NC",
    "ND",
    "NE",
    "NH",
    "NJ",
    "NM",
    "NV",
    "NY",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VA",
    "VT",
    "WA",
    "WI",
    "WV",
    "WY",
]

provinces = ["AB", "BC", "NB", "ON", "QC"]


def venue_name_fix(name):
    # fixes a few venue names that are incorrect
    # usually missing commas or spaces
    match (name):
        case "Alvin Theatre New York City Ny":
            name = "Alvin Theatre, New York City, NY"
        case "Gwinnett Civic Center Arena Duluth Ga":
            name = "Gwinnett Civic Center Arena, Duluth, GA"
        case "John F. Kennedy Memorial Center For The Performing Arts,Washington, DC":
            name = "John F. Kennedy Memorial Center For The Performing Arts, Washington, DC"

    for n in ["The", "Le", "De", "New"]:
        if f"({n})" in name:
            name = f"{n} " + re.sub(f" *\({n}\),* *", "", name)

    return name


def song_link_corrector(url):
    # fixes a single link that doesn't match up to songs table
    match (url):
        case "/song:rainy-day-women#12%20&%2035" | "/song:rainy-day-women#12 & 35":
            return "/song:rainy-day-women"
        case _:
            return url


def name_split(name, url):
    venue = []
    show = ""
    name = venue_name_fix(name)

    vn = name.split(", ")

    name = vn[0]
    city = vn[-2]
    state = country = vn[-1]

    # looks for where the show name has an identifier in it like (Early)/(Late)
    if re.match(r"[A-Z]{2}$", vn[-1]):
        state = vn[-1][:2]

    if re.match("\(.*\)", vn[-1]):
        show = re.findall("\(.*\)", vn[-1])[0].strip("()")

    if len(vn) == 4:
        name = ", ".join(vn[:1])

    if state in states:
        country = "USA"
    elif state in provinces:
        country = "Canada"

    venue.append([url, name, city, state, country, show])
    return venue


print(
    name_split(
        "John F. Kennedy Memorial Center For The Performing Arts,Washington, DC", "site"
    )
)

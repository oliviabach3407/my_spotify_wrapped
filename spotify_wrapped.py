import pandas as pd
import re
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
import requests
import time

USER_AGENT = "" #REPLACE with something unique to you (the 1.0.0 is the version of your program)
GOOGLE_SHEETS_LINK = "" #REPLACE

HOW_MANY_ARTIST = 10  # top 10 most-played artists
HOW_MANY_SONG = 10  # top 10 most-played songs

#currently, HOW_MANY_GENRES has to be a <= number than HOW_MANY_ARTIST
HOW_MANY_GENRES = 5 # top 5 occurrences of genres within your top artists

userChoseMonth = False

#function to dynamically convert Google Sheets URL to CSV export URL
def convert_google_sheet_url(url):
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'
    replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'
    return re.sub(pattern, replacement, url)

#function to count the amount of songs per a given month
def count_songs_by_month(df, month):
    count = len(df[df.date.str.contains(month)])
    hours = (3 * count) / 60
    print(f"{month.upper()} SONG NUMBER: {count} (ROUGHLY {hours:.2f} HOURS)")

#function to find the day that had the highest amount of songs played
def day_with_most_songs(df):
    #convert 'date' to datetime format
    df['date'] = pd.to_datetime(df['date'], format='%B %d, %Y at %I:%M%p')
    
    #extract the date part and use Counter to count occurrences
    date_counts = Counter(df['date'].dt.date)
    
    #find the day with the most songs
    max_day, max_count = date_counts.most_common(1)[0]
    
    print(f"\nDAY WITH MOST SONGS: {max_day} ({max_count} SONGS)")

#function to fetch genre from MusicBrainz
def get_genre_from_musicbrainz(artist_name):
    time.sleep(1) #must wait at least 1 second between queries to this specific API

    url = f"https://musicbrainz.org/ws/2/artist/?query={artist_name}&fmt=json"
    headers = {
        "User-Agent": USER_AGENT
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get('artists'):
            #fetch genres from the first matching artist
            artist_data = data['artists'][0]
            genres = [tag['name'] for tag in artist_data.get('tags', [])]
            return genres
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching genre for {artist_name}: {e}")
        return []

#function to call the API for each artist
def analyze_top_genres(popular_artists):
    genre_counter = Counter()
    for artist in popular_artists:
        genres = get_genre_from_musicbrainz(artist)
        genre_counter.update(genres)
    return genre_counter.most_common(HOW_MANY_GENRES)

###################
#      MAIN       #
###################

#automatically detect the current year
current_year = datetime.now().year
pandas_url = convert_google_sheet_url(GOOGLE_SHEETS_LINK)

#try loading data, with error handling
try:
    df = pd.read_csv(pandas_url)
except Exception as e:
    print(f"Error loading data: {e}")
    exit()

df = pd.read_csv(pandas_url, header=None)
df.columns = ['date', 'song', 'artist', 'id', 'link']

###################
# SONGS BY MONTH  #
###################

print(f'''+-----------------------------------+
| Songs by Month for the Year: {current_year} |
+-----------------------------------+''')

#analyze and print monthly song counts
for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
    count_songs_by_month(df, month)

##########################
# DAY WITH MOST LISTENS  #
##########################

day_with_most_songs(df)

######################
# GETTING USER INPUT #
######################

#filter by either month AND year or just year:
monthOrYear = input("\nWould you like to get your results based on a month or the whole year? (Answer m or y)\n")
if monthOrYear[0].strip().lower() == 'm':
    month_input = input("\nWhich month would you like to get specific data for?\n")
    month_input = month_input.strip().capitalize() #reformat user input

    try:
        #filter the google sheet by month AND year
        filtered_df = df[df['date'].dt.strftime('%B %Y') == f'{month_input} {current_year}']
    except Exception as e:
        print(f"Error filtering by {month_input}. Either you entered the Month wrong, or there is no data for that month.")

    userChoseMonth = True

elif monthOrYear[0].strip().lower() == 'y':
    filtered_df = df[df['date'].dt.strftime('%Y') == f'{current_year}']

    userChoseMonth = False

else:
    print("Invalid Input. Please try again.")

###############################
# SUMMARY OF LISTENING TRENDS #
# TOP ARTISTS                 #
# TOP SONGS                   #
###############################

#some error-checking to make sure the filtering works
if len(filtered_df) == 0:
    print(f"\n[ERROR] No data found for {month_input} {current_year}. Please check the date format.")

else:
    counts_artist = Counter(filtered_df.artist)
    counts_song = Counter(filtered_df.song)

    top_artist = counts_artist.most_common() #if you want to display just top artist
    top_song = counts_artist.most_common() #if you want to display just top song

    most_popular_artists = counts_artist.most_common(HOW_MANY_ARTIST)
    most_popular_songs = counts_song.most_common(HOW_MANY_SONG)

    if userChoseMonth:
        print("\n------------------------------------------------")
        print(f"FILTERING BY MONTH: {month_input} AND YEAR: {current_year}")
        print("------------------------------------------------")

        print(f'''\n+----------------------------------+
| Summary of Your Listening Trends |
+----------------------------------+''')
        print(f"You LISTENED TO {len(counts_artist.items())} DIFFERENT ARTISTS IN {month_input}, {current_year}")
        print(f"You LISTENED TO {len(counts_song.items())} DIFFERENT SONGS IN {month_input}, {current_year}")
        print(f"You LISTENED TO {len(filtered_df)} SONGS IN {month_input}, {current_year} ({3*len(filtered_df)} MINUTES OR {3*len(filtered_df) / 60:.2f} HOURS)")
    else:
        print("\n------------------------------------------------")
        print(f"FILTERING BY YEAR: {current_year}")
        print("------------------------------------------------")

        print(f'''\n+----------------------------------+
| Summary of Your Listening Trends |
+----------------------------------+''')
        print(f"You LISTENED TO {len(counts_artist.items())} DIFFERENT ARTISTS IN {current_year}")
        print(f"You LISTENED TO {len(counts_song.items())} DIFFERENT SONGS IN {current_year}")
        print(f"You LISTENED TO {len(filtered_df)} SONGS IN {current_year} ({3*len(filtered_df)} MINUTES OR {3*len(filtered_df) / 60:.2f} HOURS)")

    print(f'''\n+----------------+
| Top {HOW_MANY_ARTIST} Artists |
+----------------+''')    
    for i, (artist, count) in enumerate(most_popular_artists, start=1):
        print(f"{i}. {artist}: {count} plays")
    
    print(f'''\n+--------------+
| Top {HOW_MANY_SONG} Songs |
+--------------+''')    
    for i, (song, count) in enumerate(most_popular_songs, start=1):
        print(f"{i}. {song}: {count} plays")

###################
# GENRE ANALYSIS  #
###################

print("\n\nAccessing genre API - this will take a few seconds...")

#usage with a list of top artists
top_genres = analyze_top_genres(most_popular_artists) #replace most_popular_artists with 

print(f'''\n+--------------+
| Top {HOW_MANY_GENRES} Genres |
+--------------+''') 

#genres are figured out by how artists are listed on musicbrainz
for genre, count in top_genres:
    print(f"{genre.upper()}: {count} occurrences within your top {HOW_MANY_ARTIST} artists")

#visualize top genres with a graph (this works, if you want it, just uncomment)
# if top_genres:
#     genres, counts = zip(*top_genres)
#     plt.figure(figsize=(8, 5))
#     plt.bar(genres, counts, color='lightcoral')
#     plt.title('Top 5 Genres')
#     plt.xlabel('Genre')
#     plt.ylabel('Occurrences')
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.show()

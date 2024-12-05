'''
This is the newest version of spotify_wrapped script. 
Use this one. 

1. You need to follow the instructions in the https://github.com/liz-stippell/spotify_data README before being able to run this script. 
        ^^^ or you just need an existing google sheet that has your listening data in this format:
                      1                 2           3           4                                       5
        April 29, 2022 at 10:16PM	song_name  artist_name	spotify_track_id	https://open.spotify.com/track/spotify_track_id	

        My code doesn't actually use columns 4 and 5, but that's how the Applet puts the data into your sheet.
        Therefore, if you have a google sheet that has the first 3 columns and you add random data to the 4th and 5th columns,
        it will still work - in other words, this code will work for ANY COLLECTION OF SONGS - NOT JUST SPOTIFY

2. Make sure all global variables have been updated to fit your unique data
    -USER_AGENT (ex: MyUniqueName/1.0.0 ( valid@email.address ) - where 1.0.0 is a version number (can be anything))
        --> this is super flexible, the words can be anything as long as it fits this format and the 
        email is a valid email. You will be kicked out if it's not a valid email. If you don't want a 
        genre analysis, you can skip this step and comment out anything after 
        ###################
        # GENRE ANALYSIS  #
        ###################
    -HOW_MANY_ARTIST, HOW_MANY_SONG, HOW_MANY_GENRES (you can leave these as the default)
        --> see those global variables for an explanation of what they control
    -GOOGLE_SHEETS_LINKS (this is where you put the URL(s) for the google sheet(s) that have all of your listening data)
        --> IMPORTANT: this link is the link in your browser's search bar - NOT THE SHARE LINK 
        --> you NEED to give edit permissions to anyone that has the link (in the share bar)
        --> if you only have one google sheet, follow the instructions in the comments near that global variable
        --> if you have more than one, just keep adding them in this format (PAY ATTENTION TO THE COMMAS):
                GOOGLE_SHEETS_LINKS = [
                    "link one", 
                    "link two",
                    "link three",
                    "link four"
                ]
    
AT MOST, this script should take around 5 minutes to run. Unless you have a crazy amount of spreadsheets.
'''

import pandas as pd
import re
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
import requests
import time
import textwrap

#CHANGE THESE GLOBAL VARIABLES:
USER_AGENT = "MyUniqueName/1.0.0 ( valid@email.address )" #REPLACE with your own user-agent - where 1.0.0 is a version number (can be anything)
HOW_MANY_ARTIST = 10 #how many top-played artists do you want to display
HOW_MANY_SONG = 10 #how many top-played songs do you want to display
HOW_MANY_GENRES = 10 #how many top genres do you want to display

#list of Google Sheets URLs (add more as needed)
#if you only have one, delete the comma and last ""
#there has to be at least one link for this to run
GOOGLE_SHEETS_LINKS = [
    "",
    ""
]

#########################################
#DO NOT CHANGE ANYTHING BELOW THIS LINE:#
#########################################

#helper function to display nice titles
def format_title(title, width=30, char='-'):
    wrapper = textwrap.TextWrapper(width=width, expand_tabs=False)
    centered_title = f" {title} ".center(width, char)
    border = char * width
    return f"\n\n{border}\n{centered_title}\n{border}\n"

#another helper function for nice titles
def format_boxed_title(title, width=40):
    # Ensure the title fits within the box
    wrapped_title = textwrap.fill(title, width=width - 4)
    border = '+' + '-' * (width - 2) + '+'
    lines = wrapped_title.splitlines()
    
    padded_lines = [f"| {line.center(width - 4)} |" for line in lines]
    
    return f"\n{border}\n" + "\n".join(padded_lines) + f"\n{border}"

#function to dynamically convert Google Sheets URL to CSV export URL
def convert_google_sheet_url(url):
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'
    replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'
    return re.sub(pattern, replacement, url)

#function to count the amount of songs per a given month
def count_songs_by_month(df, month):
    count = len(df[df['date'].dt.strftime('%B') == month])
    hours = (3 * count) / 60
    print(f"{month.upper()} SONG NUMBER: {count} (ROUGHLY {hours:.2f} HOURS)")

#function to find the day that had the highest amount of songs played
def day_with_most_songs(df):
    df.loc[:, 'date'] = pd.to_datetime(df['date'], format='%B %d, %Y at %I:%M%p')
    date_counts = Counter(df['date'].dt.date)
    max_day, max_count = date_counts.most_common(1)[0]
    minutes = (3 * max_count)
    print(f"\nDAY WITH MOST SONGS: {max_day} ({max_count} SONGS) (ROUGHLY {minutes} MINUTES)")

#function to fetch genre from MusicBrainz
def get_genre_from_musicbrainz(artist_name):
    time.sleep(1)  #MUST wait at least 1 second between queries to this specific API
    url = f"https://musicbrainz.org/ws/2/artist/?query={artist_name}&fmt=json"
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get('artists'):
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

#function to load and combine multiple Google Sheets into one DataFrame
def load_and_combine_sheets(sheet_links):
    combined_df = pd.DataFrame()
    for link in sheet_links:
        try:
            csv_url = convert_google_sheet_url(link)
            df = pd.read_csv(csv_url, header=None)
            df.columns = ['date', 'song', 'artist', 'id', 'link']
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        except Exception as e:
            print(f"Error loading data from {link}: {e}")
    return combined_df

#function to calculate top genres for a given month
def top_genres_by_month(df, month, how_many=3):
    genre_counter = Counter()
    filtered_month = df[df['date'].dt.strftime('%B %Y').str.contains(month)]
    popular_artists = filtered_month['artist'].value_counts().head(HOW_MANY_ARTIST).index
    for artist in popular_artists:
        genres = get_genre_from_musicbrainz(artist)
        genre_counter.update(genres)
    return genre_counter.most_common(how_many)

######################
#       MAIN         #
######################

#load and combine data from all sheets
df = load_and_combine_sheets(GOOGLE_SHEETS_LINKS)

#convert the 'date' column to datetime after loading the data
try:
    df['date'] = pd.to_datetime(df['date'], format='%B %d, %Y at %I:%M%p', errors='coerce')
except Exception as e:
    print(f"Error converting dates: {e}")

#automatically detect the current year
current_year = datetime.now().year

######################
# GETTING USER INPUT #
######################

#instructions for user input:
print("--------------------------------------------------------------------------")
print("INSTRUCTIONS FOR USE:")
print("\nYou will be asked if you want to filter by month or by the whole year.\nFiltering by month will reduce all your statistics to just that month (within the current year).\nIf you filter by the whole year, then you will get some extra analytics about your top 3 genres per month within the current year.)")
print("\n\nAnything related to the genre takes some time because it is grabbing information from an external API.\nJust be patient, it should take around 5 minutes total to run.\nIf you change your mind, just stop the script and run it again.")
print("--------------------------------------------------------------------------")

#filter by either month AND year or just year:
monthOrYear = input("Would you like to get your results based on a month or the whole year? (Answer m or y)\n")
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
        print(format_title(f"FILTERING BY MONTH: {month_input} AND YEAR: {current_year}", width=50))

        ########################
        # SONGS BY MONTH       #
        ########################

        print(format_boxed_title(f"Songs by Month for the Year: {current_year}", width=50))
        for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
            count_songs_by_month(filtered_df, month)

        ##########################
        # DAY WITH MOST LISTENS  #
        ##########################

        day_with_most_songs(filtered_df)

        print(format_boxed_title(f"Summary of Your Listening Trends", width=50))
        print(f"You LISTENED TO {len(counts_artist.items())} DIFFERENT ARTISTS IN {month_input}, {current_year}")
        print(f"You LISTENED TO {len(counts_song.items())} DIFFERENT SONGS IN {month_input}, {current_year}")
        print(f"You LISTENED TO {len(filtered_df)} TOTAL SONGS IN {month_input}, {current_year} ({3*len(filtered_df)} MINUTES OR {3*len(filtered_df) / 60:.2f} HOURS)")
    else:
        print(format_title(f"FILTERING BY YEAR: {current_year}", width=50))

        ########################
        # SONGS BY MONTH       #
        ########################

        print(format_boxed_title(f"Songs by Month for the Year: {current_year}", width=50))
        for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
            count_songs_by_month(filtered_df, month)

        ##########################
        # DAY WITH MOST LISTENS  #
        ##########################

        day_with_most_songs(filtered_df)

        print(format_boxed_title(f"Summary of Your Listening Trends", width=50))
        print(f"You LISTENED TO {len(counts_artist.items())} DIFFERENT ARTISTS IN {current_year}")
        print(f"You LISTENED TO {len(counts_song.items())} DIFFERENT SONGS IN {current_year}")
        print(f"You LISTENED TO {len(filtered_df)} TOTAL SONGS IN {current_year} ({3*len(filtered_df)} MINUTES OR {3*len(filtered_df) / 60:.2f} HOURS)")

    print(format_boxed_title(f"Top {HOW_MANY_ARTIST} Artists", width=50))

    for i, (artist, count) in enumerate(most_popular_artists, start=1):
        print(f"{i}. {artist}: {count} plays")

    print(format_boxed_title(f"Top {HOW_MANY_SONG} Songs", width=50))

    for i, (song, count) in enumerate(most_popular_songs, start=1):
        print(f"{i}. {song}: {count} plays")

###################
# GENRE ANALYSIS  #
###################

print("\n\nAccessing genre API - this will take a few seconds...")

#usage with a list of top artists
top_genres = analyze_top_genres(most_popular_artists) #replace most_popular_artists with 

print(format_boxed_title(f"Top {HOW_MANY_GENRES} Genres", width=50))

#genres are figured out by how artists are listed on musicbrainz
for genre, count in top_genres:
    print(f"{genre.upper()}: {count} occurrences within your top {HOW_MANY_ARTIST} artists")

#only show genre breakdown by month if user didn't choose a specific month to filter by
if not userChoseMonth:
    for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
        print(format_boxed_title(f"Top 3 Genres for {month}", width=50)) 
        count_songs_by_month(filtered_df, month)
        top_genres = top_genres_by_month(filtered_df, month, how_many=3)
        for genre, count in top_genres:
            print(f"{genre.upper()}: {count} occurrences")
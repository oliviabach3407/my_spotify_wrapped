'''
If you haven't been collecting your spotify data for as long as you've been listening,
this script will import your listening history into a google sheet:

    1. Request all of your data history from Spotify (in settings - or look up how to do this) (takes a few days)
    2. They give you a zipped folder that has ONE json file with your entire listening history (the biggest file in that zip)
    3. Put that file into THIS directory (I named mine 'listening_history.json')
    4. Set up a google sheets API (free) - you need a SERVICE ACCOUNT - generate a key + json service account file
            ^^^ this step can be a bit complicated - look up a tutorial (will not work with anything except a SERVICE ACCOUNT)
    5. Recommended to put your JSON service file in THIS directory (mine is not here because I don't want you using it)
    6. Make sure all global variables have been updated to fit your unique data
        -SPREADSHEET_ID (an ID that is part of the link to your google sheet - it's just numbers and letters)
            if this is the whole link: https://docs.google.com/spreadsheets/d/1GAwwRdsP04GesfHzVwhcmE_OuYCdk4pNdoVxWpb-yfg/edit?gid=0#gid=0
            the id is this part: 1GAwwRdsP04GesfHzVwhcmE_OuYCdk4pNdoVxWpb-yfg
            MAKE SURE THAT YOU HAVE SHARED THIS SPREADSHEET WITH YOUR SERVICE ACCOUNT'S EMAIL ADDRESS (see in a tutorial)
        -SHEET_NAME (ex. Sheet1 or Sheet2) --> IMPORTANT: the sheet with that name has to exist for the code to run correctly
            ^^^ this sheet will be overwritten, so make sure it's empty before you run this program
        -SERVICE_ACCOUNT_FILE (the path to your SERVICE ACCOUNT API JSON file - inlude the name of that file)
        -YOUR_JSON_FILE (the path to your listening history JSON file - the one Spotify gave to you - include the name of that file)

If all goes well and you have set up the Google Sheets Applet for the other script, you should only have to run this script once
You can delete your Service Account after you run it, but there's no penalty for keeping it.
'''

import json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime

#CHANGE THESE GLOBAL VARIABLES:
SPREADSHEET_ID = '1GAwwRdsP04GesfHzVwhcmE_OuYCdk4pNdoVxWpb-yfg' #REPLACE: example ID
SHEET_NAME = 'Sheet2' #make this Sheet 1 if you are using a new google sheet (if you go with Sheet2, that sheet HAS to exist)
SERVICE_ACCOUNT_FILE = "C://Users//olivi//Desktop//Programming//Python//my_spotify_wrapped\second-form-443801-b8-e88590bc1590.json" #REPLACE: need to put the full path to the file if you don't have it in THIS directory
YOUR_JSON_FILE = "listening_history.json" #REPLACE: need to put the full path to the file if you don't have it in THIS directory

#########################################
#DO NOT CHANGE ANYTHING BELOW THIS LINE:#
#########################################

#loading JSON file
with open(YOUR_JSON_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

#format the data from the file
rows = []
for entry in data:
    ts = entry.get("ts", "")
    track_name = entry.get("master_metadata_track_name", "Unknown")
    artist_name = entry.get("master_metadata_album_artist_name", "Unknown")
    track_id = entry.get("spotify_track_uri", "").split(":")[-1]
    link_to_track = f"https://open.spotify.com/track/{track_id}"
    formatted_date = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y at %I:%M%p")
    rows.append([formatted_date, track_name, artist_name, track_id, link_to_track])

#turn all that data into a DataFrame
df = pd.DataFrame(rows)

#authenticate with the service account
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
service = build('sheets', 'v4', credentials=credentials)

#prepare data for Sheets
body = {
    "values": [df.columns.tolist()] + df.values.tolist()  # Include headers
}

#write data to Google Sheets
sheet = service.spreadsheets()
result = sheet.values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=f"{SHEET_NAME}!A1",
    valueInputOption="RAW",
    body=body
).execute()

print(f"Data successfully written to Google Sheets! Updated {result.get('updatedCells')} cells.")

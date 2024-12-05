# My Spotify Wrapped Program

Inspired heavily by https://github.com/liz-stippell/spotify_data

## Features:

-Two different scripts 

--> new_spotify_wrapped : when run, will look at EXISTING google sheet(s) to generate a spotify wrapped

--> json_to_sheets : when run, will write the listening data in a SPOTIFY json file to a google sheet

## WHERE TO START:

-If you have no existing spotify listening data in a google sheets table, follow the instructions in json_to_sheets. 

-If you DO have existing spotify listening data in a google sheets table, follow the instructions in new_spotify_wrapped.

-If you want to start collecting data on your listening (adding lines to a sheet every time you listen to a song), follow the instructions below 

## Instructions To Activate Your Google Sheets Applet:

1. Follow the setup instructions outlined in this readme: https://github.com/liz-stippell/spotify_data

2. Then replace line 9 and 10 in this spotify_wrapped.py with your unique user-agent and google sheets URL.

3. For the user-agent, it can be anything as long as it is in the format:

      NameOfProgram/1.0.0 ( valid@email.address )

5. Extra installs:

      pip install pandas

      pip install matplotlib
      
      pip install requests
      
      pip install textwrap
      
      pip install json

      pip install google-api-python-client 

      pip install google-auth

## Example Output:

Would you like to get your results based on a month or the whole year? (Answer m or y)
y


--------------------------------------------------
------------ FILTERING BY YEAR: 2024 -------------
--------------------------------------------------


+------------------------------------------------+
|       Songs by Month for the Year: 2024        |
+------------------------------------------------+
JANUARY SONG NUMBER: 349 (ROUGHLY 17.45 HOURS)
FEBRUARY SONG NUMBER: 736 (ROUGHLY 36.80 HOURS)
MARCH SONG NUMBER: 583 (ROUGHLY 29.15 HOURS)
APRIL SONG NUMBER: 1016 (ROUGHLY 50.80 HOURS)
MAY SONG NUMBER: 174 (ROUGHLY 8.70 HOURS)
JUNE SONG NUMBER: 1540 (ROUGHLY 77.00 HOURS)
JULY SONG NUMBER: 1839 (ROUGHLY 91.95 HOURS)
AUGUST SONG NUMBER: 1021 (ROUGHLY 51.05 HOURS)
SEPTEMBER SONG NUMBER: 1054 (ROUGHLY 52.70 HOURS)
OCTOBER SONG NUMBER: 1185 (ROUGHLY 59.25 HOURS)
NOVEMBER SONG NUMBER: 29 (ROUGHLY 1.45 HOURS)
DECEMBER SONG NUMBER: 182 (ROUGHLY 9.10 HOURS)

DAY WITH MOST SONGS: 2024-08-03 (213 SONGS) (ROUGHLY 639 MINUTES)

+------------------------------------------------+
|        Summary of Your Listening Trends        |
+------------------------------------------------+
You LISTENED TO 611 DIFFERENT ARTISTS IN 2024
You LISTENED TO 1375 DIFFERENT SONGS IN 2024
You LISTENED TO 9708 TOTAL SONGS IN 2024 (29124 MINUTES OR 485.40 HOURS)

+------------------------------------------------+
|                 Top 10 Artists                 |
+------------------------------------------------+
1. Example Artist: 631 plays
2. Example Artist: 346 plays
3. Example Artist: 337 plays
4. Example Artist: 308 plays
5. Example Artist: 264 plays
6. Example Artist: 171 plays
7. Example Artist: 161 plays
8. Example Artist: 159 plays
9. Example Artist: 153 plays
10. Example Artist: 136 plays

+------------------------------------------------+
|                  Top 10 Songs                  |
+------------------------------------------------+
1. Example Song: 101 plays
2. Example Song: 57 plays
3. Example Song: 56 plays
4. Example Song: 55 plays
5. Example Song: 51 plays
6. Example Song: 41 plays
7. Example Song: 39 plays
8. Example Song: 38 plays
9. Example Song: 37 plays
10. Example Song: 35 plays


Accessing genre API - this will take a few seconds...

+------------------------------------------------+
|                 Top 10 Genres                  |
+------------------------------------------------+
ALTERNATIVE ROCK: 3 occurrences within your top 10 artists
ROCK: 2 occurrences within your top 10 artists
RAP: 2 occurrences within your top 10 artists
HIP HOP: 2 occurrences within your top 10 artists
INDIE ROCK: 2 occurrences within your top 10 artists
INDIE POP: 2 occurrences within your top 10 artists
POP RAP: 2 occurrences within your top 10 artists
INDIETRONICA: 2 occurrences within your top 10 artists
POP: 1 occurrences within your top 10 artists
HIP-HOP: 1 occurrences within your top 10 artists

+------------------------------------------------+
|            Top 3 Genres for January            |
+------------------------------------------------+
JANUARY SONG NUMBER: 349 (ROUGHLY 17.45 HOURS)
ALTERNATIVE ROCK: 8 occurrences
INDIE ROCK: 4 occurrences
ROCK: 3 occurrences

+------------------------------------------------+
|           Top 3 Genres for February            |
+------------------------------------------------+
FEBRUARY SONG NUMBER: 736 (ROUGHLY 36.80 HOURS)
METAL: 3 occurrences
METALCORE: 3 occurrences
ROCK: 2 occurrences

+------------------------------------------------+
|             Top 3 Genres for March             |
+------------------------------------------------+
MARCH SONG NUMBER: 583 (ROUGHLY 29.15 HOURS)
ALTERNATIVE ROCK: 6 occurrences
INDIE ROCK: 3 occurrences
ROCK: 2 occurrences

+------------------------------------------------+
|             Top 3 Genres for April             |
+------------------------------------------------+
APRIL SONG NUMBER: 1016 (ROUGHLY 50.80 HOURS)
ALTERNATIVE ROCK: 5 occurrences
INDIE ROCK: 3 occurrences
ROCK: 2 occurrences

+------------------------------------------------+
|              Top 3 Genres for May              |
+------------------------------------------------+
MAY SONG NUMBER: 174 (ROUGHLY 8.70 HOURS)
METAL: 3 occurrences
INDIE ROCK: 3 occurrences
INDUSTRIAL METAL: 2 occurrences

+------------------------------------------------+
|             Top 3 Genres for June              |
+------------------------------------------------+
JUNE SONG NUMBER: 1540 (ROUGHLY 77.00 HOURS)
ALTERNATIVE ROCK: 6 occurrences
INDIE ROCK: 4 occurrences
ROCK: 2 occurrences

+------------------------------------------------+
|             Top 3 Genres for July              |
+------------------------------------------------+
JULY SONG NUMBER: 1839 (ROUGHLY 91.95 HOURS)
ALTERNATIVE ROCK: 4 occurrences
ROCK: 3 occurrences
POP ROCK: 3 occurrences

+------------------------------------------------+
|            Top 3 Genres for August             |
+------------------------------------------------+
AUGUST SONG NUMBER: 1021 (ROUGHLY 51.05 HOURS)
ALTERNATIVE ROCK: 3 occurrences
ROCK INDIE GRUNGE PSYCHEDELIC BRIGHTON RAYGUN MUSIC RECORDS: 1 occurrences
RAP: 1 occurrences

+------------------------------------------------+
|           Top 3 Genres for September           |
+------------------------------------------------+
SEPTEMBER SONG NUMBER: 1054 (ROUGHLY 52.70 HOURS)
ALTERNATIVE ROCK: 3 occurrences
BRITISH: 2 occurrences
UK: 2 occurrences

+------------------------------------------------+
|            Top 3 Genres for October            |
+------------------------------------------------+
OCTOBER SONG NUMBER: 1185 (ROUGHLY 59.25 HOURS)
ALTERNATIVE ROCK: 3 occurrences
ELECTROPOP: 3 occurrences
POP ROCK: 3 occurrences

+------------------------------------------------+
|           Top 3 Genres for November            |
+------------------------------------------------+
NOVEMBER SONG NUMBER: 29 (ROUGHLY 1.45 HOURS)
HARD ROCK: 4 occurrences
HEAVY METAL: 3 occurrences
METAL: 2 occurrences

+------------------------------------------------+
|           Top 3 Genres for December            |
+------------------------------------------------+
DECEMBER SONG NUMBER: 182 (ROUGHLY 9.10 HOURS)
ROCK: 3 occurrences
ALTERNATIVE ROCK: 3 occurrences
PROGRESSIVE ROCK: 3 occurrences
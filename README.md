# My Spotify Wrapped Program

Inspired heavily by https://github.com/liz-stippell/spotify_data

## Instructions For Use:

Follow the setup instructions outlined in this readme: https://github.com/liz-stippell/spotify_data

Then replace line 9 and 10 in this spotify_wrapped.py with your unique user-agent and google sheets URL.

For the user-agent, it can be anything as long as it is in the format: 
     NameOfProgram/1.0.0 ( valid@email.address )

Extra installs:
      pip install matplotlib
      pip install requests
      pip install time

## What is Different In this Version: 
-Modularized the existing code in https://github.com/liz-stippell/spotify_data
---> created some more global constants (for number of top artists/songs/genres displayed)
---> added user input to determine which month to give specific data for
-Added a top genre analysis
---> utlizes the musicbrainz API to link artists to their genre
---> determines your top genres based on what genre your top artists are associated with
---> can generate a graph that displays your top genres if you uncomment the code at the bottom

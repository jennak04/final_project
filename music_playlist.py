### MUSIC PLAYLIST MAKER

import requests
import json
import os

from dotenv import load_dotenv 

load_dotenv() 
API_KEY = os.getenv("GEMINI_API_KEY")

URL = (
    "https://generativelanguage.googleapis.com"
    "/v1beta/models/gemini-2.5-flash:generateContent"
    f"?key={API_KEY}"
)

# Testing api key

# if API_KEY:
#     print("API key loaded successfully!")
# else:
#     print("API key not found.")

######### FUNCTION - CREATE PLAYLIST ###########
def create_playlist():
    """Allows user to name playlist"""
    return input("Enter playlist name: ")

########################################

playlist = []
playlist_name = ""

######### FUNCTION - GET SONG INFO ###########

# Ask gemini for song information
# def get_song_info(song_name):
#     """Get song information using Gemini."""

#     prompt = f"""
#     The user entered this song:

#     {song_name}

#     Find information about the song and return ONLY valid JSON.

#     Use this exact format:

#     {{
#         "song": "song title",
#         "artist": "artist name",
#         "genre": "genre",
#         "duration": "minutes:seconds",
#         "description": "1-2 sentence description"
#     }}

#     rules:
#     - Return only JSON.
#     - No extra text before or after the JSON.
#     """

#     body = {"contents": [{"parts": [{"text": prompt}]}]}

#     try:
#         response = requests.post( URL, 
#         headers={"Content-Type": "application/json"}, 
#         json=body, timeout=30 ) 
        
#         if response.status_code != 200: 
#             print("API Error:", response.status_code) 
#             return None

#         data = response.json()

#         text = data["candidates"][0]["content"]["parts"][0]["text"].strip()

#         if text.startswith("```"):
#             text = text.split("\n", 1)[1]
#             text = text.rsplit("```", 1)[0]

#         return json.loads(text)

#     except Exception as e:
#         print("Error getting song information:", e)
#         return None

# MOCK FUNCTION to avoid api errors during testing

def get_song_info(song_name):
    """Mock version for testing without API"""

    print(f"(MOCK) Getting info for: {song_name}")

    return {
        "song": song_name,
        "artist": "Test Artist",
        "genre": "Pop",
        "duration": "3:30",
        "description": "This is a fake description used for testing"
    }
    
######### FUNCTION - VIEW PLAYLIST ###########

def view_playlist():
    if not playlist:
        print("Playlist is empty.")
        return

    print(f"\n===== {playlist_name} =====")

    for i, song in enumerate(playlist, 1):
        print(
            f"{i}. {song['song']} - "
            f"{song['artist']} ({song['duration']})")
    
######### FUNCTION - ADD SONG ###########

def add_song():
    song_name = input("Enter song name: ")

    result = get_song_info(song_name)

    if result:
        playlist.append(result)
        print(f"Added {result['song']} by {result['artist']}")
        
        
#####################################

######### FUNCTION - REMOVE SONG ###########

def remove_song():
    if not playlist:
        print("Playlist is empty.")
        return

    view_playlist()

    try:
        index = int(input("Song number to remove: ")) - 1

        if 0 <= index < len(playlist):
            removed = playlist.pop(index)
            print(f"Removed {removed['song']}")
        else:
            print("Invalid song number")

    except ValueError:
        print("Please enter a number")

########################################

######### FUNCTION - GET SONG DESCRIPTION ###########

def get_song_desc():
    if not playlist:
        print("Playlist is empty")
        return

    view_playlist()

    try:
        index = int(input("Song number: ")) - 1

        if 0 <= index < len(playlist):
            song = playlist[index]

            print()
            print(f"Genre:\n{song['genre']}\n")
            print(f"Description:\n{song['description']}\n")

        else:
            print("Invalid song number")

    except ValueError:
        print("Please enter a number")
    
########################################

######### FUNCTION - GET PLAYLIST DESCRIPTION ###########

def get_playlist_desc():
    if not playlist:
        print("Playlist is empty.")
        return
    
    genres = []
    total_seconds = 0

    for song in playlist:
        genres.append(song["genre"])

        parts = song["duration"].split(":")
        minutes = int(parts[0])
        seconds = int(parts[1])
    
        total_seconds += minutes * 60 + seconds
        
    unique_genres = ", ".join(set(genres))
    total_minutes = total_seconds // 60
    remaining_seconds = total_seconds % 60

    print(
        f"'{playlist_name}' contains {len(playlist)} songs\n"
        f"Genres: {unique_genres}\n"
        f"Total Duration: {total_minutes}:{remaining_seconds:02d}\n"
    )

    print("Songs:")

    for song in playlist:
        print(f"- {song['song']} by {song['artist']}")
    

########################################

######### FUNCTION - SAVE PLAYLIST ###########

def save_playlist():
    filename = f"{playlist_name}.json"

    data = {
        "playlist_name": playlist_name,
        "songs": playlist
    }

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print(f"\nPlaylist saved to {filename}")

    except Exception as e:
        print("Error saving playlist:", e)

########################################

def main():
    global playlist_name

    print("🎵 MUSIC PLAYLIST MAKER 🎵")
    print("=" * 30)

    playlist_name = create_playlist()

    while True:
        print("\n1. Add Song")
        print("2. Remove Song")
        print("3. View Playlist")
        print("4. See song description")
        print("5. See playlist description")
        print("6. Save and Exit")

        choice = input("Choice: ")

        if choice == "1":
            add_song()

        elif choice == "2":
            remove_song()

        elif choice == "3":
            view_playlist()
            
            
        elif choice == "4":
            get_song_desc()
            
        elif choice == "5":
            get_playlist_desc()
            
        elif choice == "6":
            save_playlist()
            print("Playlist saved")
            break

        else:
            print("Invalid choice.")
            


main()
# For Pseudo see ./"Pseudo Codes"/main.md

import os
import json
import time
import playsound
import threading
import youtubesearchpython
import pytube
import random

# User Defined Modules
#import menus

"""
Q- How Will Code Work ???
A- we will gonna make a global youtubesearchpython.VideoSearch object with our search string
and call function download_song() which will download songs and keep 3 
songs in a upcoming queue so to fight delay due to buffering and at the and function will call
youtubesearchpython.VideoSearch().next() so that we can get a list of next 3 songs as soon as
user Reaches the end of queue we will download 3 more songs and enqueue them too.

Pseudo Code:
    1. make a global youtubesearchpython.VideoSearch object with our search string
    2. call function download_song() which will download songs
    3. make queue and add songs to it
    4. make thread to play songs
    5. At End Of of download_song() update new list of songs
    6. Download Songs if there are less than 2 songs in queue # Currently found no need but left if change mind in future
"""


class SongList:
    # contains the id time and name of all the songs in the current playlist
    songs = []
    current_song_number : int
    def __init__(self, 
            searchstr = None,
            song = None, 
            playlist = None, 
            shuffle = False, 
            repeatqueue = False,
            repeatone = False,
    ):
        if song: 
            self.songs.append(get_song_info(song))
        if playlist:
            self.songs.append(get_playlist_info(playlist))
        if searchstr:
            self.searchObject = youtubesearchpython.VideosSearch( searchstr, 
                    limit = 1) # it will fetch a single song at a time with requested type
        self.shuffle = shuffle
        self.current_song_number = 0
        self.repeatqueue = repeatqueue
        self.repeatone = repeatone
    """
        Returns a dict containing song_id, duration and title as a string that 
        needed to play next based on the user choices
    """
    def get_next_song(self) -> dict:
        if self.shuffle:
            return self.songs[random.randint(0, len(self.songs))]
        if self.repeatone:
            return self.songs[self.current_song_number]
        if self.repeatqueue :
            if self.current_song_number == len(self.songs):
                self.current_song_number = 0
        if self.searchObject:
            song = self.searchObject.result()["result"]
            self.searchObject.next()
            return {
                "id" : song.get("id"),
                "duration" : song.get("duration"),
                "title" : song.get("title"),
                "link" : song.get("link"),
            }
        self.current_song_number += 1
        return self.songs[self.current_song_number - 1]



"""
    This function will return a list of song id from a playlist
    The ids will later be used in playMusic() function to play music
"""
def get_playlist_info(playlist : str) -> list:
    songlist = youtubesearchpython.Playlist(playlist)
    playlist = []
    for i in songlist.videos:
        playlist.append({
            "id" : i.get("id"),
            "duration" : i.get("duration"),
            "title" : i.get("title"),
            "link" : i.get("link"),
        })
    return playlist

"""
    Return the information of a song that later be stored in SongList object
"""
def get_song_info(song_id : str) -> list:
    video = json.loads(youtubesearchpython.Video.get(song_id, 
            mode = youtubesearchpython.ResultMode.json))
    return [{
        "id" : video.get("id"),
        "duration" : video.get("duration"),
        "title" : video.get("title"),
        "link" : video.get("link"),
    }]


def playMusic(track_number: int = 1):
    number_of_attempts = 0

    while True:
        if len(musicQueue) > track_number:
            print("Currently Playing: ", musicQueue[track_number])
            playsound.playsound(musicQueue[track_number]) # it is intentional so that in future we can implement playing privious song again 
            track_number += 1
            number_of_attempts = 0
        elif number_of_attempts > 30:
            print("Internet speed is too slow :-( , Try again later")
            exit(1) # exiting code if no song is there to play from last 5 minutes 
        else:
            print("Please Wait for some time while we are downloading some songs")
            number_of_attempts += 1
            time.sleep(10)

def download_song(songlist : SongList, path : str = "./Downloads/"):
    currentsong = songlist.get_next_song() 
    link = currentsong["link"]
    title = currentsong["title"]
    video_duration = currentsong["duration"]
    # Checks For Is Song Of Suitable Length Or Not
    isVideoTooLongOrTooShort = (video_duration.count(":") != 1)
    isVideoShorterThan11Min = (int(video_duration.split(":")[0]) <= 11)

    if (not isVideoTooLongOrTooShort) and (isVideoShorterThan11Min):
        yt = pytube.YouTube(link)
        audio_stream = yt.streams.filter(only_audio=True).all()
        audio_stream[0].download(path)
    else:
        # Trying Again if current song isn't suitable for Downloading and playing
        songlist.next()
        download_song(songlist, path)
    
    # updating music queue
    songlist.next()

if __name__ == "__main__":
    musicQueue = [] # will store name of songs as soon as a song ends it will pop out the song before it (i.e. we will play song at index 1)

    # User Inputs i.e. latest released
    music_choice = input("Enter The Type Of Music/Song You Want To Listen :\t") + "song"

    thread = threading.Thread(target=playMusic, name="Music Player")
    thread.start()

    try:
        while True:
            songlist = SongList(searchstr=music_choice)
            download_song(songlist, path = "./Downloads/")
            if not thread.is_alive():
                break
    except KeyboardInterrupt:
        print("Exiting Process")
        thread._stop()
        exit(2)
        
    



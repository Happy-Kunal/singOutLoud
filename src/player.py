import os
import time
import playsound
import multiprocessing
import youtubesearchpython
import pytube
import youtubesearchpython
import random

class SongList:
    # contains the id time and name of all the songs in the current playlist
    songs = []
    current_song_number : int
    searchObject = None
    def __init__(self, 
            searchstr = None,
            song = None, 
            playlist = None, 
            shuffle = False, 
            repeatone = False,
            repeatqueue = False
    ):
        if song: 
            self.songs.append(get_song_info(song))
        if playlist:
            self.songs += get_playlist_info(playlist)
        if searchstr:
            self.searchObject = youtubesearchpython.VideosSearch( searchstr, 
                    limit = 1) # it will fetch a single song at a time with requested type
        self.shuffle = shuffle
        self.current_song_number = -1
        self.repeatqueue = repeatqueue
        self.repeatone = repeatone
    """
        Returns a dict containing song_id, duration and title as a string that 
        needed to play next based on the user choices
    """
    def get_next_song(self) -> dict:
        if self.shuffle:
            return self.songs[random.randrange(0, len(self.songs))]
        if self.repeatone:
            return self.songs[self.current_song_number]
        if self.repeatqueue :
            if self.current_song_number == len(self.songs) - 1:
                self.current_song_number = 0
        if self.searchObject:
            song = self.searchObject.result()["result"][0]
            self.searchObject.next()
            return {
                "id" : song.get("id"),
                "duration" : song.get("duration"),
                "title" : song.get("title"),
                "link" : song.get("link"),
            }
        self.current_song_number += 1
        return self.songs[self.current_song_number]



"""
    This function will return a list of song id from a playlist
    The ids will later be used in playMusic() function to play music
"""
def get_playlist_info(playlist : str) -> list:
    songlist = youtubesearchpython.Playlist(playlist)
    playlist = []
    for song in songlist.videos:
        playlist.append({
            "id" : song.get("id"),
            "duration" : song.get("duration"),
            "title" : song.get("title"),
            "link" : song.get("link"),
        })
    return playlist

"""
    Return the information of a song that later be stored in SongList object
"""
def get_song_info(song_id : str) -> list:
    video = youtubesearchpython.Video.get(song_id, 
            mode = youtubesearchpython.ResultMode.dict)
    return [{
        "id" : video.get("id"),
        "duration" : video.get("duration"),
        "title" : video.get("title"),
        "link" : video.get("link"),
    }]


def playMusic(SongListObject: SongList, path: str = "./Downloads/"):
    number_of_attempts = 0

    while True:
        if len(SongListObject.songs) < 1:
            print("Please Wait for some time while we are downloading some songs")
            number_of_attempts += 1
            time.sleep(10)

        elif number_of_attempts > 30:
            print("Internet speed is too slow :-( , Try again later")
            exit(1) # exiting code if no song is there to play from last 5 minutes 
        
        else:
            song = SongListObject.get_next_song()
            print("Currently Playing: ",song["title"])
            print("Duration :", song["duration"])
            playsound.playsound(f"{path}" + song["title"])
            number_of_attempts = 0
            
import time
import playsound
import youtubesearchpython
import pytube
import random

class SongList:
    # contains the id time and name of all the songs in the current playlist
    songs = []
    current_song_number : int
    playMusicThreadObject = None
    def __init__(self,
            path = "./Downloads/",
            searchstr = "English Songs",
            shuffle = False, 
            repeatone = False,
            repeatqueue = False
    ):
        
        self.path = path
        self.searchObject = youtubesearchpython.VideosSearch( searchstr, limit = 1) # it will fetch a single song at a time with requested type
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

        self.current_song_number += 1
        return self.songs[self.current_song_number]



def playMusic(SongListObject: SongList):
    number_of_attempts = 0
    path = SongListObject.path
    print("I am Here at Playmusic")
    print(SongListObject.songs)

    while True:
        if len(SongListObject.songs) == 0:
            print("I am Here at If")
            print(SongListObject.songs)
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
            playsound.playsound(path + song["title"] + ".mp4")
            number_of_attempts = 0
            
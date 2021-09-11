import time
import youtubesearchpython
import pytube
import random
import vlc


class Player:
    # contains the id time and name of all the songs in the current playlist
    songs = []
    current_song_number : int
    searchObject = None
    # dict to store the current song that is playing to download the song
    __currentSong = {}

    def __init__(self,
            searchstr = None,
            song = None,
            playlist = None,
            shuffle = False,
            repeatqueue = False,
            repeatone = False,
            path = "./Downloads"
    ):
        if song:
            self.songs.append(self.__get_song_info(song))
        if playlist:
            self.songs.append(self.__get_playlist_info(playlist))
        if searchstr:
            self.searchObject = youtubesearchpython.VideosSearch( searchstr,
                    limit = 1) # it will fetch a single song at a time with requested type
        self.shuffle = shuffle
        self.current_song_number = 0
        self.repeatqueue = repeatqueue
        self.repeatone = repeatone
        self.player = vlc.MediaPlayer()
        self.path = path


    def get_next_song(self) -> dict:
        """
        Returns a dict containing song_id, duration and title as a string that
        needed to play next based on the user choices
        """
        if self.shuffle:
            return self.songs[random.randint(0, len(self.songs) - 1)]
        if self.repeatone:
            return self.songs[self.current_song_number]
        if self.repeatqueue :
            if self.current_song_number == len(self.songs):
                self.current_song_number = 0
        if self.searchObject:
            song = self.searchObject.result()["result"][0]
            self.searchObject.next()
            # storing the result in the song list to enable more features
            self.songs.append({
                "id" : song.get("id"),
                "duration" : song.get("duration"),
                "title" : song.get("title"),
                "link" : song.get("link"),
                # will set it to true after being downloaded so we do not have 
                # to download a song two times if the user press previous
                "downloaded" : False,
            })
        self.__currentSong = self.songs[self.current_song_number]
        self.current_song_number += 1
        return self.__currentSong

    def play(self):
        """
        This does not require the music player to run on a different
        thread.
        """
        song_path =  self.path + "/" + self.get_next_song()["title"] + ".mp4"
        self.player.stop()
        song = vlc.media(song_path)
        self.player.set_media(song)
        self.player.play()


    def pause(self):
        """
        Pause or unpause the song. No effect if nothing is playinig
        """
        self.player.pause()


    def __get_playlist_info(self, playlist : str) -> list:
        """
        This function will return a list of song id from a playlist
        The ids will later be used in playMusic() function to play music
        """
        songlist = youtubesearchpython.Playlist(playlist)
        playlist = []
        for i in songlist.videos:
            playlist.append({
                "id" : i.get("id"),
                "duration" : i.get("duration"),
                "title" : i.get("title"),
                "link" : i.get("link"),
                # will set it to true after being downloaded so we do not have 
                # to download a song two times if the user press previous
                "downloaded" : False,
            })
        return playlist

    def __get_song_info(self, song_id : str) -> list:
        """
        Return the information of a song that later be stored in SongList object
        """
        video = youtubesearchpython.Video.get(song_id,
                mode = youtubesearchpython.ResultMode.dict)
        return [{
            "id" : video.get("id"),
            "duration" : video.get("duration"),
            "title" : video.get("title"),
            "link" : video.get("link"),
            # will set it to true after being downloaded so we do not have 
            # to download a song two times if the user press previous
            "downloaded" : False,
        }]

    
    def __del__(self):
        self.player.release()



    def download_song(self):
        # TODO : Help wanted make the download_song() function in a loop
        # with a thread safe mechanism
        path = self.path
        link = self.__currentSong["link"]
        title = self.__currentSong["title"]
        video_duration = self.__currentSong["duration"]
        downloaded = self.__currentSong["downloaded"]

        if downloaded:
            return None
        else:    
            # Checks For Is Song Of Suitable Length Or Not
            isVideoTooLongOrTooShort = (video_duration.count(":") != 1)
            isVideoShorterThan11Min = (int(video_duration.split(":")[0]) <= 11)

            if (not isVideoTooLongOrTooShort) and (isVideoShorterThan11Min):
                yt = pytube.YouTube(link)
                audio_stream = yt.streams.filter(only_audio=True)
                audio_stream[0].download(path, filename=f"{title}.mp4")
            else:
                # Trying Again if current song isn't suitable for Downloading and playing
                self.download_song()




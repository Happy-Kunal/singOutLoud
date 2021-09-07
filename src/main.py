# For Pseudo see ./"Pseudo Codes"/main.md

import os
import time
import multiprocessing
import youtubesearchpython
import pytube

import player

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
    
    # User Inputs i.e. latest released
    music_choice = input("Enter The Type Of Music/Song You Want To Listen :\t") + "song"

    process = multiprocessing.Process(target=playMusic, name="Music Player")
    process.start()
    
    try:
        while True:
            songlist = SongList(searchstr=music_choice)
            download_song(songlist, path = "./Downloads/")
            if not process.is_alive():
                break
    except KeyboardInterrupt:
        print("Exiting Process")
        process.terminate()
        exit(2)
        
    



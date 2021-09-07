# For Pseudo see ./"Pseudo Codes"/main.md

import os
import time
import multiprocessing
import youtubesearchpython
import pytube

import player
import dynamic_terminal

def download_song(songlist : player.SongList):
    path = songlist.path

    searchObject = songlist.searchObject
    currentsong = searchObject.result()["result"][0]
    link = currentsong["link"]
    title = currentsong["title"]
    video_id = currentsong["id"]
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
        songlist.searchObject = searchObject.next()
        download_song(songlist)
    
    songlist.songs.append({
        "id" : video_id,
        "duration" : video_duration,
        "title" : title,
        "link" : link
    })
    # updating music queue
    songlist.searchObject = searchObject.next()

if __name__ == "__main__":
    
    # User Inputs i.e. latest released
    music_choice = input("Enter The Type Of Music/Song You Want To Listen :\t") + "song"
    SongListObject = player.SongList(searchstr=music_choice)

    playMusicProcessObject = multiprocessing.Process(target=player.playMusic, name="musicPlayer", args=(SongListObject,))
    playMusicProcessObject.start()
    SongListObject.playMusicProcessObject = playMusicProcessObject
    
    dynamicTerminalProcessObject = multiprocessing.Process(target=dynamic_terminal.dynamic_terminal, name="dynamicTerminal", args=(SongListObject, playMusicProcessObject))
    dynamicTerminalProcessObject.start()

    try:
        while True:
            download_song(SongListObject)
            if not dynamicTerminalProcessObject.is_alive():
                break
    except KeyboardInterrupt:
        print("Exiting Process")
        dynamicTerminalProcessObject.terminate()
        exit(2)
    
    finally:
        SongListObject.playMusicProcessObject.terminate()
        

        
    



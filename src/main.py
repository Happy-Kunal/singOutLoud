# For Pseudo see ./"Pseudo Codes"/main.md

import time
import killAbleThread
import pytube

import player
import dynamic_terminal

def download_song(songlist : player.SongList):
    path = songlist.path

    searchObject = songlist.searchObject
    print(type(searchObject))
    currentsong = searchObject.result()["result"][0]
    link = currentsong["link"]
    title = currentsong["title"]
    video_duration = currentsong["duration"]

    # Checks For Is Song Of Suitable Length Or Not
    isVideoTooLongOrTooShort = (video_duration.count(":") != 1)
    isVideoShorterThan11Min = (int(video_duration.split(":")[0]) <= 11)

    if (not isVideoTooLongOrTooShort) and (isVideoShorterThan11Min):
        yt = pytube.YouTube(link)
        audio_stream = yt.streams.filter(only_audio=True)
        audio_stream[0].download(path, filename=f"{title}.mp4")
    else:
        # Trying Again if current song isn't suitable for Downloading and playing
        searchObject.next()
        download_song(songlist)
    
    songlist.songs.append({
        "duration" : video_duration,
        "title" : title,
        "link" : link
    })
    # updating music queue
    searchObject.next()

if __name__ == "__main__":
    
    # User Inputs i.e. latest released
    music_choice = input("Enter The Type Of Music/Song You Want To Listen :\t") + "song"
    SongListObject = player.SongList(searchstr=music_choice)

    playMusicThreadObject = killAbleThread.killAbleThread(target=player.playMusic, name="musicPlayer", args=(SongListObject,))
    playMusicThreadObject.start()
    SongListObject.playMusicThreadObject = playMusicThreadObject
    
    try:
        while True:
            download_song(SongListObject)
            if not SongListObject.playMusicThreadObject.is_alive():
                break
    except KeyboardInterrupt:
        print("Exiting Process, Please Wait ...")
        SongListObject.playMusicThreadObject.kill()
    
    finally:
        SongListObject.playMusicThreadObject.kill()
        

        
    



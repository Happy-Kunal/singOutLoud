# For Pseudo see ./"Pseudo Codes"/main.md

import os
import time
import playsound
import threading
import youtubesearchpython

# User Defined Modules
import menus


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

def download_song(searchObject : youtubesearchpython.VideosSearch, path : str = "./Downloads/", musicQueue : list = []):
    Downloading_str = "youtube-dl --ignore-errors -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 --no-progress -o "

    while (len(musicQueue) > 9):
        time.sleep(300)
    
    # getting song information from YT
    searchResult = searchObject.result()["result"][0]
    
    link = searchResult["link"]
    title = searchResult["title"]
    video_duration = searchResult["duration"]

    # Checks For Is Song Of Suitable Length Or Not
    isVideoTooLongOrTooShort = (video_duration.count(":") != 1)
    isVideoShorterThan11Min = (int(video_duration.split(":")[0]) <= 11)

    if (not isVideoTooLongOrTooShort) and (isVideoShorterThan11Min):
        # print(f"{Downloading_str} {path} {title}.mp3 {link}") # For Checking weather correct command is executing or not
        # Downloading Song
        os.system(f"{Downloading_str} {path}\"{title}.mp3\" {link} >/dev/null 2>/dev/null") #https://stackoverflow.com/questions/617182/how-can-i-suppress-all-output-from-a-command-using-bash
    else:
        # Trying Again if current song isn't suitable for Downloading and playing
        searchObject.next()
        download_song(searchObject, path)
    
    # updating music queue
    musicQueue.append(f"{path}{title}.mp3")
    searchObject.next() # making search object cursor on next song
    
    return (musicQueue, searchObject)


if __name__ == "__main__":
    musicQueue = [] # will store name of songs as soon as a song ends it will pop out the song before it (i.e. we will play song at index 1)

    # User Inputs i.e. latest released
    music_choice = input("Enter The Type Of Music/Song You Want To Listen :\t") + "song"
    searchObject = youtubesearchpython.VideosSearch(music_choice, limit = 1) # it will fetch a single song at a time with requested type

    thread = threading.Thread(target=playMusic, name="Music Player")
    thread.start()

    try:
        while True:
            musicQueue, searchObject = download_song(searchObject, path = "./Downloads/", musicQueue = musicQueue)
            if not thread.is_alive():
                break
    except KeyboardInterrupt:
        print("Exiting Process")
        thread._stop()
        exit(2)
        
    



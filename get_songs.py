# https://github.com/ytdl-org/youtube-dl#embedding-youtube-dl
# https://github.com/alexmercerind/youtube-search-python
# https://gist.github.com/umidjons/8a15ba3813039626553929458e3ad1fc

import os
import youtubesearchpython
Downloading_str = "youtube-dl --ignore-errors -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0  -o"

def search_and_download_song(searchString:str, path:str = "./Downloads/"):
    videosSearch = youtubesearchpython.VideosSearch(searchString, limit = 3).result() #searching for 3 videos on youtube

    for result in videosSearch["result"]:
        link = result["link"]
        title = result["title"]
        video_duration = result["duration"]

        isVideoTooLongOrTooShort = (video_duration.count(":") != 1)
        isVideoShorterThan11Min = (int(video_duration.split(":")[0]) <= 11)

        if (not isVideoTooLongOrTooShort) and (isVideoShorterThan11Min):
            print(f"{Downloading_str} {path} {title}.mp3 {link}") # For Checking weather correct command is exxecuting or not
            os.system(f"{Downloading_str} {path}\"{title}.mp3\" {link}")

if __name__ == "__main__":
    search_and_download_song("NoCopyrightSounds")

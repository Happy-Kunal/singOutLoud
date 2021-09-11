# For Pseudo see ./"Pseudo Codes"/main.md

import time
import pytube
import player

if __name__ == "__main__":    
    # TODO : integrate all the function run dynamicTerminal on mainthread and 
    # player on main thread and download_song on a different thread
    # User Inputs i.e. latest released
    music_choice = input("Enter The Type Of Music/Song You Want To Listen :\t") + "song"
    SongListObject = player.Player(searchstr=music_choice)

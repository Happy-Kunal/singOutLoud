#  CAUTION : DON'T MESS WITH IT UNLESS YOU KNOW WHAT YOU ARE DOING
# https://stackoverflow.com/questions/37498704/print-text-before-input-prompt-in-python#37499080

import sys
import readline # The readline module is imported so that editing and history are available at the input prompt
from time import sleep

from main import SongList
from threading import Thread

# Get the (current) number of lines in the terminal
import shutil
height = shutil.get_terminal_size().lines - 1

# Get write buffer so that we can print above our input prompt
stdout_write_bytes = sys.stdout.buffer.write


# Some ANSI/VT100 Terminal Control Escape Sequences
CSI = b'\x1b['
CLEAR = CSI + b'2J'
CLEAR_LINE = CSI + b'2K'
SAVE_CURSOR = CSI + b's'
UNSAVE_CURSOR = CSI + b'u'

GOTO_INPUT = CSI + b'%d;0H' % (height + 1)

def emit(*args):
    stdout_write_bytes(b''.join(args))

def set_scroll(n):
    return CSI + b'0;%dr' % n

def available_options_for_input(): # for printing menu
    print("[D]isplay [Q]ueue")
    print("[P]revious")
    print("[N]ext")
    print("[S]huffle")
    print("[RS] Repeat Single")
    print("[RQ] Repeat Queue")
    print("[H]elp")


emit(CLEAR, set_scroll(height))

def dynamic_terminal(SongListObject: SongList, playMusicThreadObject: Thread):
    try:
        while True:
            #Get input
            emit(SAVE_CURSOR, GOTO_INPUT, CLEAR_LINE)
            try:
                choice = int(input('Choice (type [H]elp for help): '))
                choice = choice.lower()
            except ValueError:
                continue
            finally:
                emit(UNSAVE_CURSOR)

            if choice in ("h", "help"):
                available_options_for_input()
            
            elif choice in ("d", "q", "queue", "display", "song", "songs", "music", "list", "music list", "song list"):
                for index, song in enumerate(SongListObject.songs):
                    print(f"{index + 1}. {song}")

            elif choice in ("p", "previous", "back"):
                playMusicThreadObject._stop()
                SongListObject.current_song_number -= 1
            
            elif choice in ("n", "next", "ahead"):
                pass
            
            elif choice in ("s", "shuffle", "party", "something else"):
                pass
            
            elif choice in ("rs", "single", "ro", "repeat one") :
                pass
            
            elif choice in ("rq", "rq", "repeat all", "repeat queue") :
                pass
            
            else:
                print("Sorry, But, Enter A Valid Choice")



    except KeyboardInterrupt:
        #Disable scrolling, but leave cursor below the input row
        emit(set_scroll(0), GOTO_INPUT, b'\n')

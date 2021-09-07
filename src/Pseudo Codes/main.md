# Pseudo Code For main.py
## Older Downwards
---
***6 September 2021***
```
1. download_song() will run on another thread iff user want it (i.e. Having Slow internet speed for live streaming)
2. playMusic() will run on another thread
    - playmusic will show menu
    - user input will we availabe at bottom
    - user input will make script peroform requested feature
```

---
***5 September 2021***
```
Q- How Will Code Work ???
A- we will gonna make a global youtubesearchpython.VideoSearch object with our search string
and call function download_song() which will download songs and keep 3 
songs in a upcoming queue so to fight delay due to buffering and at the and function will call
youtubesearchpython.VideoSearch().next() so that we can get a list of next 3 songs as soon as
user Reaches the end of queue we will download 3 more songs and enqueue them too.

Pseudo Code:
    1. make a global youtubesearchpython.VideoSearch object with our search string
    2. call function download_song() which will download songs
    3. make queue and add songs to it
    4. make thread to play songs
    5. At End Of of download_song() update new list of songs
    6. Download Songs if there are less than 2 songs in queue # Currently found no need but left if change mind in future
```

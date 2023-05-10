import pyautogui
import pyperclip
import time
import soundcard as sc
import soundfile as sf
import os.path
import sys
import os
import pydub
import ffmpeg
import eyed3
from termcolor import colored
import keyboard

def emergency_exit():
    # Your emergency exit code here
    print("Emergency exit activated! Any songs in progress will not be saved!")
    time.sleep(3)
    os._exit(0)
   
keyboard.add_hotkey('esc', emergency_exit) #keyoard listener

conf_path = os.getcwd()
sys.path.append(conf_path)
sys.path.append(conf_path + '\scripts\Setup') 
def MusicRipper(PlaylistLength, WhichPlaylist, PlaylistGenre):
    PlaylistPath= "D:/Coding Projects/Personal Projects/MusicMachine/Music For The Big One/"+WhichPlaylist+"/"
    #Save all songs currently in playlist in an array for skipping if duplicates
    songsInPlaylist = []
    for file_name in os.listdir(PlaylistPath):
        song = os.path.join(PlaylistPath, file_name)
        song = eyed3.load(song)
        songsInPlaylist.append(song)

    s = 0
    print("Launch In Album Mode? (y/n)")
    getAlbumMode = input()
    if getAlbumMode == 'y':
        albumMode = True
    else:
        albumMode = False
    print("Launch in background mode? (y/n)")
    getBackMode = input()
    if getBackMode == 'y':
        gameMode = True
    else:
        gameMode = False
    restartFlag = False
    for i in range(PlaylistLength):
        if gameMode == True and restartFlag != True:
            pyautogui.hotkey('alt','tab')
        if restartFlag == True:
            restartFlag = False
        s = s + 1
        time.sleep(3)
        pyautogui.moveTo(254,2034)
        for i in range(3):
            pyautogui.click()
        time.sleep(2)
        pyautogui.hotkey('ctrl','c')

        try:
            song_length = pyperclip.paste().split("/ ")[-1]
            tmp1 = song_length.split(":")[0]
            tmp2 = song_length.split(":")[1].strip("\r\n")
        except:
            pyautogui.moveTo(254,2034)
            for i in range(3):
                pyautogui.click()
            time.sleep(2)
            pyautogui.hotkey('ctrl','c')
            song_length = pyperclip.paste().split("/ ")[-1]
            tmp1 = song_length.split(":")[0]
            tmp2 = song_length.split(":")[1].strip("\r\n")
        
        tmp1 =  int(tmp1) * 60
        tmp2 = int(tmp2)
        song_length_seconds = tmp1+tmp2-1
        #print(song_length_seconds)

        pyautogui.moveTo(450,2034)
        pyautogui.click()


        #print(song_length)

        pyautogui.hotkey('f12')
        time.sleep(2)
        pyautogui.moveTo(3771,1325)
        pyautogui.click()
        pyautogui.hotkey('ctrl','shift','c')
        time.sleep(1)
        pyautogui.moveTo(1422,2020)
        pyautogui.drag(10,0, button= 'left')
        time.sleep(1)
        #pyautogui.click()
        #time.sleep(3)
        pyautogui.moveTo(3208,1594)
        time.sleep(1)

        pyautogui.click()

        pyautogui.moveTo(3021,1680)
        time.sleep(1)
        pyautogui.mouseDown(button='left')
        pyautogui.moveTo(3805,1680)
        pyautogui.hotkey('ctrl','c')
        time.sleep(1)
        pyautogui.mouseUp(button='left')

        try:
            Artist_Album_Year = pyperclip.paste().split("generic ")[-1]
            Artist = Artist_Album_Year.split(" • ")[0].strip('"')
            Album = Artist_Album_Year.split(" • ")[1].strip('"')
            Year = Artist_Album_Year.split(" • ")[2].strip('"')
        except:
            try:
                Artist_Album_Year = pyperclip.paste().split("generic ")[-1]
                Artist = Artist_Album_Year.split(" • ")[0].strip('"') 
                Album = Artist_Album_Year.split(" • ")[1].strip('"')
                Year = 9999
            except:
                Artist_Album_Year = pyperclip.paste().split("generic ")[-1]
                Artist = Artist_Album_Year.split(" • ")[0].strip('"')
                Album = "Exception"
                Year = 9999
    #ln 67 error catch Index Error when Title,Album,Year is too long
        pyautogui.moveTo(3202,1593)
        pyautogui.click()
        pyautogui.moveTo(3021,1618)
        time.sleep(1)
        pyautogui.mouseDown(button='left')
        pyautogui.moveTo(3805,1618)
        pyautogui.hotkey('ctrl','c')
        time.sleep(1)
        pyautogui.mouseUp(button='left')

        Song_Name = pyperclip.paste().split("generic ")[-1].strip('"')
        #print(Artist_Album_Year)
        #print(Song_Name)

        class Song:
            def __init__(self, title, artist, album, length, year):
                self.title = title
                self.artist = artist
                self.album = album
                self.length = length
                self.year = year
                
                

        # Create instances of the Song class
        song1 = Song(Song_Name, Artist, Album, song_length, Year)

        songs = {song1}
        for song in songs:
            print("Song #: ", s)
            print("Title:", song.title)
            print("Artist:", song.artist)
            print("Album:", song.album)
            print("Length:", song.length.strip("\r\n"))
            print("Year:", song.year, "\n")
            
        #if song is already in playlist skip and return to begining of function
        for oldSong in songsInPlaylist:
            if Song_Name == oldSong.tag.title and Artist == oldSong.tag.artist:
                pyautogui.moveTo(201,2035)
                pyautogui.click()
                restartFlag = True
                break
            
        #restarts loop skipping song
        if restartFlag == True:
            pyautogui.hotkey('f12')
            continue
        #restart song to get full recording
        pyautogui.hotkey('f12')
        pyautogui.moveTo(0,1987)
        pyautogui.click()
        
        #Display Running Environment
        pyautogui.hotkey('alt','tab')
        
        from pydub import AudioSegment
        OUTPUT_FILE_NAME = os.path.join(PlaylistPath, Song_Name+".wav")    # file name.
        SAMPLE_RATE = 48000              # [Hz]. sampling rate.
        RECORD_SEC = song_length_seconds                  # [sec]. duration recording audio.
        
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
            # record audio with loopback from default speaker.
            data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)
            
            try:
                # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
                sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)
                #song name must not include special chars, create try catch
            except:
                ExceptionName = os.path.join(PlaylistPath, str(s)+".wav")
                OUTPUT_FILE_NAME = ExceptionName
                sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)
        
        temp = OUTPUT_FILE_NAME.strip(".wav")    
        temp = temp + ".mp3"        
        AudioSegment.from_wav(OUTPUT_FILE_NAME).export(temp, format="mp3")
        temp = eyed3.load(temp)  
        temp.tag.artist = Artist
        temp.tag.album = Album
        temp.tag.title = Song_Name
        try:
            temp.tag.recording_date = str(Year)
        except:
           temp.tag.recording_date = "" 
        temp.tag.album_artist = Artist
        temp.tag.genre = PlaylistGenre
        if albumMode == True:
            temp.tag.track_num = s
        temp.tag.save()        
        os.remove(OUTPUT_FILE_NAME) 



a =print(colored("   _____                 .__            _____                   .__     .__                  ____   ____ ____ ", "yellow"))  
b =print(colored("  /     \   __ __  ______|__|  ____    /     \  _____     ____  |  |__  |__|  ____    ____   \   \ /   //_   |", "yellow"))  
c =print(colored(" /  \ /  \ |  |  \/  ___/|  |_/ ___\  /  \ /  \ \__  \  _/ ___\ |  |  \ |  | /    \ _/ __ \   \   Y   /  |   |", "yellow"))  
d =print(colored("/    Y    \|  |  /\___ \ |  |\  \___ /    Y    \ / __ \_\  \___ |   Y  \|  ||   |  \\  ___/     \     /   |   |", "yellow"))  
e =print(colored("\____|__  /|____//____  >|__| \___  >\____|__  /(____  / \___  >|___|  /|__||___|  / \___  >    \___/ /\ |___|", "yellow"))  
f =print(colored("        \/            \/          \/         \/      \/      \/      \/          \/      \/           \/      ", "yellow"))  

g =print(colored("===============================================================================================================\n", "magenta"))  


Welcome_Prompt = "Please Enter: The Number Of Songs, the Name of the Playlist on this Computer, and the Genre: x,y,z\nPress 'esc' to terminate program"        
underlined_text = "\033[4m" + Welcome_Prompt + "\033[0m"
print(colored(underlined_text, "yellow"))
inputPrompt = input()
numOfSongs = int(inputPrompt.split(",")[0])
Playlist = inputPrompt.split(",")[1]
Genre = inputPrompt.split(",")[-1]
MusicRipper(numOfSongs,Playlist, Genre)

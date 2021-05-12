import subprocess
import os

def filesInput() -> tuple:
    '''User interaction with the program. Returns a tuple of the inputs
        provided from the user. '''
    videoInput  = input("Input the YouTube link or name of your video: ")
    audioFile   = input("Input the name of your audio file: ")
    audioFormat = input("Input the format of the audio file (default: mp3): ")

    return videoInput, audioFile + validateFormat(audioFormat)


def overwrite(videoInput: str, audioFile: str):
    print("\nWARNING: ")
    print("This file is already in the directory and will be overwritten!")
    response = None
    
    while response != 'yes' and response != 'no':
        response = input("Type 'yes' or 'no' to proceed: ").lower()

        if response == 'yes': return True
        
        elif response == 'no': return False


def avoidOverWriting(videoInput: str, audioFile: str):
    ''' If the audio file isnt in the directory, returns False as overwriting
        is then determined impossible. Otherwise, validates if the user
        is fine with the file being overwritten. If not, returns True. '''
    if directoryContains(audioFile):
        if overwrite(videoInput, audioFile):
            os.remove(audioFile) # If overwrite is True, remove the audioFile and continue the script

        else:
            return True

    return False


def directoryContains(audioFile: str) -> bool:
    ''' Returns True or False if the file is already in the directory to avoid overwriting.'''
    return audioFile in os.listdir()


def validateFormat(audioFormat: str):
    ''' Returns the audio format along with the '.', but the format must be
        within the recommended list. Otherwise will return the default format
        which is mp3. '''
    if audioFormat in ['mp3', 'wav', 'flac']:
        return '.' + audioFormat

    return '.mp3' # default format is mp3 if inproper input


def youtubeLink(videoInput: str) -> bool:
    ''' Returns True if the input was from YouTube or False otherwise. '''
    return 'youtube' in videoInput


def youtubeDownload(user_link: str, audioFile) -> None:
    ''' Downloads the video from YouTube if the user inputted a YouTube link. '''
    print('Downloading...')
    try:
        command = f"youtube-dl -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 {user_link}"
        subprocess.call(command, shell=True)
        videoInput = max(os.listdir(), key=os.path.getctime)
        os.rename(videoInput, audioFile)

    except os.error:
        print('Invalid characters used for File name. YouTube title is now File name.')
    
    print('Done Downloading..')

def convertVideo(videoInput: str, audioFile: str) -> None:
    print('Starting to Convert...')
    
    command = f"ffmpeg -i {videoInput}.mp4 -ab 160k -ac 2 -ar 44100 -vn {audioFile}"
    subprocess.call(command, shell=True)

    print('DONE')

    

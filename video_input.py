import subprocess
import os

def directoryContains(audioFile: str) -> bool:
    ''' Returns True or False if the file is already in the directory to avoid overwriting.'''
    return audioFile in os.listdir()


def overwrite(videoInput: str, audioFile: str):
    print("\nWARNING: ")
    print("This file is already in the directory and will be overwritten!")

    while True:
        response = input("Type 'yes' or 'no' to proceed: ").lower()

        if response == 'yes':
            os.remove(audioFile)
            convertVideo(videoInput, audioFile)
            return
        
        elif response == 'no':
            return

        continue

def convertVideo(videoInput: str, audioFile: str) -> None:
    print('Starting to Convert...')

    command = f"ffmpeg -i {videoInput} -ab 160k -ac 2 -ar 44100 -vn {audioFile}"
    subprocess.call(command, shell=True)

    print('DONE')

def validateFormat(audioFormat: str):

    if audioFormat in ['mp3', 'wav', 'flac']:
        return '.' + audioFormat

    return '.mp3' # default format is mp3 if inproper input

def filesInput() -> tuple:
    videoInput  = input("Input the link to your video file: ")
    audioFile   = input("Input the name of your audio file: ")
    audioFormat = input("Input the format of the audio file (default: mp3): ")

    return videoInput, audioFile + validateFormat(audioFormat)


def main():
    videoInput, audioFile = filesInput()
    
    if directoryContains(audioFile):
        overwrite(videoInput, audioFile)

    else:
        convertVideo(videoInput, audioFile)

if __name__ == '__main__':
    main()
    

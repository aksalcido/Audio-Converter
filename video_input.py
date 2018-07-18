import subprocess
import os


def directoryContains(audioFile: str) -> bool:
    ''' Returns True or False if the file is already in the directory to avoid overwriting.'''
    return audioFile in os.listdir()


def convertVideo(videoInput: str, audioFile: str) -> None:
    print('Starting to Convert...')
    
    command = f"ffmpeg -i {videoInput} -ab 160k -ac 2 -ar 44100 -vn {audioFile}"
    subprocess.call(command, shell=True)

    print('DONE')


def overwrite(videoInput: str, audioFile: str):
    print("\nWARNING: ")
    print("This file is already in the directory and will be overwritten!")
    response = None

    while True:
        response = input("Type 'yes' or 'no' to proceed: ").lower()

        if response == 'yes':
            os.remove(audioFile)
            convertVideo(videoInput, audioFile)
            return
        
        elif response == 'no':
            return

        continue


def main():
    videoInput = input("Input the link to your video file: ")
    audioFile  = input("Input the name of your audio file: ")


    if directoryContains(audioFile):
        overwrite(videoInput, audioFile)

    else:
        convertVideo(videoInput, audioFile)




if __name__ == '__main__':
    main()
    

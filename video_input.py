import subprocess
import os


def directoryContains(videoFile: str) -> bool:
    ''' Returns True or False if the file is already in the directory to avoid overwriting.'''
    return videoFile in os.listdir()


def convertVideo(fileInput: str, videoFile: str) -> None:
    print('Starting to Convert...')
    
    command = f"ffmpeg -i {fileInput} -ab 160k -ac 2 -ar 44100 -vn {videoFile}"
    subprocess.call(command, shell=True)

    print('DONE')


def overwrite(fileInput: str, videoFile: str):
    print("\nWARNING: ")
    print("This file is already in the directory and will be overwritten!")
    response = None

    while True:
        response = input("Type 'yes' or 'no' to proceed: ").lower()

        if response == 'yes':
            os.remove(videoFile)
            convertVideo(fileInput, videoFile)
            return
        
        elif response == 'no':
            return

        continue


def main():
    fileInput = input("Input the link to your video file: ")
    videoFile = input("Input the name of your audio file: ")


    if directoryContains(videoFile):
        overwrite(fileInput, videoFile)

    else:
        convertVideo(fileInput, videoFile)




if __name__ == '__main__':
    main()
    

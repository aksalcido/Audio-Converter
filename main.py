import audio_extractor as audio

def main():
    videoInput, audioFile = audio.filesInput()

    # Automatically Ends the Program if the User doesn't want to Overwrite
    if audio.avoidOverWriting(videoInput, audioFile):
        return

    else:
        # YouTube links are handled different as requires a download
        if audio.youtubeLink(videoInput):
            audio.youtubeDownload(videoInput, audioFile)

        # Handles the videos that are already in the directory
        else:
            audio.convertVideo(videoInput, audioFile)


if __name__ == '__main__':
    main()

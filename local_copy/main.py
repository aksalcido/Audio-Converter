import audio_extractor as audio_extract

def main():
    videoInput, audioFile = audio_extract.filesInput()

    # Automatically Ends the Program if the User doesn't want to Overwrite
    if audio_extract.avoidOverWriting(videoInput, audioFile):
        return

    else:
        # YouTube links are handled different as requires a download
        if audio_extract.youtubeLink(videoInput):
            audio_extract.youtubeDownload(videoInput, audioFile)

        # Handles the videos that are already in the directory
        else:
            audio_extract.convertVideo(videoInput, audioFile)


if __name__ == '__main__':
    main()

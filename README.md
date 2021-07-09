# remove-silence
removes portions of silence from audio files

REQUIREMENTS:
  - python 3.x
  - pydub module: https://pypi.org/project/pydub/

USE:
  - step 1: select the audio file to remove periods of silence from (only .wav and .mp3 files are currently accepted!)
  - step 2: input minimum silence length in millseconds (for example "500" will ignore all periods of silence shorter than 500 milliseconds)
  - step 3: input silence threshold in decibels (reccomended value is "-40", however if there is a lot of background noise you may try raising it. feel free to use what works best for you!)

NOTE: the longer tha audio file, the more time it will take! However I have used this to process audio files over 1 hour and it works perfectly for me

#https://towardsdatascience.com/the-easiest-way-to-download-youtube-videos-using-python-2640958318ab
from pytube import YouTube

# https://www.reddit.com/r/learnpython/comments/ey41dp/merging_video_and_audio_using_ffmpegpython/

# Misc
import os
import subprocess
import shutil
import math
import datetime
import ffmpeg

# Plots
import matplotlib.pyplot as plt
# %matplotlib inline

# Image Operation
import cv2

# This removes invalid characters from filenames
# Invalid Windows Characters are: \/:*?"<>|
# Example Command: remove(filename, '\/:*?"<>|')
def remove(value, deletechars):
    for c in deletechars:
        value = value.replace(c,'')
    return value;

url = input("Please enter the URL of the video you would like to download:\n")

video = YouTube(url)

path = os.getcwd()
newFolderPath = path + "\\" + remove(video.title, "'\\/:*?\"<>|")

try:
    os.mkdir(newFolderPath)
except OSError:
    print("Creation of directory %s failed" % newFolderPath)

#print(video.length)
#print(video.rating)
#print(video.views)
#print(video.streams)

# For the 4k Webm one, use itag = 313
# For the 1080p MP4 one, use itag = 137
# To check which is right, use the print(video.streams) and look for the res
# property and see what res you want and then check the itag for that one
# Or  you could do .streams.order_by("resolution").desc().first().download() to auto
# get the highest resolution video regardless of format
# video.streams.get_by_itag(137).download()
# print(video.streams.order_by("resolution").desc().first())
# print(video.streams.filter(only_audio=True).order_by("abr").desc().first())

videoName = remove(video.title, "'\\/:*?\"<>|.") + " Video"
video.streams.order_by("resolution").desc().first().download(filename=videoName, output_path=newFolderPath)

audioName = remove(video.title, "'\\/:*?\"<>|.") + " Audio"
video.streams.filter(only_audio=True).order_by("abr").desc().first().download(filename=audioName, output_path=newFolderPath)

#videoPath = '"' + newFolderPath + "\\" + videoName + '"'
#audioPath = '"' + newFolderPath + "\\" + audioName + '"'
videoPath = ''
audioPath = ''

# https://stackoverflow.com/questions/5899497/how-can-i-check-the-extension-of-a-file
# https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
directory = os.fsencode(newFolderPath)
    
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if os.path.splitext(filename)[0] == videoName:
         videoPath += os.path.join(os.fsdecode(directory), filename)
         continue
     elif os.path.splitext(filename)[0] == audioName:
         audioPath += os.path.join(os.fsdecode(directory), filename)
         continue

outputType = input("What format would you like the audio + video to be in? (1 for mkv (Default If Blank) or 2 for mp4 (Experimental)):\n")

#cmd = ""

#videoIn = ffmpeg.input(r"C:\Users\Ayden\Desktop\Python Programs\Youtube Downloader\Downtown Calgary - 4K AERIAL TOUR\Downtown Calgary - 4K AERIAL TOUR Video.webm")
#audioIn = ffmpeg.input(r"C:\Users\Ayden\Desktop\Python Programs\Youtube Downloader\Downtown Calgary - 4K AERIAL TOUR\Downtown Calgary - 4K AERIAL TOUR Audio.webm")

videoIn = ffmpeg.input(videoPath)
audioIn = ffmpeg.input(audioPath)

if outputType == "2":
    # MP4
    #cmd = "ffmpeg -y -i " + audioPath + " -r 30 -i " + videoPath + " -filter:a aresample=async=1 -strict -2 -c:a flac -c:v copy " + '"' + newFolderPath + "\\" + remove(video.title, '\/:*?"<>|') + " Combined.mp4" + '"'
    mergedVideo = ffmpeg.output(videoIn, audioIn, newFolderPath + "\\" + remove(video.title, '\/:*?"<>|.') + " Combined.mp4", vcodec="copy", acodec="flac", strict="experimental")
    try:
        mergedVideo.run(capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
        raise e
else:
    # mkv
    # This is the default as ffmpeg says it is more stable than mp4
    #cmd = "ffmpeg -y -i " + audioPath + " -r 30 -i " + videoPath + " -filter:a aresample=async=1 -c:a flac -c:v copy " + '"' + newFolderPath + "\\" +  remove(video.title, '\/:*?"<>|') + " Combined.mkv" + '"'
    mergedVideo = ffmpeg.output(videoIn, audioIn, newFolderPath + "\\" + remove(video.title, '\/:*?"<>|.') + " Combined.mkv", vcodec="copy", acodec="flac")
    try:
        mergedVideo.run(capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
        raise e

#subprocess.call(cmd, shell=True)

print("Your video can be found at %s" % newFolderPath)
input("To End, Press Enter")

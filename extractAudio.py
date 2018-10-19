import os
from util import get_video_start
import subprocess
import shlex


def createFFmpegCommandFullExtraction(videoPath, outPath,start, sampleRate, numChannels, bitrate):
    return "ffmpeg -i '{}' -ss 00:00:0{} -ab {}k -ac {} -ar {} -vn '{}'".format(videoPath, start, bitrate, numChannels,
                                                                           sampleRate, outPath)

def call_proc(cmd, jobnum, jobcount):
    """ This runs in a separate thread. """
    #subprocess.call(shlex.split(cmd))  # This will block until cmd finishes
    print ("Extracting audio {}/{} \n Command : {}".format(jobnum, jobcount,cmd))
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return (out, err)


# duration in seconds
def createFullAudioClips(videoFiles, videoFilesPath, outPath, sampleRate=48000, numChannels=1, bitrate=128):

    videoFilePaths = [os.path.join(videoFilesPath, fileName) for fileName in videoFiles]
    for i, (videoFile, videoFilePath) in enumerate(zip(videoFiles, videoFilePaths)):
        audioFileName = videoFile.split(".")[:-1][0] + ".wav"
        audioFilePath = os.path.join(outPath, audioFileName)
        if os.path.exists(audioFilePath):
            # print("SKIPPED : {} alrady exists". format(audioFileName))
            continue

        start = get_video_start(videoFilePath)
        command = createFFmpegCommandFullExtraction(videoFilePath, audioFilePath,start, sampleRate, numChannels, bitrate)
        out, err =call_proc(command, i, len(videoFilePaths))
        print (err)

    print("Finished extraction")



if __name__ =="__main__":
    HAP_DIR = "/home/nuc/Documents/dataStore/VIDEO/hap"
    FULL_AUDIO_DIR = "/home/nuc/Documents/dataStore/AUDIO"

    createFullAudioClips(os.listdir(HAP_DIR),HAP_DIR, FULL_AUDIO_DIR)
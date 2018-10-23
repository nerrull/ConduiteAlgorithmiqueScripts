import os
import subprocess
from util import get_video_start
from os.path import basename
from convertToHAP import convert_resize

known_files = [
    "VIRB_0280_000004.mp4",
    "VIRB_0280_000030.mp4",
    "VIRB_0280_000053.mp4",
    "VIRB_0280_000138.mp4",
    "VIRB_0280_000212.mp4",
    "VIRB_0280_000242.mp4",
    "VIRB_0280_000320.mp4",
    "VIRB_0280_000354.mp4"
]


def find_oversize(dir):
    files = [file for file in os.listdir(dir) if file.endswith(".mp4")]
    numfiles =len(files)
    filelist = []
    for i,file in enumerate(files):
        # print ("Checking file {} - {}/{}".format( file, i+1, numfiles))
        filename = file.split('.')[0]
        infile = os.path.join(dir, file)

        check_cmd = "ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {}".format(infile)

        output = subprocess.Popen(check_cmd,
                                  shell=True,
                                  stdout=subprocess.PIPE
                                  ).stdout.read().decode("utf-8")
        if "1920" not in output:
            print ("Found file {} - {}/{}".format(file, i + 1, numfiles))
            # print (output)
            filelist.append(file)

        if (i %100) ==0:
            print ("Progress {}/{}".format(i+1, numfiles))

    return filelist

def reencode_oversize(dir,files):
    numfiles = len(files)
    for i, file in enumerate(files):
        print ("Checking file {} - {}/{}".format(file, i + 1, numfiles))
        filename = file.split('.')[0]
        infile = os.path.join(dir, file)
        # outfile = os.path.join(dir, filename + "_resize.mp4")
        outfile = os.path.join(dir, 'hap', filename + '.mov')
        convert_resize(infile, outfile)


if __name__ =="__main__":
    VIDEO_DIR = "/home/nuc/Documents/dataStore/VIDEO"
    files = find_oversize(VIDEO_DIR)
    print(files)
    reencode_oversize(VIDEO_DIR,files)
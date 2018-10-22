import os
import subprocess
from util import get_video_start


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

dir = VIDEO_DIR

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
                                  ).stdout.read()
        if "1920" not in output:
            print ("Found file {} - {}/{}".format(file, i + 1, numfiles))
            # print (output)
            filelist.append(basename(filename))

        if (i %100) ==0:
            print ("Progress {}/{}").format(i+1, numfiles)

    return filelist

def reencode_oversize(files):
    numfiles = len(files)
    for i, file in enumerate(files):
        print ("Checking file {} - {}/{}".format(file, i + 1, numfiles))
        filename = file.split('.')[0]
        infile = os.path.join(dir, file)
        # outfile = os.path.join(dir, filename + "_resize.mp4")
        outfile = os.path.join(dir, 'hap', filename + '.mov')

        start = get_video_start(infile)

        resize_cmd = "ffmpeg -y -i {} -vf scale=w=1920:h=1080 -ss 00:00:0{} -c:v hap  -c:a aac -strict -2 -async 1 {}   ".format(
            infile, start, outfile)

        subprocess.call(resize_cmd, shell=True)


if __name__ =="__main__":
    VIDEO_DIR = "/home/nuc/Documents/dataStore/VIDEO"
    files = find_oversize(VIDEO_DIR)
    reencode_oversize(files)
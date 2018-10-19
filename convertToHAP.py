import os
import subprocess
from util import get_video_start
from decimal import *
dir = "/home/nuc/Documents/dataStore/VIDEO"

files = [file for file in os.listdir(dir) if file.upper().endswith(".MP4")]
numfiles =len(files)
for i,file in enumerate(files):
    filename = file.split('.')[0]
    infile = os.path.join(dir, file)
    outfile = os.path.join(dir, 'hap', filename + '.mov')
    if os.path.exists(outfile):
        continue

    print ("Encoding file {} - {}/{}".format( file, i+1, numfiles))
    start = get_video_start(infile)
    split_cmd = "ffmpeg -i {}  -ss 00:00:0{} -c:v hap  -c:a aac -strict -2 -async 1 {}   ".format(infile,Decimal(start),  outfile)
    subprocess.call(split_cmd, shell=True)

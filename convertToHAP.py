import os
import subprocess
import re
start_regexp = '..start: (\d{1}).(\d+),'
re_start = re.compile(start_regexp)
start_neg_regexp = '..start: -(\d{1}).(\d+),'
re_neg_start = re.compile(start_neg_regexp)

def get_video_start(filename ):
    command = "ffmpeg -i '" + filename + "' 2>&1 | grep 'start'"
    output = subprocess.Popen(command,
                              shell=True,
                              stdout=subprocess.PIPE
                              ).stdout.read().decode('utf-8')
    print ("Output: {}".format(output))
    matches = re_start.search(output)
    video_start =0
    if matches !=None:
        video_start = int(matches.group(1)) + int(matches.group(2))/1000000.
        print ("Video start in seconds: "+str(video_start))

    else:
        matches = re_neg_start.search(output)
        if matches != None:
            video_start = int(matches.group(1)) + int(matches.group(2)) / 1000000.
            print ("Video start in seconds: " + str(video_start))

    return video_start



dir = "/home/nuc/Documents/dataStore/VIDEO"

files = [file for file in os.listdir(dir) if file.endswith(".mp4")]
numfiles =len(files)
for i,file in enumerate(files):
    print ("Encoding file {} - {}/{}".format( file, i+1, numfiles))
    filename = file.split('.')[0]
    infile = os.path.join(dir, file)
    outfile = os.path.join(dir, 'hap', filename + '.mov')
    if os.path.exists(outfile):
        continue

    start = get_video_start(infile)
    split_cmd = "ffmpeg -i {}  -ss 00:00:0{} -c:v hap  -c:a aac -strict -2 -async 1 {}   ".format(infile,start,  outfile)
    subprocess.call(split_cmd, shell=True)

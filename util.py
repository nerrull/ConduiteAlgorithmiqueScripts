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
                              ).stdout.read().decode("utf-8")
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
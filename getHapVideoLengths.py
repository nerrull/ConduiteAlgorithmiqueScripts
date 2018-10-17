from os.path import join
import subprocess
import h5py as h5
from utils.defs import DATA_STORE, HAP_DIR, VIDEO_DIR
import numpy as np
db_path = join(DATA_STORE, "database.h5")

# HAP_DIR = ""
outfile = "./durations.txt"


def get_all_clip_durations(fileNames):
    durations = []
    with open(outfile, mode='w') as f:
        for name in fileNames:
            filePath = join(HAP_DIR, name + ".mov")
            command = "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {}".format(filePath)
            l = subprocess.check_output(command, shell=True)
            f.write(l)
            length = float(l)
            durations.append(length)
            print("Video {}/{} - length {}".format(i, len(fileNames), length))
        return durations

if __name__ =="__main__":
    with h5.File(db_path, mode='r') as f:
        video_names = f.get("video_names").value
        d =get_all_clip_durations(video_names)

    with h5.File(db_path, mode='a') as f:
        durations = np.array(d, dtype= np.float32)
        dset = f.create_dataset("video_durations", durations.shape, dtype=np.float32, data=durations)

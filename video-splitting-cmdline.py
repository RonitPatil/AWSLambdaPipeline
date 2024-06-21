#__copyright__   = "Copyright 2024, VISA Lab"
#__license__     = "MIT"

import os
import subprocess
import math


def video_splitting_cmdline(self, video_filename):
    filename = os.path.basename(video_filename)
    outfile = os.path.splitext(filename)[0] + ".jpg"
    ffmpeg_path = '/opt/bin/ffmpeg'

    # Updated split command to use the ffmpeg_path variable
    split_cmd = ffmpeg_path + ' -ss 0 -r 1 -i ' + video_filename + ' -vf fps=1/10 -start_number 0 -vframes 10 ' + outfile + "/" + 'output-%02d.jpg -y'
    
    try:
        subprocess.check_call(split_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.returncode)
        print(e.output)

    fps_cmd = 'ffmpeg -i ' + video_filename + ' 2>&1 | sed -n "s/.*, \\(.*\\) fp.*/\\1/p"'
    fps = subprocess.check_output(fps_cmd, shell=True).decode("utf-8").rstrip("\n")
    return outfile
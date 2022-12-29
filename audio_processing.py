# -*- coding: utf-8 -*-
"""
    File: audio_processing.py
    Author: Pablo Alfaro Saracho
    Description: Functions to process audio files
"""

import os
import subprocess
from scipy import signal
import numpy as np

def generate_wav(audio_file,folder,mono):
    audio_file_wav = '.'.join([os.path.splitext(audio_file)[0],"wav"])
    audio_file_wav = os.path.join(folder,os.path.basename(audio_file_wav))
    if mono:
        subprocess.call('ffmpeg -y -i '+'\"'+audio_file+'\"'+' -ac 1 '+'\"'+audio_file_wav+'\"', shell = True)
    else:
        subprocess.call('ffmpeg -y -i '+'\"'+audio_file+'\"'+' '+'\"'+audio_file_wav+'\"', shell = True)
    return audio_file_wav

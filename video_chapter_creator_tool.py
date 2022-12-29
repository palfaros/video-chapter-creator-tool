# -*- coding: utf-8 -*-
"""
    File: video_chapter_creator_tool.py
    Author: Pablo Alfaro Saracho
    Description: Tool to generate mkmerge compatible XML chapter file from video
"""

#%% LIBRARIES
import argparse
import os
import sys
from utils import header
from time_processing import convert_seconds_to_hh_mm_ss
from audio_processing import generate_wav
from video_processing import get_video_frame_rate, get_black_frames_from_video, silence_finder_from_black_frames
import numpy as np
import soundfile as sf
from chapter_processing import generate_chapter_file, get_chapter_info

#%% INPUT ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument('-v','--video-file', type=str, required=True)
parser.add_argument('-a','--audio-file', type=str, required=True)
parser.add_argument('-f','--framerate', nargs=2)
args = parser.parse_args()

video_file = args.video_file
audio_file = args.audio_file
fps = args.framerate

logs_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)),'logs')
os.makedirs(logs_folder,mode=0o777,exist_ok=True)
log_file = '.'.join([os.path.splitext(os.path.basename(video_file))[0],"txt"]) # It is like os.path.splitext(file_target)[0] + ".txt" but consuming less memory
log_file = os.path.join(logs_folder,log_file)
if os.path.exists(log_file):
    os.remove(log_file)

#%% DEFINE LOGGER
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open(log_file, "a")
   
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        
    def close(self):
        self.terminal = 0
        self.log.close()

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass    

orig_stdout = sys.stdout
sys.stdout = Logger()

print(header("ARGUMENTS"))
print ('Number of arguments:', len(vars(args)), 'arguments')
print ('Argument List:')
for input_argument in vars(args):
    print (input_argument,"-", getattr(args, input_argument))
    
print()

#%% VIDEO PROCESSING
print(header("VIDEO PROCESSING"))

video_frame_rate = get_video_frame_rate(video_file)
print('Video Frame Rate (FPS):',video_frame_rate)
print()

black_frames,is_black_frame = get_black_frames_from_video(video_file)
indexes_consecutive_black_frames,mean_indexes_black_frames = silence_finder_from_black_frames(is_black_frame)

indexes_consecutive_black_frames_seconds = (np.array(indexes_consecutive_black_frames)/video_frame_rate)
mean_indexes_black_frames_seconds = (np.array(mean_indexes_black_frames)/video_frame_rate)

count=0
for i,j in zip(indexes_consecutive_black_frames_seconds,mean_indexes_black_frames_seconds):
    count += 1
    print('Black frames sequence',count,'found in',convert_seconds_to_hh_mm_ss(i[0]),'-',convert_seconds_to_hh_mm_ss(i[1]),'Middle frame is',convert_seconds_to_hh_mm_ss(j))

print()

#%% AUDIO PROCESSING
print(header("AUDIO PROCESSING"))

if len(fps)==2:
    indexes_consecutive_black_frames_seconds = (np.array(indexes_consecutive_black_frames)/video_frame_rate*(float(fps[0])/float(fps[1])))
    mean_indexes_black_frames_seconds = (np.array(mean_indexes_black_frames)/video_frame_rate*(float(fps[0])/float(fps[1])))
    print(header("FPS conversion applied",align='l'))
    
count=0
for i,j in zip(indexes_consecutive_black_frames_seconds,mean_indexes_black_frames_seconds):
    count += 1
    print('Black frames sequence',count,'found in',convert_seconds_to_hh_mm_ss(i[0]),'-',convert_seconds_to_hh_mm_ss(i[1]),'Middle frame is',convert_seconds_to_hh_mm_ss(j))

print()

print(header("Check silence inside black frames sequences",align='l'))
temp_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)),'temp')
os.makedirs(temp_folder,mode=0o777,exist_ok=True)
audio_file_wav = generate_wav(audio_file,temp_folder,mono=True)

tolerance = 0

x, Fs = sf.read(audio_file_wav)
x = x/x.max()

silences_indexes = []
silences_mean = []

for i,j in zip(indexes_consecutive_black_frames_seconds,mean_indexes_black_frames_seconds):
    first_sample = int(i[0]*Fs)
    last_sample = int(i[1]*Fs)
    middle_sample = int(j*Fs)
    
    if i[0]==0.0:
        silences_indexes.append((first_sample,last_sample))
        silences_mean.append(first_sample)  
    else:
        result = np.where(abs(x[first_sample:last_sample+1]) <= tolerance)
        if len(result) > 0:
            silences_indexes.append((first_sample+result[0][0],first_sample+result[0][-1]))
            silences_mean.append(first_sample+result[0][-1])
   
count=0
for i,j in zip(silences_indexes,silences_mean):
    count += 1
    print('Silence',count,'found in',convert_seconds_to_hh_mm_ss(i[0]/Fs),'-',convert_seconds_to_hh_mm_ss(i[1]/Fs),'Chapter starts at',convert_seconds_to_hh_mm_ss(j/Fs))

os.remove(audio_file_wav)

print()
#%%
print(header("CHAPTER FILE GENERATION"))

output_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)),'outputs')
os.makedirs(output_folder,mode=0o777,exist_ok=True)
chapter_file_xml = '.'.join([os.path.splitext(video_file)[0],"xml"])
output_file = os.path.join(output_folder,os.path.basename(chapter_file_xml))

chapters = []
for i in silences_mean:
    chapters.append(i/Fs)
    
generate_chapter_file(chapters,output_file)

print('SUCCESS. Chapter file generated.',output_file)

print()

print(header("Check chapter file",align='l'))
chapters = get_chapter_info(output_file)

count=0
for i in chapters:
    count += 1
    print('Chapter',count,'starts at',convert_seconds_to_hh_mm_ss(i))

print()

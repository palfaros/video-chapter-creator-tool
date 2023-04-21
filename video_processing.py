# -*- coding: utf-8 -*-
"""
    File: video_processing.py
    Author: Pablo Alfaro Saracho
    Description: Functions to process video files
"""

import cv2
import numpy as np
from statistics import mean

def get_video_frame_rate(video_file):

    video = cv2.VideoCapture(video_file)
    frame_rate = video.get(cv2.CAP_PROP_FPS)
    video.release()

    return frame_rate

def get_black_frames_from_video(video_file):
    
    vidcap = cv2.VideoCapture(video_file)
    success,image = vidcap.read()
    
    black_frames = []
    is_black_frame = []
    
    black_frame_threshold = 3
    
    count = 0
    success = True
    while success:
      if np.average(image)<black_frame_threshold:
          is_black_frame.append(1)
          black_frames.append(count)
      else:
          is_black_frame.append(0)

      success,image = vidcap.read()
      count += 1
      
    vidcap.release()
    
    return black_frames,is_black_frame

def silence_finder_from_black_frames(is_black_frame):
    consecutive_black_frames_counter = 0
    indexes_consecutive_black_frames = []
    mean_indexes_black_frames = []
    
    min_consecutives_black_frames = 2
    
    # First iteration
    if(is_black_frame[0]==1):
        consecutive_black_frames_counter = consecutive_black_frames_counter + 1
        
    # Iterations 1 to N-1
    for i in range(1,len(is_black_frame)-1):
        if (is_black_frame[i]==1) and (is_black_frame[i-1]==1):
            consecutive_black_frames_counter = consecutive_black_frames_counter + 1
        else:
            if (consecutive_black_frames_counter >= min_consecutives_black_frames):
                indexes = (i-consecutive_black_frames_counter,i)
                indexes_consecutive_black_frames.append(indexes)
                mean_indexes_black_frames.append(mean(indexes))
                consecutive_black_frames_counter = 0
            else:
                consecutive_black_frames_counter = 0
    # Final iteration
    if (is_black_frame[-1]==1) and (is_black_frame[-2]==1):
        consecutive_black_frames_counter = consecutive_black_frames_counter + 1
        if (consecutive_black_frames_counter >= min_consecutives_black_frames):
            indexes = (i-consecutive_black_frames_counter,i)
            indexes_consecutive_black_frames.append(indexes)
            mean_indexes_black_frames.append(mean(indexes))
            consecutive_black_frames_counter = 0
                
    return indexes_consecutive_black_frames,mean_indexes_black_frames

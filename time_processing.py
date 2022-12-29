# -*- coding: utf-8 -*-
"""
    File: time_processing.py
    Author: Pablo Alfaro Saracho
    Description: Functions to convert seconds to hours:minutes:seconds string format and vice versa
"""

def convert_seconds_to_hh_mm_ss(s):
    seconds = abs(s) % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    if (s<0):
        if seconds < 10:
            return ("-%02d:%02d:0%.3f" % (hour, minutes, seconds)).replace('.',',')
        else:
            return ("-%02d:%02d:%.3f" % (hour, minutes, seconds)).replace('.',',')
    else:
        if seconds < 10:
            return ("%02d:%02d:0%.3f" % (hour, minutes, seconds)).replace('.',',')
        else:
            return ("%02d:%02d:%.3f" % (hour, minutes, seconds)).replace('.',',')

def convert_hh_mm_ss_to_seconds(time_str):
    h, m, s = time_str.split(':')
    seconds = int(h) * 3600 + int(m) * 60 + float(s)
    
    return seconds

if __name__ == '__main__':
    print('Time in seconds to hours:minutes:seconds example')

    time_in_seconds = 30.41
    print('Seconds ->',time_in_seconds,'-','Hours:Minutes:Seconds ->',convert_seconds_to_hh_mm_ss(time_in_seconds))

    time_in_seconds = 652.88
    print('Seconds ->',time_in_seconds,'-','Hours:Minutes:Seconds ->',convert_seconds_to_hh_mm_ss(time_in_seconds))

    time_in_seconds = 19210.1932
    print('Seconds ->',time_in_seconds,'-','Hours:Minutes:Seconds ->',convert_seconds_to_hh_mm_ss(time_in_seconds))
    
    time_in_seconds = -19210.1932
    print('Seconds ->',time_in_seconds,'-','Hours:Minutes:Seconds ->',convert_seconds_to_hh_mm_ss(time_in_seconds))

    time_in_seconds = 0.5
    print('Seconds ->',time_in_seconds,'-','Hours:Minutes:Seconds ->',convert_seconds_to_hh_mm_ss(time_in_seconds))

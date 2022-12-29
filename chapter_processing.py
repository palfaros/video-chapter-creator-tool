# -*- coding: utf-8 -*-
"""
    File: chapter_processing.py
    Author: Pablo Alfaro Saracho
    Description: Functions to process and generate chapter files
"""

import xml.etree.ElementTree as ET #To manage xml files content
import xml.etree.cElementTree as cET #To create ElementTrees files content
from lxml import etree # To create and write xml files
from time_processing import convert_hh_mm_ss_to_seconds

def get_chapter_info(chapter_file_xml):
    tree = ET.parse(chapter_file_xml)
    root = tree.getroot()
    
    chapters = []
    
    for chapter in root.iter('ChapterTimeStart'):
        chapters.append(convert_hh_mm_ss_to_seconds(chapter.text))
     
    return chapters

def convert_seconds_to_mkvmerge_hh_mm_ss(s):
    seconds = abs(s) % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    if (s<0):
        if seconds < 10:
            return ("-%02d:%02d:0%.9f" % (hour, minutes, seconds))
            return ("-%02d:%02d:%.9f" % (hour, minutes, seconds))
    else:
        if seconds < 10:
            return ("%02d:%02d:0%.9f" % (hour, minutes, seconds))
        else:
            return ("%02d:%02d:%.9f" % (hour, minutes, seconds))

def generate_chapter_file(chapters,chapter_file_xml):

    root = etree.Element('Chapters')
    edition_entry = etree.SubElement(root,'EditionEntry')
    
    count = 0
    for chapter in chapters:
        count += 1
        chapter_atom = etree.SubElement(edition_entry,'ChapterAtom')
        chapter_time_start = etree.SubElement(chapter_atom,'ChapterTimeStart').text = convert_seconds_to_mkvmerge_hh_mm_ss(chapter)
        chapter_flag_hidden = etree.SubElement(chapter_atom,'ChapterFlagHidden').text = '0'
        chapter_flag_enabled = etree.SubElement(chapter_atom,'ChapterFlagEnabled').text = '1'
        chapter_display = etree.SubElement(chapter_atom,'ChapterDisplay')
        chapter_string = etree.SubElement(chapter_display,'ChapterString').text = "%s %s" %('Chapter',str(count))
        chapter_language = etree.SubElement(chapter_display,'ChapterLanguage').text = 'eng'
    
    tree = etree.ElementTree(root)
    tree.write(chapter_file_xml,pretty_print=True,encoding="utf-8", xml_declaration=True,doctype='<!-- <!DOCTYPE Chapters SYSTEM "matroskachapters.dtd"> -->')
    
if __name__ == '__main__':

    file = 'example_chapter_file.xml'
    chapters = [0,60,120]
    generate_chapter_file(chapters,file)
    chapters = get_chapter_info(file)
    print(chapters)

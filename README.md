# Video Chapter Creator Tool

Pablo Alfaro, 2022

## Summary

A tool to automatically create a chapter file from a video, e.g., a TV show episode or a movie.

## Description

![Diagram](https://user-images.githubusercontent.com/116673615/210000242-ee1f6414-2222-4208-852f-5b4f721c140f.gif)

## Getting Started

### Dependencies

* [ffmepg](https://github.com/FFmpeg/FFmpeg)
* Windows 10, Linux

### Installing



```
git clone https://github.com/palfaros/video-chapter-creator-tool.git
```

### Executing program

This tool requires a video file and its audio track separately. Video must be ```.mp4``` or ```.avi``` only.
```
video_chapter_creator_tool.py -v S0xEyy.avi -a S0xEyy_Track01.ac3
```
The tool allows to use video and audio files with different framerate. The audio track framerate is set to be the final framerate of the chapter file. To use this feature, the old framerate (video) and the new framerate (audio) must be specified. For example, if video framerate is 25 fps and audio framerate is 23.976:
```
video_chapter_creator_tool.py -v S0xEyy.avi -a S0xEyy_Track01.ac3 -f 25.000 23.976
```

## Help

Run the ```video_chapter_creator_tool.py``` script with --help for usage information.

```
video_chapter_creator_tool.py --help
```

Output:

```
usage: video_chapter_creator_tool.py [-h] -v VIDEO_FILE -a AUDIO_FILE [-f FRAMERATE FRAMERATE]

optional arguments:
  -h, --help            show this help message and exit
  -v VIDEO_FILE, --video-file VIDEO_FILE
  -a AUDIO_FILE, --audio-file AUDIO_FILE
  -f FRAMERATE FRAMERATE, --framerate FRAMERATE FRAMERATE
```

## Authors

[Pablo Alfaro Saracho](https://www.linkedin.com/in/pablo-alfaro-saracho)

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the [MIT License](https://mit-license.org/) - see the LICENSE.md file for details


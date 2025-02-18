# mymedia

Tools to manage my video and manga collections for media server like kavita and emby

## Installation

- TODO

## Usage

### For TV (Anime)

#### rename_tv

Assume following folder structure

```
- TV name (2025)
    - Season 1
        - [Moozzi2] TV name - 01 (BD 1920x1080 HEVC-YUV444P10 FLACx2).mkv
        - [Moozzi2] TV name - 02 (BD 1920x1080 HEVC-YUV444P10 FLAC).mkv
    
    - Season 2
        - ...

```

Inside the `TV name (2025)` folder, run the following command:

```
mymedia_rename_tv
```

This will rename all video files (and subtitle files) to match the standard naming convention required by the media server:

```
- TV name (2025)
    - Season 1
        - TV name S01E01.mkv
        - TV name S01E02.mkv
    
    - Season 2
        - TV name S02E01.mkv
        - ...
```

A `rename_history.log` file will be generated in each Season folder, containing a mapping of the original names to the new names

You can also run the command from within a specific Season folder. In that case, only the video files in that season will be renamed.

Additionally, if there are no Season folders and the video files are placed directly under the `TV name (2025)` folder, running the command inside the TV folder will automatically assume that all videos belong to Season 1.


##### Auto detection and manual configration

- TODO


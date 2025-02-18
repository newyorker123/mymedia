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
$ mymedia_rename_tv
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

The library automatically detects the TV series name and season number from the folder structure. To ensure accurate detection, the folder names must follow a specific format:

1. The outermost folder should be named `TV name (yyyy)`, where the parentheses and year are required.
2. The season folder should be named `Season x`, where "x" is the season number.

If you want to override the automatic detection, you can use the following flags in the command line:

- `-n`, `--name`
  - The name of the TV series
- `--season`
  - The season number

Note that the `--season` flag can only be used if you're inside a specific season folder or if there is no season folder at all.

```
$ mymedia_rename_tv -n "New Name" --season 2
```

##### Episode regex

Episode numbers are automatically extracted from the original filename using regular expressions. Some examples of valid filename formats include:

- [VCB-Studio] Tensei shitara Dainana Ouji [01][Ma10p_1080p][x265_flac_aac].mkv
- [Nekomoe kissaten&LoliHouse] Ishura - 01 [WebRip 1080p HEVC-10bit AAC ASSx2].mkv
- [Nekomoe kissaten&LoliHouse] Ao no Hako - 04v2 [WebRip 1080p HEVC-10bit AAC ASSx2].mkv
- [Moozzi2] Boku no Kokoro no Yabai Yatsu - 25 END (BD 1920x1080 HEVC-YUV444P10 FLACx2).mkv
- Chi.Chikyuu.no.Undo.ni.Tsuite.S01E06.2024.1080p.NF.WEB-DL.H264.DDP2.0-ZeroTV

If the episode number cannot be matched using the default pattern, you can provide a custom regex pattern with the `--ep_regex` flag. The episode number should be grouped in parentheses, like this: `"Episode (\d\d)"`.

Example usage:

```
$ mymedia_rename_tv --ep_regex "Episode (\d\d)\s"
```

##### Episode number offset

Some anime series have consecutive episode numbering across different seasons. For example, the first episode of Season 2 of *Re:Zero* is episode 26. As a result, the first episode you download for Season 2 may have a filename like:

- [VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 2nd Season [26][Ma10p_1080p][x265_flac_aac].mkv

If you want to rename this to `S02E01`, you can use the `-o, --offset` flag.

```
$ mymedia_rename_tv --offset -25
```

The offset of `-25` will be **added** to the original episode number (26), so the final episode number will be 01. (Note that the offset should be negative in this case)

The offset, along with the series name and season, will be saved in the `mymedia-config.json` file inside each season folder.

The next time you download a new episode, you won't need to provide the `--offset` flag again; the program will read the `mymedia-config.json` file and automatically apply the offset to the new episode—without affecting previously renamed episodes.


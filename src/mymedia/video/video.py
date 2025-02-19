import re
import sys

VID_SUFFIX_LIST=['.mkv','.mp4']
SUB_SUFFIX_LIST=['.srt','.ass','.ASS','.SRT']
IMG_SUFFIX_LIST=['.jpg','.png','.jpeg']
NFO_SUFFIX_LIST=['.nfo']

MYMEIDA_CONFIG="mymedia-config.json"
HISTORY="rename_history.log"

EP_REGEX=[
    r"EP(\d+)",
    r"Ep(\d+)",
    r"\[(\d+)\]",
    r"S\d\dE(\d+)",
    r"第(\d+)集",
    r"第(\d+)話",
    r"#(\d+)",
    r"^(\d+)$",
    r"-\s(\d+)\s",
    r"-\s(\d+)v[23]",

]
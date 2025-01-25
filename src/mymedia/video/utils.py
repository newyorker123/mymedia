import re
import sys

from ..utils import get_group

VID_SUFFIX_LIST=['.mkv','.mp4']
SUB_SUFFIX_LIST=['.srt','.ass','.ASS','.SRT']
IMG_SUFFIX_LIST=['.jpg','.png','.jpeg']
NFO_SUFFIX_LIST=['.nfo']

MYMEIDA_CONFIG="mymedia-config.json"
HISTORY="rename_history.log"

PATTERN=fr"EP(\d+)|Ep(\d+)|\[(\d+)\]|S\d\dE(\d+)|第(\d+)集|第(\d+)話|#(\d+)|^(\d+)$|-\s(\d+)\s|-\s(\d+)v[23]"

def match_episode_num(file,pattern):
    try:
        episode=get_group(re.search(pattern,file.stem,re.I))
        episode=int(episode)
    except AttributeError:
        print(f"Can't get episode number for {file.name}. Please refine regex.")
        number=input("Please input episode number(-1 to exit): ")
        if number=="-1":
            sys.exit()
        else:
            episode=int(number)
    return episode
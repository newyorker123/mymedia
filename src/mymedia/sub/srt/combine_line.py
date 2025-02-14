import argparse
from pathlib import Path

from . import SrtFile

def parse_args(args=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("files", nargs='*')

    return parser.parse_args(args)

def get_target_list(srt_list):
    if len(srt_list) == 0:
        return list(Path.cwd().glob("*.srt"))
    
    return srt_list

def combline_line_for_single_srt(srt:SrtFile) -> SrtFile:
    
    i=0
    new_srt=SrtFile()
    while i<srt.num_of_lines:
        a=srt[i]
        if i==srt.num_of_lines-1:
            new_srt.add_line(a.start,a.end,a.content)
            i+=1
        else:
            b=srt[i+1]
            if a.start==b.start and a.end==b.end:
                new_srt.add_line(a.start,a.end,f"{a.content}\n{b.content}")
                i+=2
            else:
                new_srt.add_line(a.start,a.end,a.content)
                i+=1

    return new_srt



def combine_line(args=None):
    args=parse_args(args)

    target_list=get_target_list(args.files)

    for srt in target_list:
        srt=SrtFile.from_file(srt)
        new_srt=combline_line_for_single_srt(srt)
        new_srt.output(file_stem=srt.file.stem)




def main(args=None):
    combine_line(args)


if __name__=="__main__":
    main()

from pathlib import Path
import shutil
import argparse
from .split_image import split_dir

def parse_args(args=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("-nr",action="store_true",help="Not reverse the order of two-page manga")
    return parser.parse_args(args)

def main():
    args = parse_args()
    Path("out").mkdir(exist_ok=True)

    for volume in [folder for folder in Path(".").glob('*/') if folder.name != 'out']:
        volume_name=volume.name 
        volume_out=volume/volume_name
        assert (volume/"out").exists(), f"{volume_name} doesn't have an out folder"
        split_dir(volume,1,2,False,False,not args.nr,False,volume_out)
        shutil.copytree(volume/"out",volume_out,dirs_exist_ok=True)
        volume_out.replace(Path("out")/volume_name)

if __name__=="__main__":
    main()
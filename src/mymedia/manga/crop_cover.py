# crop BookWalker JP cover image

from PIL import Image
from pathlib import Path
import argparse

EXTENSIONS=['.jpg','.png','.jpeg']

def parse_args(args=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('-p','--path',default='.')
    parser.add_argument('-s','--source',nargs='*',help="file extension")
    parser.add_argument('-w','--width',default=1312,type=float)
    parser.add_argument('--overwrite',action='store_true')
    return parser.parse_args(args)



def cal_corner(width,height=None):
    total_width=3840
    total_height=2160

    left=(total_width-width)/2
    right=total_width-left

    upper=212
    lower=2076

    return (left,upper,right,lower)

def crop_image(inpath,width=1312):
    with Image.open(inpath) as img:
        cropped_img=img.crop(cal_corner(width))

    return cropped_img

def save(cropped_images:list,images_path,overwrite:bool):
    if overwrite:
        for cropped,img in zip(cropped_images,images_path):
            cropped.save(img)
    else:
        for i,(cropped,img) in enumerate(zip(cropped_images,images_path)):
            out=img.parent/f"000_{i}{img.stem}"
            cropped.save(img.parent/f"000_{i}{img.suffix}")

def main():
    args=parse_args()
    path=Path(args.path)
    extensions=['.'+ext for ext in args.source] if args.source else EXTENSIONS
    width=float(args.width)

    images_path=sorted(sum([list(path.glob(f'*{ext}')) for ext in extensions],start=[]))

    cropped_images=[crop_image(img,width) for img in images_path]

    save(cropped_images,images_path,args.overwrite)





if __name__=="__main__":
    main()
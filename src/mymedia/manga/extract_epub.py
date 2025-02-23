from pathlib import Path 
import zipfile
import argparse
import re
import shutil


def extract_epub(path:Path|str):
    path=Path(path)

    out=path/'out'
    out.mkdir(exist_ok=True)

    tmp=path/'tmp'

    for book in path.glob('*.epub',case_sensitive=False):
        tmp.mkdir(exist_ok=True)

        tmp_book=Path(shutil.copy2(book,tmp))
        tmp_book=tmp_book.rename(tmp_book.with_suffix('.zip'))

        shutil.unpack_archive(tmp_book,tmp)

        extract_images(book.stem,tmp,out)
        print(f"{book.stem} finished")


def extract_images(name:str,tmp:Path,out:Path):

    images = None

    if tmp/'OEBPS' in tmp.iterdir():
        extract_folder=tmp/'OEBPS'
        images=extract_folder/'images'
    elif tmp/'item' in tmp.iterdir():
        extract_folder=tmp/'item'
        images=extract_folder/'image'

    if images is None:
        raise ValueError('No valid image folder')

    if not images.exists():
        raise FileNotFoundError("Image folder doesn't exist")

    images.replace(out/name)
    shutil.rmtree(tmp)

def parse_args(args=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("-p","--path",default='.')
    return parser.parse_args(args)


def main():
    args=parse_args()
    path=Path(args.path)
    extract_epub(path)




if __name__=="__main__":
    main()

    



     

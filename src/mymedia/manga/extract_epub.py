from pathlib import Path 
import zipfile
import argparse
import re
import shutil


out=Path('out')
out.mkdir(exist_ok=True)


def extract_epub():
    tmp=Path('tmp')
    tmp.mkdir()

    for book in Path('.').glob('*.epub'):
        tmp_book=Path(shutil.copy2(book,tmp))
        tmp_book=tmp_book.rename(tmp_book.with_suffix('.zip'))

        shutil.unpack_archive(tmp_book,'tmp')

        extract_images(book.stem,tmp)


def extract_images(name:str,tmp:Path):
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


def main():
    extract_epub()




if __name__=="__main__":
    main()

    



     

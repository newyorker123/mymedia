mode_help="""
该脚本用于把处于文件夹结构下的图片文件打包为cbz文件, 并重命名为name Vol.xx Chap.yy.cbz。存在3种模式:

1. 2层文件夹结构, 首层为volume文件夹, 第二层为chapter文件夹,常见于bilibili漫画。输出文件名为name Vol.xx Chap.yy.cbz。要使用该模式, 令mode='bilibili'
2. 1层文件夹结构, 只有volume文件夹, 常见于台版单行本。输出文件名为name Vol.xx.cbz。要使用该模式, 令mode='vol'
3. 1层文件夹结构, 只有chapter文件夹, 常见于简体网站的不成单行本的连载图源或条漫。输出文件名为name Chap.yy.cbz。要使用该模式, 令mode='chap'

默认为台版, 即模式2
"""

import argparse
import re
from pathlib import Path
import shutil
import zipfile

from . import CHAP_REGEX,VOL_REGEX
from mymedia.utils import match_num, match_string,file_sort,cat_regex


def archive_image(image_dir:Path,out_dir,out_stem,delete:int,sort_func=file_sort):

    files=list(image_dir.iterdir())
    if delete < 0:
        files=sorted(files,key=sort_func)[:delete]
    elif delete > 0:
        files=sorted(files,key=sort_func)[delete:]

    archive_file=Path(out_dir)/f"{out_stem}.cbz"


    with zipfile.ZipFile(archive_file, mode="w",strict_timestamps=False) as archive:
        for file in files:
            archive.write(file,arcname=file.name)

    return archive_file


def set_default_args(args):

    if args['out'] is None:
        args['out'] = '.' if args['mode'] == 'vol' else 'out'




def prompt_args(mode):
    args=dict()

    args['name']=input("Enter series name:")

    if mode == 'vol':
        vol_regex=input("Enter volume regex(no input to use default, ';' to seperate multiple values):")
        args['vol_regex']=None if (vol_regex=="0" or vol_regex=="") else vol_regex.split(';')
    elif mode == 'chap':
        chap_regex=input("Enter chapter regex(no input to use default, ';' to seperate multiple values):")
        args['chap_regex']=None if (chap_regex=='0' or chap_regex == "") else chap_regex.split(';')

        title_regex=input("Enter title regex(no input for no title, ';' to seperate multiple values):")
        args['title_regex']=None if (title_regex=='0' or title_regex == "") else title_regex.split(';')
    else:
        vol_regex=input("Enter volume regex(no input to use default, ';' to seperate multiple values):")
        args['vol_regex']=None if (vol_regex=="0" or vol_regex=="") else vol_regex.split(';')

        chap_regex=input("Enter chapter regex(no input to use default, ';' to seperate multiple values):")
        args['chap_regex']=None if (chap_regex=='0' or chap_regex == "") else chap_regex.split(';')

        title_regex=input("Enter title regex(no input for no title, ';' to seperate multiple values):")
        args['title_regex']=None if (title_regex=='0' or title_regex == "") else title_regex.split(';')

    delete=input("Enter pages to delete for every chapter(0 for not delete):")
    args['delete']=0 if (delete=='0' or delete == "") else int(delete)

    return args


def mode_bilibili(path:Path,output_dir:Path,name ,vol_regex:list, chap_regex:list, title_regex:str, delete:int):
    volumes=[folder for folder in path.glob('*/') if folder.name != output_dir.name]
    title_note={}

    for volume in volumes:
        vol_num=match_num(volume.name,vol_regex,'volume')

        for chapter in volume.glob('*/'):
            chap_num=match_num(chapter.name,chap_regex)
            out_stem=f"{name} Vol.{vol_num} Ch.{chap_num}"
            cbz_file=archive_image(chapter,output_dir,out_stem,delete)

            if title_regex is not None:
                title=match_string(chapter.name,title_regex,'title')
                ci=create_ComicInfo(output_dir)

                if '&' in title:
                    title_note[cbz_file.name]=title
                    title=title.replace('&','')

                write_title_to_cbz(title,ci)
                archive_ComicInfo(cbz_file,ci)

        print(f"Volume {vol_num} finished")

    if title_note:
        print("=====================================")
        for k,v in title_note.items():
            print(f"{k} has '&' in the title. The original title is : {v}")


def mode_vol(path:Path,output_dir:Path, name, vol_regex:list[str]):
    folders=[folder for folder in path.glob('*/') if folder.name != output_dir.name]
    
    for folder in folders:
        if name is not None:
            vol_num=match_num(folder.name,vol_regex,"volume")
            out_stem=f"{name} Vol.{vol_num}"
        else:
            out_stem=folder.name

        change_colophon(folder)

        archive_image(folder,output_dir,out_stem,0,None)

        print(f"{folder} finished")

def change_colophon(volume:Path):
    imgs=list(volume.glob('img[0-9][0-9][0-9]*.jpg'))
    if len(imgs) > 0:
        
        colophon=volume/'i-colophon.jpg'
        white=volume/'i-white.jpg'
        if colophon.exists():
            colophon.rename(colophon.with_stem('z-colophon'))
        if white.exists():
            white.rename(white.with_stem('c-white'))
        


        


def create_ComicInfo(output_path='out'):

    output_path=Path(output_path)
    output_path.mkdir(exist_ok=True)
    comicinfo=output_path/'ComicInfo.xml'

    with open(comicinfo,mode='w',encoding='utf8') as f:
        f.write("<?xml version='1.0' encoding='utf-8'?>\n")
        f.write("<ComicInfo>\n")

    return comicinfo

def write_title_to_cbz(title:str,comicinfo:Path):

    with open(comicinfo,mode='a',encoding="utf8") as f:
        f.write(f"<Title>{title}</Title>\n")

    return comicinfo

def archive_ComicInfo(cbz_file,comicinfo:Path):

    with open(comicinfo,mode='a',encoding="utf8") as f:
        f.write("</ComicInfo>\n")

    with zipfile.ZipFile(cbz_file, mode="a") as archive:
        archive.write(comicinfo,'ComicInfo.xml')

    comicinfo.unlink()


def mode_chap(path:Path,output_dir:Path, name, chap_regex: list[str], title_regex:str,delete:int):
    folders=[folder for folder in path.glob('*/') if folder.name != output_dir.name]

    if len(folders) != 1:
        raise RuntimeError('Can only have one manga folder')
    
    manga=folders[0]
    title_note={}
    for chap in manga.glob('*/'):
        chap_num=match_num(chap.name,chap_regex,'chapter')

        out_stem=f"{name} Ch.{chap_num}"
        cbz_file=archive_image(chap,output_dir,out_stem,delete)
        
        if title_regex is not None:
            title=match_string(chap.name,title_regex,'title')
            ci=create_ComicInfo(output_dir)

            if '&' in title:
                title_note[cbz_file.name]=title
                title=title.replace('&','')

            write_title_to_cbz(title,ci)
            archive_ComicInfo(cbz_file,ci)

        print(f"Chapter {chap_num} finished")

    if title_note:
        print("=====================================")
        for k,v in title_note.items():
            print(f"{k} has '&' in the title. The original title is : {v}")



def parse_args(args=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("-p","--path",default='.')
    parser.add_argument("-m","--mode",default='vol',help=mode_help)
    parser.add_argument("-n","--name",help="Series name")
    parser.add_argument("-o","--out",help="The output path")
    parser.add_argument("--vol",dest="vol_regex",nargs="+",help="Volume regex")
    parser.add_argument("--chap",dest="chap_regex",nargs="+",help="Chapter regex")
    parser.add_argument("--title",dest="title_regex",nargs="+",help="Titile regex")  
    #parser.add_argument('--input',action="store_true",help="Use input prompt to input args")
    parser.add_argument('-d','--delete',type=int, default=0 ,help="每个文件夹中需要删除的图片. 2表示删除前2张, -2表示删除最后2张")
    args=parser.parse_args(args)
    args=vars(args)
    set_default_args(args)

    if args['mode'] != 'vol':
        new_args=prompt_args(args['mode'])
        args.update(new_args)

    return args

def main(args=None):

    args=parse_args(args)

    path=Path(args['path'])
    
    output_path=Path(args['out'])
    output_path.mkdir(exist_ok=True)


    if args['mode'] == 'vol':
        vol_regex= cat_regex(args['vol_regex'],VOL_REGEX)
        mode_vol(path,output_path,args['name'],vol_regex)
    elif args['mode'] == 'bilibili':
        vol_regex= cat_regex(args['vol_regex'],VOL_REGEX)
        chap_regex = cat_regex(args['chap_regex'],CHAP_REGEX)
        title_regex = args['title_regex']
        mode_bilibili(args['path'],output_path,args['name'],vol_regex,chap_regex,title_regex,args['delete'])
    else:
        chap_regex = cat_regex(args['chap_regex'],CHAP_REGEX)
        title_regex = args['title_regex']
        mode_chap(path,output_path,args['name'],chap_regex,title_regex,args['delete'])






if __name__=="__main__":
    args=main()




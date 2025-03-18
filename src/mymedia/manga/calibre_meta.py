import subprocess
import argparse
from pathlib import Path
from natsort import natsorted

from .manga import VOL_REGEX
from mymedia.utils.utils import match_num, match_string,cat_regex

def parse_args(args=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('--path',default='.')
      
    subparsers=parser.add_subparsers()

    parser_pdf=subparsers.add_parser("pdf")
    parser_pdf.add_argument("-a",'--authors',help="Set the authors")
    parser_pdf.add_argument("-p",'--publisher',help="Set the e-book publisher")
    parser_pdf.add_argument("-s",'--series',help="Set the series name")
    parser_pdf.add_argument("-d",'--date',help="Set the published date for the first book, e.g. YYYY-mm-dd")
    parser_pdf.set_defaults(func=pdf_meta)
    parser_pdf.add_argument("-c",'--comments',help="Set the e-book description for the first book")
    parser_pdf.add_argument('--vol_regex',nargs="?",default=False,const=None,help="The regex to match volume number from filename")

    parser_epub=subparsers.add_parser("epub")
    parser_epub.add_argument("-a",'--authors',help="Set the authors")
    parser_epub.add_argument("-p",'--publisher',help="Set the e-book publisher")
    parser_epub.add_argument("-s",'--series',help="Set the series name")
    parser_epub.add_argument("-d",'--date',help="Set the published date for the first book, e.g. YYYY-mm-dd")
    parser_epub.set_defaults(func=epub_meta)
    parser_epub.add_argument("-t","--title",action="store_true",help="Set the title as 'series (index)'")
    parser_epub.add_argument("--index_regex",help="The regex to match series-index number from filename")
	
    return parser.parse_args(args)

def command_for_all(args:dict):
    command=['ebook-meta']
    if args.series is not None:
        command+=['--series',args.series]
    if args.publisher is not None:
        command+=['--publisher',args.publisher]
    if args.authors is not None:
        command+=['--authors',args.authors,'--author-sort',args.authors]
		
    return command

def add_index(command:list,filename:str,regex:str):
    vol_regex=cat_regex(regex,VOL_REGEX)
    index=match_num(filename,vol_regex,'index')
    command+=["--index",str(index)]
    return command,index

      
      


def pdf_meta(args):
    #args_d=vars(args)
    path=Path(args.path)

    root_command=command_for_all(args)

    pdf_list=natsorted(path.glob("*.pdf"))

    for i,pdf in enumerate(pdf_list):
        command=root_command.copy()
        command.insert(1,pdf.name)

        # add comments to the first book
        if i==0: 
            if args.comments is not None:
                command+=['--comments',args.comments]
            if args.date is not None:
                 command+=['--date',args.date]
        if args.vol_regex != False:
             command,_=add_index(command,pdf.name,args.vol_regex)


        subprocess.run(command,cwd=path) 
        print(f"{pdf.name} finished")
      

def epub_meta(args):
    
    path=Path(args.path)

    root_command=command_for_all(args)
    # clear tags
    root_command+=["--tags",""]

    epub_list=natsorted(path.glob("*.epub"))

    for i,epub in enumerate(epub_list):
        command=root_command.copy()
        command.insert(1,epub.name)

        command,index=add_index(command,epub.name,args.index_regex)

        # add comments to the first book
        if i==0: 
            if args.date is not None:
                 command+=['--date',args.date]
        if args.title:
            command+=["--title",f"{args.series} ({index})"]

        subprocess.run(command,cwd=path) 
        print(f"{epub.name} finished")

    




def main(args=None):
    args=parse_args(args)
    args.func(args)
    
	
	

if __name__=="__main__":
	main()
	

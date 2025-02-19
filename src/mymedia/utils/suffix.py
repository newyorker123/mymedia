from pathlib import Path
import argparse

def change_suffix(path:Path|str,to:str,from_=None,recursive=False):
    path=Path(path)

    files=[p for p in path.rglob('*') if p.is_file()] if recursive else [p for p in path.glob('*') if p.is_file()]

    target = [f for f in files if f.suffix.lower() == ('.'+from_).lower()] if from_ is not None else files

    for f in target:
        f.rename(f.with_suffix('.'+to))


def parse_args(args=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("-p",'--path',default=".",help="The path for the operation")
    parser.add_argument("-r",'--recursive',action="store_true",help="recursively apply the operation for all files under path")
    parser.add_argument('--from',dest="from_",help="apply to what files, e.g. 'zip'")
    parser.add_argument('to',help="change to what, i.e. 'cbz'")

    return parser.parse_args(args)

def main():
    args =parse_args()
    change_suffix(args.path,args.to,args.from_,args.recursive)
    

if __name__=="__main__":
    main()

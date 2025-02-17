import argparse
from pathlib import Path
import re
import logging
import json
import sys

from .utils import VID_SUFFIX_LIST,SUB_SUFFIX_LIST,IMG_SUFFIX_LIST,NFO_SUFFIX_LIST,EP_REGEX,MYMEIDA_CONFIG
from mymedia.utils import match_num,cat_regex



class TVFile:
    TYPE="TV"
    def __init__(self,path:Path,ep_regex:list[str]):
        self.path=path.resolve()
        self.original_name=self.path.name
        self.ep_regex=ep_regex
        self.match_ep=match_num(self.path.name,ep_regex,'episode')

    def __repr__(self):
        return f"{self.__class__.__name__}({self.path})"
    
    def rename(self,name,season,offset:int=0):
        old_name=self.original_name
        new_f=self.path.with_stem(f"{name} S{season:02}E{self.match_ep+offset:02}")
        new_name=new_f.name
        if new_name != old_name:
            self.path.rename(new_f)
            self.log_rename(old_name,new_name,season)
            return 1
        return 0
    
    def log_rename(self,old_name,new_name,season):
        logger=logging.getLogger(f"Season {season}")
        logger.debug(f"{self.TYPE} : \"{old_name}\" is renamed to \"{new_name}\"")
    

class ShowFile(TVFile):
    TYPE="VIDEO"
    standard_regex=r"^.*?\sS\d+E\d+"

    def __init__(self,path:Path,ep_regex:list[str]):
        super().__init__(path,ep_regex)
        self.new=False if re.search(self.standard_regex,self.path.stem) else True


class SubFile(TVFile):
    TYPE="SUB"
    standard_regex=r"^.*?\sS\d+E\d+(\.\w+)?"

    def __init__(self,path:Path,ep_regex:list[str]):
        super().__init__(path,ep_regex)
        self.new=False if re.search(self.standard_regex,self.path.stem) else True

    def get_sub_version(self):
        if (res:=re.search(r"\b(tc|sc|jptc|jpsc|chs|cht|jp|jap|gb)\b",self.original_name,re.I)):
            version=res.group(1).lower()
            if 'tc' in version:
                version='cht'
            elif 'sc' in version:
                version='chs'

            if version=='gb':
                version='chs'

        else:
            version='chs'
            
        return version
    
    def rename(self,name,season,offset=0):
        version=self.get_sub_version()
        old_name=self.original_name
        new_p=self.path.with_stem(f"{name} S{season:02}E{self.match_ep+offset:02}.{version}")
        new_name=new_p.name
        if old_name != new_name:
            self.path.rename(new_p)
            self.log_rename(old_name,new_name,season)
            return 1
        return 0


class ThumbFile(TVFile):
    TYPE="THUMB"
    standard_regex=r".*?-thumb$"

    def __init__(self,path:Path,ep_regex:list[str]):
        super().__init__(path,ep_regex)
        #self.new=False if re.search(self.standard_pattern,self.path.stem) else True

    @staticmethod
    def is_thumb(file:Path):
        if file.suffix in IMG_SUFFIX_LIST and re.search(ThumbFile.standard_regex,file.stem):
            return True
        else:
            return False
        
class NFOFile(TVFile):
    def __init__(self,path:Path,ep_regex:list[str]):
        super().__init__(path,ep_regex)

    





class SeasonFolder:
    name=None
    def __init__(self,path:Path|str,ep_regex:list[str]=EP_REGEX,name:None|str=None,season:None|int=None,offset:None|int=None,start:None|int=None):
        self.path=Path(path).resolve()
        self.ep_regex:list[str]=ep_regex
        self.vid_list=[]
        self.sub_list=[]
        self.thumb_list=[]
        self.nfo_list=[]
        self.other_list=[]
        self.start=None

        self.config=None
        self.log=None
        self.stats=None
        self.scan()

        self.set_from_cl(name,season,offset,start)

        if None in [self.name,self.season,self.offset]:
            if self.config:
                self.infer_config()
            if None in [self.name,self.season]:
              self.infer_path()

        if self.config is None:
            self.save_config()

        


    def set_from_cl(self,name,season,offset,start):
        """Set attribute from command line argument"""
        if name:
            self.__class__.name=name 
        
        self.season=season

        if start is not None:
            self.set_start(start)
        else:
            self.offset=offset
        

    def set_start(self,start):
        start_ep_num=self.vid_list[0].match_ep
        self.offset=start-start_ep_num
        self.start = True
        



    def infer_season(self):
        try:
            self.season=int(re.search(r"(?<=Season\s)\d+$",self.path.name).group())
        except AttributeError:
            self.season=1



    def scan(self):
        for f in self.path.iterdir():
            if f.is_file():
                if f.suffix in VID_SUFFIX_LIST:
                    self.vid_list.append(ShowFile(f,self.ep_regex))
                elif f.suffix in SUB_SUFFIX_LIST:
                    self.sub_list.append(SubFile(f,self.ep_regex))
                elif ThumbFile.is_thumb(f):
                    self.thumb_list.append(ThumbFile(f,self.ep_regex))
                #elif f.suffix in NFO_SUFFIX_LIST:
                #    self.nfo_list.append(NFOFile(f,self.pattern))
                elif f.name == "rename_history.log":
                    self.log=f 
                elif f.name=="mymedia-config.json":
                    self.config=f
                else:
                    self.other_list.append(f)
            
        self.vid_list.sort(key=lambda f:f.match_ep)
        self.sub_list.sort(key=lambda f:f.match_ep)
        self.thumb_list.sort(key=lambda f:f.match_ep)
        self.nfo_list.sort(key=lambda f:f.match_ep)

    def infer_config(self):
        with open(self.config,"r",encoding='utf-8') as f:
            obj=json.load(f)
        
        self.__class__.name=self.__class__.name if self.__class__.name else obj.get("name",None)
        self.season=self.season if (self.season is not None) else obj.get("season",None)
        self.offset=self.offset if (self.offset is not None) else obj.get("offset",0)

    def infer_path(self):
        self.offset = self.offset if self.offset else 0
        
        try:
            match_season=int(re.search(r"(?<=^Season\s)\d+",self.path.name).group())
        except AttributeError:
            match_season=-1

        if self.season is None:
            self.season = match_season if match_season != -1 else 1
        
        if self.name is None:
            if match_season == -1:
                try:
                    match_name=re.search(r".*?(?=\s\(\d{4}\))",self.path.name).group()
                except AttributeError:
                    match_name=input("Can't infer TV name.\nPlease enter name(-1 to exit): ")
                    if match_name=='-1':
                        sys.exit()
            else:
                try:
                    match_name=re.search(r".*?(?=\s\(\d{4}\))",self.path.parent.name).group()
                except AttributeError:
                    match_name=input("Can't infer TV name.\nPlease enter name(-1 to exit): ")
                    if match_name=='-1':
                        sys.exit()

            self.__class__.name=match_name

    def save_config(self):
        json_file=self.path/"mymedia-config.json"
        data={"name":self.name,"season":self.season,"offset":self.offset}

        with open(json_file,"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False)

        self.config=json_file
  
    def get_target(self,new:None|bool,vid:bool,sub:bool,thumb:bool,nfo:bool) -> dict[str,list]:

        target={}

        if new == True:
            if vid:
                target["vid"]=[f for f in self.vid_list if f.new]
            if sub:
                target["sub"]=[f for f in self.sub_list if f.new]
            if thumb:
                target["thumb"]=[f for f in self.thumb_list if f.new]
            if nfo:
                target["nfo"]=[f for f in self.nfo_list if f.new]    
        elif new == False:
            if vid:
                target["vid"]=self.vid_list
            if sub:
                target["sub"]=self.sub_list
            if thumb:
                target["thumb"]=self.thumb_list
            if nfo:
                target["nfo"]=self.nfo_list
        else:
            if vid:
                bool_list=[f.new for f in self.vid_list]
                if sum(bool_list)==0 or sum(bool_list)==len(bool_list):
                    target["vid"]=self.vid_list
                else:
                    target["vid"]=[f for f in self.vid_list if f.new]
            if sub:
                bool_list=[f.new for f in self.sub_list]
                if sum(bool_list)==0 or sum(bool_list)==len(bool_list):
                    target["sub"]=self.sub_list
                else:
                    target["sub"]=[f for f in self.sub_list if f.new]
            if thumb:
                bool_list=[f.new for f in self.thumb_list]
                if sum(bool_list)==0 or sum(bool_list)==len(bool_list):
                    target["thumb"]=self.thumb_list
                else:
                    target["thumb"]=[f for f in self.thumb_list if f.new]
            if nfo:
                bool_list=[f.new for f in self.nfo_list]
                if sum(bool_list)==0 or sum(bool_list)==len(bool_list):
                    target["nfo"]=self.nfo_list
                else:
                    target["nfo"]=[f for f in self.nfo_list if f.new]

        return target


    def rename_season(self,new:None|bool,vid:bool,sub:bool,thumb:bool,nfo:bool):
        print(f"Start renaming for season {self.season}:")

        target = self.get_target(new,vid,sub,thumb,nfo)
        if len(target['vid']) != len(self.vid_list) and self.start:
            raise ValueError(f"Option 'start' can't be used for mixed season in {self.path.name}")
        
        self.init_logger()

        statistics={}

        for k in target:
            if self.offset > 0:
                target[k].reverse()
            
            count=0
            for f in target[k]:
                count+=f.rename(self.name,self.season,self.offset)
            
            statistics[k]=count

        print(f"Rename season {self.season} finished\n")
        
        self.stats=statistics
        
    def init_logger(self):
        logger=logging.getLogger(f"Season {self.season}")
        file_handler = logging.FileHandler(self.path/"rename_history.log", mode="a", encoding="utf-8")
        logger.setLevel("DEBUG")
        #file_handler.setLevel("DEBUG")
        formatter = logging.Formatter("{asctime} {message}",style="{",datefmt="%Y-%m-%d %H:%M")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    def console_log(self):
        print(f"Season {self.season}:")
        
        if 'vid' in self.stats:
            print(f"Video : {self.stats['vid']}/{len(self.vid_list)}")
        if 'sub' in self.stats:
            print(f"Subtitle : {self.stats['sub']}/{len(self.sub_list)}")
        print("==============================================================")




def parse_args(args=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--path",default=".")
    parser.add_argument("-n","--name",help="TV show's name")
    parser.add_argument("--season",type=int)
    parser.add_argument("-m","--movie",action="store_true")
    parser.add_argument("--ep_regex",nargs='+',help="regex to match episode number")
    
    group1=parser.add_mutually_exclusive_group()
    group1.add_argument("-o",'--offset',type=int)
    group1.add_argument("--start",nargs="?",type=int,const=1)
    
    group2=parser.add_mutually_exclusive_group()
    group2.add_argument("--new",action="store_true",help="Include only new files")
    group2.add_argument('--all',action="store_true",help="Include all old files")
    
    parser.add_argument("--thumb",action="store_true",help="Include thumbnail")
    return parser.parse_args(args)

def main(args=None):
    args=parse_args(args)
    path=Path(args.path)

    ep_regex=cat_regex(args.ep_regex,EP_REGEX)

    new=None
    if args.new:
        new=True
    elif args.all:
        new=False

    

    if args.movie:
        pass
    else:
        season_obj_list=[]
        if season_list:=list(path.glob("Season */")):
            for season_path in season_list:
                s=SeasonFolder(season_path,ep_regex,args.name,args.season,args.offset,args.start)
                s.rename_season(new,True,True,args.thumb,False)
                season_obj_list.append(s)
        else:
            s=SeasonFolder(path,ep_regex,args.name,args.season,args.offset,args.start)
            s.rename_season(new,True,True,args.thumb,False)
            season_obj_list.append(s)
        
        for s in season_obj_list:
            s.console_log()
        

if __name__=="__main__":
    main()


        


        
        






            
            













        


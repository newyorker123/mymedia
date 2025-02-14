import re
from pathlib import Path

class SrtLine:
    def __init__(self,num,start:str,end:str,content:str):
        self.num=num
        self.start = start.strip()
        self.end = end.strip()
        self.content = content.strip()

    @staticmethod
    def parse_text(lines:str):
        lines=lines.strip().split("\n",2)
        num=int(lines[0])
        start = re.search(r".*?(?=-->)",lines[1]).group().strip()
        end = re.search(r"(?<=-->).*",lines[1]).group().strip()
        content =lines[2].strip()

        return num,start,end,content

    
    @classmethod
    def from_text(cls,lines:str):
        num,start,end,content = cls.parse_text(lines)
        return cls(num,start,end,content)

    @property    
    def text(self):
        return f"{self.num}\n{self.start} --> {self.end}\n{self.content}\n"
    
    @text.setter
    def text(self,lines:str):
        num,start,end,content=  self.parse_text(lines)
        self.num=num
        self.start = start
        self.end = end
        self.content = content

    def __repr__(self):
        return self.text



class SrtFile:
    def __init__(self,srt_list:list[SrtLine]|None=None,file=None):
        if srt_list is None:
            srt_list=[]

        self.srt_list=srt_list
        
        self.file=file
        if self.file is not None:
            self.file=Path(self.file.resolve())

    @property
    def num_of_lines(self):
        return len(self.srt_list)


    @classmethod
    def from_text(cls,text:str,file=None):
        srt_list=text.split("\n\n")
        return cls([SrtLine.from_text(line) for line in srt_list],file)
    
    @classmethod
    def from_file(cls,file_path:str|Path):
        with open(file_path,encoding='utf-8') as f:
            text=f.read()
        obj = cls.from_text(text,file_path)
        return obj
    
    @property
    def num_of_lines(self):
        return len(self.srt_list)
    
    def __getitem__(self,key):
        return self.srt_list[key]
    
    def add_line(self,start,end,content,num=None):
        if num is None:
            num= 1 if len(self.srt_list) == 0 else self.srt_list[-1].num+1

        self.srt_list.append(SrtLine(num,start,end,content))
    
    def output(self,dir='out',file_stem=None):
        text='\n'.join([srtline.text for srtline in self.srt_list])
        
        dir=Path(dir)
        dir.mkdir(exist_ok=True)

        if file_stem is None:
            if self.file is not None:
                file_stem=self.file.stem
            else: 
                raise FileNotFoundError("Please enter output file stem")

        with open(dir/f"{file_stem}.srt",'w') as f:
            f.write(text)

        

    



        



    



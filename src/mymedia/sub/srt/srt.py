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



class SrtFIle:
    def __init__(self,srt_list:list[SrtLine]|None=None):
        if srt_list is None:
            srt_list=[]

        self.srt_list=srt_list

    @property
    def num_of_lines(self):
        return len(self.srt_list)


    @classmethod
    def from_text(cls,text:str):
        srt_list=text.split("\n\n")
        return cls([SrtLine.from_text(line) for line in srt_list])
    
    @classmethod
    def from_file(cls,file_path:str|Path):
        with open(file_path) as f:
            text=f.read()
        return cls.from_text(text)
    
    @property
    def num_of_lines(self):
        return len(self.srt_list)
    
    def output(self,file_path):
        with open(file_path,'w') as f:
            f.write('\n'.join([srtline.text for srtline in self.srt_list]))

    



        



    



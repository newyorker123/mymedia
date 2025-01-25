import re
import json
from pathlib import Path
from typing import Sequence
import pytest 

from mymedia.video.rename_tv import main
from mymedia.video.utils import MYMEIDA_CONFIG,HISTORY

def create_standard_files(path:str|Path,name,season,ep_list:Sequence[int],log_list:Sequence[int],name_template):
    path=Path(path)

    for ep in ep_list:
        new_name=f"{name} S{season:02}E{ep:02}.mkv"
        (path/f"{new_name}").touch()
        if ep in log_list:
            create_history(path,name_template.format(num=ep),new_name)


@pytest.fixture(params=[
    pytest.param("[VCB-Studio] Boogiepop wa Warawanai [{num:02}][Ma10p_1080p][x265_flac].mkv",id="vcb"),
    pytest.param("[Moozzi2] NieR Automata Ver1.1a - {num:02} (BD 1920x1080 x265-10Bit FLACx2).mkv",id="Moozzi2")
]     
)
def name_template(request):
    return request.param

def create_config(path,name,season,offset=0):
    
    data={"name":name,"season":season,"offset":offset}
    with open(path/f"{MYMEIDA_CONFIG}",'w') as f:
        json.dump(data,f)

def read_config(path) -> dict:
    with open(path,"r") as f:
        data=json.load(f)
    return data

def compare_config(file1,file2):
    f1=read_config(file1)
    f2=read_config(file2)

    assert f1==f2

def create_history(path,original_name,new_name):
    with open(path/f"{HISTORY}","a") as f:
        f.write(f"\"{original_name}\" is renamed to \"{new_name}\"\n")

def read_history(path) -> dict:
    data={}

    with open(path,"r") as f:
        for line in f:
            match=re.search(r"\"(.*)\" is renamed to \"(.*)\"",line)
            data[match.group(1)]=match.group(2)
    return data 

def compare_history(file1,file2):
    f1=read_history(file1)
    f2=read_history(file2)

    assert f1==f2



def compare(path1:Path,path2:Path):
    file1=list(path1.iterdir())
    file1.sort()
    file2=list(path2.iterdir())
    file2.sort()

    assert len(file1)==len(file2)

    for f1,f2 in zip(file1,file2):
        assert f1.name==f2.name

        if f1.suffix == ".json":
            compare_config(f1,f2)
        elif f1.suffix == ".log":
            compare_history(f1,f2)



@pytest.fixture
def plain_all_new_path_with_name_folder(name_template,tmp_path):
    no_season_folder=(tmp_path/"actual"/"动漫名称 (2025)")
    no_season_folder.mkdir(parents=True)

    for i in range(1,13):
        ep_file=no_season_folder/(name_template.format(num=i))
        ep_file.touch()

    return no_season_folder

@pytest.fixture
def plain_all_new_path_with_name_folder_offset_12(name_template,tmp_path):
    no_season_folder=(tmp_path/"actual"/"动漫名称 (2025)")
    no_season_folder.mkdir(parents=True)

    for i in range(13,25):
        ep_file=no_season_folder/(name_template.format(num=i))
        ep_file.touch()

    return no_season_folder








class TestPlain:

    @staticmethod
    def expect_path(root_path,name_template,log_list):
        no_season_folder=(root_path/"expect"/"动漫名称 (2025)")
        no_season_folder.mkdir(parents=True)
        create_standard_files(no_season_folder,"动漫名称",1,range(1,13),log_list,name_template)
        create_config(no_season_folder,"动漫名称",1)
        return no_season_folder







    def test_renaname_all_new(self,plain_all_new_path_with_name_folder,tmp_path,monkeypatch,name_template):
        monkeypatch.chdir(plain_all_new_path_with_name_folder)
        main([])
        expect=self.expect_path(tmp_path,name_template,range(13))
        compare(plain_all_new_path_with_name_folder,expect)

    
    def test_renaname_all_new_offset_12(self,plain_all_new_path_with_name_folder,tmp_path,monkeypatch,name_template):
        monkeypatch.chdir(plain_all_new_path_with_name_folder)
        main(["--offset","-12"])
        expect=self.expect_path(tmp_path,name_template)
        compare(plain_all_new_path_with_name_folder,expect)

    




    
from pathlib import Path
import json
import pytest

from mymedia.video.utils import MYMEIDA_CONFIG,HISTORY

NO_NAME="[VCB-Studio] Boogiepop wa Warawanai [Ma10p_1080p]"
PATH_NAME="Path Name"
CONFIG_NAME="Config Name"
INPUT_NAME="Input Name"
CL_NAME="Cl Name"
CONFIG_SEASON=10
CL_SEASON=12
CONFIG_OFFSET=9
CL_OFFSET=12

def create_config(path,name,season,offset=0):
    
    data={"name":name,"season":season,"offset":offset}
    with open(path/f"{MYMEIDA_CONFIG}",'w') as f:
        json.dump(data,f)

# Folder structure that has no file in it

@pytest.fixture
def plain_with_name_no_config_nof(tmp_path):
    def _plain_with_name_no_config_nof(actual=True):
        """
        Parameter
        ===========
        actual:bool
            if True, in 'actual' folder. Or in 'expect folder'
        """
        if actual:
            root:Path=tmp_path/"actual"/f"{PATH_NAME} (2024)"
        else:
            root:Path=tmp_path/"expect"/f"{PATH_NAME} (2024)"

        root.mkdir(parents=True)
        return root
    
    return _plain_with_name_no_config_nof
    
@pytest.fixture
def plain_with_name_with_config_nof(tmp_path):
    def _plain_with_name_with_config_nof(actual=True):
        if actual:
            root:Path=tmp_path/"actual"/f"{PATH_NAME} (2024)"
        else:
            root:Path=tmp_path/"expect"/f"{PATH_NAME} (2024)"

        root.mkdir(parents=True)
        create_config(root,CONFIG_NAME,CONFIG_SEASON,CONFIG_OFFSET)

        return root
    
    return _plain_with_name_with_config_nof

@pytest.fixture
def plain_no_name_with_config_nof(tmp_path):
    def _plain_no_name_with_config_nof(actual=True):
        if actual:
            root:Path=tmp_path/"actual"/f"{NO_NAME}"
        else:
            root:Path=tmp_path/"expect"/f"{NO_NAME}"

        root.mkdir(parents=True)
        create_config(root,CONFIG_NAME,CONFIG_SEASON,CONFIG_OFFSET)

        return root
    
    return _plain_no_name_with_config_nof

@pytest.fixture
def plain_no_name_no_config_nof(tmp_path):
    def _plain_no_name_no_config_nof(actual=True):
        if actual:
            root:Path=tmp_path/"actual"/f"{NO_NAME}"
        else:
            root:Path=tmp_path/"expect"/f"{NO_NAME}"

        root.mkdir(parents=True)

        return root
    
    return _plain_no_name_no_config_nof


@pytest.fixture
def season_with_name_no_config_nof(tmp_path):
    def _season_with_name_no_config_nof(actual=True):
        """
        Parameter
        ===========
        actual:bool
            if True, in 'actual' folder. Or in 'expect folder'
        """
        if actual:
            root:Path=tmp_path/"actual"/f"{PATH_NAME} (2024)"
        else:
            root:Path=tmp_path/"expect"/f"{PATH_NAME} (2024)"

        root.mkdir(parents=True)
        
        (root/"Season 0").mkdir()
        (root/"Season 1").mkdir()
        (root/"Season 2").mkdir()

        
        return root
    
    return _season_with_name_no_config_nof




    




        
        
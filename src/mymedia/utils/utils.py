import re
import sys
from pathlib import Path

# def get_group(match):

#     if match is None:
#         raise ValueError(f"")
    
#     for f in match.groups():
#         if f:
#             return f 
        

def is_num(n:str):
    try:
        float(n)
    except ValueError:
        return False 
    else:
        return True


def convert_to_number(n:str):
    """Convert a number string to number

    n can be '2.1' or '2'.
    If n is '2.1', convert it to float 2.1
    If n is '2', convert it to int 2
    """
    if not is_num(n):
        raise ValueError(f"Can't conver {n} to number")

    if '.' in n:
        return float(n)
    else:
        return int(n)


def match_num(content:str,patterns:list[str]|str,type_=None):
    if isinstance(patterns,str):
        patterns=[patterns]

    for pattern in patterns:
        match = re.search(pattern,content)
        if match:
            return convert_to_number(match.group(1))
    
    type_= 'number' if type_ is None else type_
    return raise_match_error(content,type_,'num',True)


def match_string(content:str,patterns:list[str],type_=None):
    if isinstance(patterns,str):
        patterns=[patterns]

    for pattern in patterns:
        match = re.search(pattern,content)
        if match:
            return match.group(1)
    
    type_='string' if type_ is None else type_
    return raise_match_error(content,type_,'str',True)




def raise_match_error(content:str,type_,out_type,input_=True,extra_message=None):
    """
    Parameters
    ----------
    content : str
              The content to be matched, e.g. file.name
    
    type_ : str
            The content type, e.g. volume,chapter,title. Used in help message.
    
    out_type :str
              'num' or 'str'. Used to convert user input

    """

    print(f"Can't match {type_} for {content}")
    if input_:
        if extra_message:
            res=input(f"Please enter {type_}({extra_message}, -1 to exit):")
        else:
            res=input(f"Please enter {type_}(-1 to exit):")
        if res == '-1':
            sys.exit()

        if out_type == 'num':
            res=convert_to_number(res)

        return res
    else:
        raise ValueError(f"Can't match {type_} for {content}")
    

# def file_sort(file:Path):
#     num=re.search(r"\d+(_\d+)?",file.stem).group()
#     num=re.sub('_',".",num)
#     try:
#         num=float(num)
#     except ValueError:
#         ValueError(f"Can't sort file {file.name} because the finename is't number")
#     return num


def cat_regex(regex,regex_list:list[str]):
    if (regex is None or regex == ""):
        return regex_list
    elif isinstance(regex,list):
        return regex+regex_list
    elif isinstance(regex,str):
        return [regex] + regex_list
    else:
        raise ValueError('regex must be str or list')

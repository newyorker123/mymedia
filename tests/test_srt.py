from pathlib import Path
import pytest

from mymedia.sub.srt import SrtLine

@pytest.fixture
def srt_file():
    with open('tests/data/test_srt.srt') as f:
        res=f.read()
    return res

def test_SrtLine(srt_file):

    srt_lines=srt_file.split("\n\n")
    srt_objs=[SrtLine(l) for l in srt_lines]
    
    assert srt_objs[0].num==1
    assert srt_objs[0].start=="00:00:00,500"
    assert srt_objs[0].end=="00:00:01,500"
    assert srt_objs[0].content=="平匡先生"

    assert srt_objs[1].num==2
    assert srt_objs[1].start=="00:00:00,500"
    assert srt_objs[1].end=="00:00:01,500"
    assert srt_objs[1].content=="平匡さん"

    assert srt_objs[2].num==3
    assert srt_objs[2].start=="00:00:02,500"
    assert srt_objs[2].end=="00:00:04,400"
    assert srt_objs[2].content=="你能当我的男朋友吗"

    assert srt_objs[3].num==4
    assert srt_objs[3].start=="00:00:02,500"
    assert srt_objs[3].end=="00:00:04,400"
    assert srt_objs[3].content=="私の恋人になってもらえませんか？"

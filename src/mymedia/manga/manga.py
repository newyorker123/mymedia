import re

digit=r"\d+(\.\d+)?"

VOL_REGEX=[
    fr"Vol[._]({digit})",
    fr"第({{digit}})[卷集]",
    fr"\({digit}\)",
    fr"\s({digit})",
]

CHAP_REGEX=[
    fr"Chap[._]({digit})",
    fr"第({{digit}})[章话]",
]





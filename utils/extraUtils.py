from random import shuffle
from enum import Enum

class Status(Enum):
    SUCCESS = 1
    ERROR = 0
    DUPLICATE = 2

def shuffle_str(s: str) -> str:
    lst = []
    for char in s:
        lst.append(char)
    shuffle(lst)
    suffled_str = ''.join(lst)
    return suffled_str
if __name__ == '__main__':
    print(shuffle_str('OláAmigo'))

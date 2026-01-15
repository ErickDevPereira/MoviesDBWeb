from random import shuffle
from enum import Enum
from typing import List

class Status(Enum):
    SUCCESS = 1
    ERROR = 0
    DUPLICATE = 2
    DELETION = 3

class Vote(Enum):
    LIKE = "UP"
    UNLIKE = "DOWN"

def shuffle_str(s: str) -> str:
    lst = []
    for char in s:
        lst.append(char)
    shuffle(lst)
    suffled_str = ''.join(lst)
    return suffled_str

def translate(lst: List[float | int]) -> List[str]:

    new_lst = []
    for item in lst:

        if item != 0 and item != 0.5 and item != 1:
            raise ValueError("The values inside the list can be one of the following:\n0\n0.5\n1\nNothing else!")

        if item == 0:
            new_lst.append("empty_star")
        elif item == 0.5:
            new_lst.append("half_star")
        else:
            new_lst.append("full_star")
    
    return new_lst

if __name__ == '__main__':
    print(translate([0.5, 0, 1]))

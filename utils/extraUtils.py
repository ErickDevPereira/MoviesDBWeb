from random import shuffle
from enum import Enum
from typing import List

class Status(Enum):
    SUCCESS: int = 1
    ERROR: int = 0
    DUPLICATE: int = 2
    DELETION: int = 3

class Vote(Enum):
    LIKE: str = "UP"
    UNLIKE: str = "DOWN"

def shuffle_str(s: str) -> str:

    """
    Explanation:
    This function shuffles a string and returns it afterwards.
    
    Parameters:
    s: string to be shuffled.
    """

    lst: List[str] = []
    for char in s:
        lst.append(char)
    shuffle(lst)
    suffled_str: str = ''.join(lst)
    return suffled_str

def translate(lst: List[float | int]) -> List[str]:

    """
    Explanation:
    This function transform a list with 0.5, 0 and 1 into a list that gives meaning to each of these values,
    then it returns such list. For example [0, 0.5, 1, 1] as input will output [empty_star, half_star, full_star, full_star].
    This function is part of the proccess that generates the figure with stars that represent the average score of a user.

    Parameters:
    lst: list with the numbers 0, 0.5 or 1.
    """

    new_lst: List[str] = []
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

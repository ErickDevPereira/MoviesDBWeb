from random import shuffle
def shuffle_str(s: str) -> str:
    lst = []
    for char in s:
        lst.append(char)
    shuffle(lst)
    suffled_str = ''.join(lst)
    return suffled_str
if __name__ == '__main__':
    print(shuffle_str('OláAmigo'))

import os
from typing import Tuple

def load_src_db(username: str, password: str) -> None:
    FILE = open('src/SrcDbKey.txt', 'w')
    FILE.write('Username:\n' + username + '\nPassword:\n' + password)
    FILE.close()

def del_src_db() -> None:
    if os.path.exists('src/SrcDbKey.txt'):
        os.remove('src/SrcDbKey.txt')
        print('The key to enter on the Database was deleted in order to protect the database.')
    else:
        print("Can't find the file")

def load_src_google() -> Tuple[str, str]:
    FILE = open('src/google_keys.txt', 'r')
    lst = FILE.readlines()
    client_id = lst[1][:-1]
    secret_id = lst[-1][:]
    FILE.close()
    return client_id, secret_id

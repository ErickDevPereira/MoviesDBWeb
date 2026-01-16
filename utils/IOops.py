import os
from typing import Tuple, Any, List

def load_src_db(username: str, password: str) -> None:
    """
    Explanation:
    This function will write the username and password of your MySQL account
    inside a file that is placed at src directory.

    Parameters:
    username: name of the MySQL account's user
    password: password to your MySQL account
    """
    FILE: Any = open('src/SrcDbKey.txt', 'w')
    FILE.write('Username:\n' + username + '\nPassword:\n' + password)
    FILE.close()

def del_src_db() -> None:
    """
    Explanation:
    This function will delete the file with your MySQL account data (username and password).
    This function must be called when the web server is OFF.
    """
    if os.path.exists('src/SrcDbKey.txt'):
        os.remove('src/SrcDbKey.txt')
        print('The key to enter on the Database was deleted in order to protect the database.')
    else:
        print("Can't find the file")

def load_src_google() -> Tuple[str, str]:

    """
    Explanation:
    This function will read the client and secret id from a file inside the src directory and
    return such strings inside a tuple.
    """

    FILE: Any = open('src/google_keys.txt', 'r')
    lst: List[str] = FILE.readlines()
    client_id: str = lst[1][:-1]
    secret_id: str = lst[-1][:]
    FILE.close()
    return client_id, secret_id

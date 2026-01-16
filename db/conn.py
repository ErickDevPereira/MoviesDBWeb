import mysql.connector as conn
from typing import Any, List

def my_connection() -> Any:

    """
    Explanation:
    This function stablishes a connection between Python and the database inside
    MySQL, then it returns it.
    """

    FILE: Any = open('src/SrcDbKey.txt', 'r')
    txt_list: List[str] = FILE.readlines()
    username: str = txt_list[1][:-1]
    password: str = txt_list[-1]
    db: Any = conn.connect(
        user = username,
        password = password,
        host = 'localhost',
        database = 'MoviesDB'
    )
    return db
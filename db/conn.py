import mysql.connector as conn
from typing import Any

def my_connection() -> Any:
    FILE = open('src/SrcDbKey.txt', 'r')
    txt_list = FILE.readlines()
    username = txt_list[1][:-1]
    password = txt_list[-1]
    db: Any = conn.connect(
        user = username,
        password = password,
        host = 'localhost',
        database = 'MoviesDB'
    )
    return db
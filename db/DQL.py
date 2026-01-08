from typing import Any, Tuple, List
from werkzeug.security import check_password_hash

def validate_user(db: Any, username: str, password: str) -> bool:

    """
    Explanation:
    This function returns True if the given username and password are found inside
    a record in the Users table.

    Parameters:
    db: database connection object.
    username: Nickname of the user.
    password: password without cryptograph over it.
    """

    cursor = db.cursor()
    cursor.execute("""
                SELECT
                    username, password
                FROM
                    Users
                WHERE
                    username = %s
                """, (username,))
    get_people = cursor.fetchall()
    cursor.close()
    if len(get_people) > 0:
        if check_password_hash(get_people[0][1], password):
            return True #This username and password exists in the database for the same record.
    return False #This username and passowrd aren't present inside the database.

def check_if_user_exists(db: Any, username: str) -> bool:

    """
    Explanation:
    The function returns True if such user exists in the table Users,
    but returns False otherwise.

    Parameters:
    db : connection to the data base
    username : Nickname of the user
    """

    cursor: Any = db.cursor()
    cursor.execute("""
                SELECT
                    username
                FROM
                    users
                WHERE
                    username = %s
                    """, (username,))
    data: List[Tuple[str]] = cursor.fetchall()
    if len(data) > 0:
        return True
    return False

def get_id(db: Any, username: str) -> int:

    """
    Explanation:
    This function receives a connection object and a username and, as response,
    retrieves the id of that user if it exists, but return -1 otherwise.

    Parameters:
    db: Connection to MySQL
    username: Nickname of the user
    """

    is_there_a_user: bool = check_if_user_exists(db, username)
    if is_there_a_user:
        cursor: Any = db.cursor()
        cursor.execute(
            """
                SELECT
                    user_id
                FROM
                    Users
                WHERE
                    username = %s
            """,
            (username,))
        id: int =  cursor.fetchall()[0][0]
        cursor.close()
        return id
    return -1

if __name__ == '_main__':
    print(get_id('Erick001'))
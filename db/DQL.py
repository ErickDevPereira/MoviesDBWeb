from typing import Any, Tuple, List, Dict
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

def get_by_id(db: Any, user_id: int) -> Dict[str, str] | None:
    """
    Explanation:
    The inputs are a connection to database and the id of the user. Such function
    returns information about that user throughout a dictionary.

    Parameters:
    db: Connection to MySQL
    user_id: id of a user as integer
    """
    cursor = db.cursor()
    cursor.execute("""
                SELECT
                    username, email, phone
                FROM
                   users
                WHERE
                    user_id = %s   
            """, (user_id,))
    dirt_info = cursor.fetchall()
    if len(dirt_info) == 0:
        return None #Case at which the id doesn't exist inside the database
    info = {'username': dirt_info[0][0], 'email': dirt_info[0][1], 'phone': dirt_info[0][2]}
    return info

def get_movies_by_user(db: Any, user_id: int) -> Dict[str, str]:

    cursor = db.cursor()
    cursor.execute("""
                SELECT
                    imdb_id, title, release_date, runtime, imdbRating, genre, director
                FROM
                    movie_info AS i INNER JOIN movie_people AS p
                    ON i.movie_id = p.movie_id
                WHERE
                    i.user_id = %s
            """, (user_id,))
    dataset = cursor.fetchall()
    cursor.close()
    """for row in range(0, len(dataset)):
        for col in range(0, len(dataset[0])):
            if dataset[row][col] is None:
                dataset[row][col] = 'Undefined'"""
    organized_dataset = [
        {
        "imdb_id" : dataset[i][0],
        "title": dataset[i][1],
        "release_date": dataset[i][2],
        "runtime": dataset[i][3],
        "imdbRating": dataset[i][4],
        "genre": dataset[i][5],
        "director": dataset[i][6]
        } for i in range(0, len(dataset))
    ]
    return organized_dataset

def get_title_by_imdb(db: Any, imdb_id: str) -> str | None:

    cursor = db.cursor()
    cursor.execute("SELECT title FROM movie_info WHERE imdb_id = %s",
                   (imdb_id,))
    lst = cursor.fetchall()
    cursor.close()
    if len(lst) > 0:
        title = lst[0][0]
        return title
    return None

def user_has_movie(db: Any, title: str, user_id: int) -> bool:

    cursor = db.cursor()
    cursor.execute("SELECT title FROM movie_info WHERE user_id = %s AND title = %s",
                   (user_id, title))
    dataset = cursor.fetchall()
    cursor.close()
    return len(dataset) > 0

def get_comment_by_imdb(db: Any, imdb_id: str) -> List[Dict[str, str]]:

    cursor = db.cursor()
    cursor.execute("""
                SELECT
                   c.comment_id,
                   u.username,
                   u.email,
                   c.date,
                   c.text
                FROM
                    users AS u INNER JOIN comments AS c
                    ON u.user_id = c.user_id
                WHERE
                    c.imdb_id = %s""",
                (imdb_id,))
    dataset = cursor.fetchall()
    cursor.close()
    organized_dataset = [{
        "comment_id": dataset[i][0],
        "username" : dataset[i][1],
        "email" : dataset[i][2],
        "date" : dataset[i][3],
        "text" : dataset[i][4]
    } for i in range(len(dataset))]
    return organized_dataset

def get_imdb_by_comment(db: Any, comment_id: int) -> str | None:

    cursor = db.cursor()
    cursor.execute("""
                SELECT
                    imdb_id
                FROM
                    comments
                WHERE
                    comment_id = %s
            """,(comment_id,))
    data = cursor.fetchall()
    if len(data) > 0:
        return data[0][0]
    return None

def user_has_upvoted(db: Any, comment_id: int, user_id: int) -> bool:

    """
    Explanation:
    Given a comment ID and a user ID, the function returns True if
    that comment has a like from that user, False otherwise.
    
    Parameters:
    db: connection to the database.
    comment_id: ID of the comment to be analyzed.
    user_id: ID of the user that possibly liked that comment
    """

    cursor = db.cursor()
    cursor.execute("""
                SELECT
                    vote
                FROM
                    comments AS c INNER JOIN votes AS v
                    ON c.comment_id = v.comment_id
                WHERE
                    c.comment_id = %s AND v.user_id = %s
                """,
                (comment_id, user_id))
    data = cursor.fetchall()
    cursor.close()

    if len(data) == 0:
        return False #That user didn't voted on the comment
    
    if data[0][0] == "UP":
        return True #That user gave a thumb up on the comment.
    
    return False

def user_has_downvoted(db: Any, comment_id: int, user_id: int) -> bool:

    """
    Explanation:
    Given a comment ID and a user ID, the function returns True if
    that comment has an unlike from that user, False otherwise.
    
    Parameters:
    db: connection to the database.
    comment_id: ID of the comment to be analyzed.
    user_id: ID of the user that possibly liked that comment
    """

    cursor = db.cursor()
    cursor.execute("""
                SELECT
                    vote
                FROM
                    comments AS c INNER JOIN votes AS v
                    ON c.comment_id = v.comment_id
                WHERE
                    c.comment_id = %s AND v.user_id = %s
                """, (comment_id, user_id))
    data = cursor.fetchall()
    cursor.close()

    if len(data) == 0:
        return False #That user didn't voted on the comment
    
    if data[0][0] == "DOWN":
        return True #That user gave a thumb up on the comment.
    
    return False

def votes_per_comment(db: Any, comment_id: int, option: int = 1) -> int:

    """
    Explanation:
    Given a comment_id, the function returns the number of down_votes if the option is 0, the number of up_votes if the option is 1
    for that given comment.

    Parameters:
    db: is the connection to the database.
    comment_id: id of the comment that will be analized.
    option: 0 applies the filter over the Down votes while 1 applies that filter over the Up votes.
    """

    cursor = db.cursor()
    cursor.execute("""
                SELECT
                    COUNT(v.vote)
                FROM
                    comments AS c INNER JOIN votes AS v
                    ON c.comment_id = v.comment_id
                WHERE
                    c.comment_id = %s
                GROUP BY
                    v.vote
                HAVING
                    v.vote = %s
                """, (comment_id, "UP" if option == 1 else "DOWN"))
    data = cursor.fetchall()
    cursor.close()
    if len(data) == 0:
        return 0
    else:
        return data[0][0]

if __name__ == '_main__':
    print(get_id('Erick001'))
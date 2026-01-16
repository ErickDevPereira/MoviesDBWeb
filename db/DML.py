from typing import Any, List, Tuple

def load_user(db: Any, username: str, password: str, email: str, phone: str) -> None:
    """
    Explanation:
    This function inserts a user on the database.

    Parameters:
    db: connection to the database inside MySQL.
    username: name of the user
    password: password of the user in Werkzeug.
    email: user's email.
    phone: phone number of that user.
    """
    cursor: Any = db.cursor()
    cursor.execute('''INSERT INTO users (username, password, email, phone) VALUES
                   (%s, %s, %s, %s)''', (username, password, email, phone)) #The id of the user will be created by MySQL.
    db.commit()
    cursor.close()

def load_movie(db: Any,
                user_id: int,
                imdb_id: str,
                title: str,
                type_: str,
                release_date: str,
                runtime: int,
                description: str,
                genre: str,
                imdbRating: float,
                actors: str,
                director: str,
                writer: str) -> None:
    
    """
    Explanation:
    This function will load a movie into the database.
    movie_info and movie_people will be loaded with the dataset that comes from the
    parameters.

    parameters:
    db: connection to the database inside MySQL.
    the other parameters will receive data about a movie.
    """

    def cleanDate(string_date: str) -> str:

        """
        Explanation:
        This function will take a date in the format 16 Jan 2026 and return it as 2026-01-16.
        This is important because date is stored in MySQL with the format "YYYY-MM-DD"
        
        Parameter:
        string_date: date with format DD Month YYYY
        
        Return:
        date as string in the format "YYYY-MM-DD"
        """

        if not isinstance(string_date, str):
            raise ValueError("The 'string_date' argument must be string")

        try:
            lst: List[str] = string_date.split()
            month: str = lst[1]
            new_month: str | None = None
            match month:
                case 'Jan':
                    new_month = '01'
                case 'Feb':
                    new_month = '02'
                case 'May':
                    new_month = '03'
                case 'April' | 'Ap' | 'Apr':
                    new_month = '04'
                case 'March' | 'Mar':
                    new_month = '05'
                case 'Jun':
                    new_month = '06'
                case 'July' | 'Jul':
                    new_month = '07'
                case 'Aug':
                    new_month = '08'
                case 'Sep':
                    new_month = '09'
                case 'Oct':
                    new_month = '10'
                case 'Nov':
                    new_month = '11'
                case 'Dec':
                    new_month = '12'
            
            new_date: str = lst[2] + '-' + new_month + '-' + lst[0]
            return new_date
        except:
            return '1850-10-10'

    cursor: Any = db.cursor()
    cursor.execute(
        """
            INSERT INTO movie_info (user_id, imdb_id, title, type, release_date, runtime, description, genre, imdbRating)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, imdb_id, title, type_, cleanDate(release_date), runtime, description, genre, imdbRating))
    db.commit()
    cursor.close()
    cursor: Any = db.cursor()
    cursor.execute('SELECT movie_id FROM movie_info ORDER BY movie_id DESC LIMIT 1')
    dataset: List[Tuple[int, ...]] = cursor.fetchall()
    movie_id: int = dataset[0][0]
    cursor.close()
    cursor: Any = db.cursor()
    cursor.execute(
        """
        INSERT INTO movie_people (movie_id, actors, director, writer)
        VALUES (%s, %s, %s, %s)
        """, (movie_id, actors, director, writer)
    )
    db.commit()
    cursor.close()

def remove_movie(db: Any, user_id: int, imdb_id: str) -> None:

    """
    Explanation:
    You give the db connection, user_id and the imdb code to the movie, then that movie with that
    code will be deleted from the account of that given user.

    Parameters:
    user_id : id of the user that will suffer the operation
    imdb_id : id of the movie that will be removed.
    """

    cursor: Any = db.cursor()
    cursor.execute("SELECT movie_id FROM movie_info WHERE imdb_id = %s AND user_id = %s",
                   (imdb_id, user_id))
    movie_id: List[Tuple[str,...]] = cursor.fetchall()[0][0]
    cursor.close()
    cursor: Any = db.cursor()
    cursor.execute("DELETE FROM movie_people WHERE movie_id = %s", (movie_id,))#Deleting from the extended table
    db.commit()
    cursor.close()
    cursor: Any = db.cursor()
    cursor.execute("DELETE FROM movie_info WHERE movie_id = %s", (movie_id,))#Deleting from the mother table
    db.commit()
    cursor.close()

def load_comment(db: Any, user_id: int, imdb_id: str, text: str) -> None:

    """
    Explanation:
    This function is responsible for loading a a comment inside the comment table.
    parameters:
    db: connection to the database.
    user_id: id of the user that made that comment
    imdb_id: imdb code of the movie that received such comment.
    text: text of the comment.
    """

    cursor: Any = db.cursor()
    cursor.execute("INSERT INTO comments (user_id, text, imdb_id) VALUES (%s, %s, %s)",
                   (user_id, text, imdb_id))
    db.commit()
    cursor.close()

def load_vote_on_db(db: Any, user_id: int, comment_id: int, vote: str) -> None:

    """
    Explanation:
    This function is responsible for inserting a vote on the votes table.

    parameters:
    db: connection to the database.
    user_id: id of the user that voted.
    comment_id: id of the comment that was voted.
    vote: type of vote (UP is a like and DOWN is dislike)
    """

    cursor: Any = db.cursor()
    cursor.execute("INSERT INTO votes (user_id, comment_id, vote) VALUES (%s, %s, %s) ",
                   (user_id, comment_id, vote))
    db.commit()
    cursor.close()

def update_vote(db: Any, user_id: int, comment_id: int, new_vote: str) -> None:

    """
    Explanation:
    This function will flip a vote for a comment given by a user.

    parameters:
    db: connection to the database.
    user_id: id of the user that changed its vote.
    comment_id: id of the comment that received that action.
    new_vote: the new vote itself (can be UP or DOWN).
    """

    cursor: Any = db.cursor()
    cursor.execute("""
                    UPDATE
                        votes
                    SET
                        vote = %s
                    WHERE
                        comment_id = %s AND user_id = %s
                    """, (new_vote, comment_id, user_id))
    db.commit()
    cursor.close()

def delete_vote(db: Any, user_id: int, comment_id: int) -> None:

    """
    Explanation:
    It will delete a vote for a user over a comment.

    parameters:
    db: connection to the database
    user_id: id of the user that wants to take out his/her vote.
    comment_id: id of the comment that suffered the action.
    """

    cursor: Any = db.cursor()
    cursor.execute("DELETE FROM votes WHERE comment_id = %s AND user_id = %s", (comment_id, user_id))
    db.commit()
    cursor.close()
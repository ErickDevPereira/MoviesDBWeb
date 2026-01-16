import mysql.connector as conn
from typing import Any, List

def run_database(password: str, username: str = 'root') -> None:

    """
    Explanation:
    This function will create the database 'moviedb' in MySQL if it doesn't exist,
    create the tables if they don't exist and create the indexes if they don't exist.
    If a specific table or index don't exist while the others are over the database, then
    the tables and indexes that are lacking on the application will be created.

    Parameters:
    password: password to your MySQL server.
    username: username to your MySQL server (the name is probably 'root')
    """

    db: Any = conn.connect(
        user = username,
        password = password,
        host = 'localhost'
    )
    cursor: Any = db.cursor()
    cursor.execute('CREATE DATABASE if not exists moviesdb') #Creating the database
    cursor.close()
    db.close()
    db: Any = conn.connect(
        user = username,
        password = password,
        host = 'localhost',
        database = 'moviesdb'
    ) #Creating a connection to the database moviesdb
    cursor: Any = db.cursor()
    cursor.execute("""
                    CREATE TABLE if not exists users (
                        user_id INT PRIMARY KEY AUTO_INCREMENT,
                        username VARCHAR(64) NOT NULL UNIQUE,
                        password VARCHAR(1024) NOT NULL,
                        email VARCHAR(256) NOT NULL,
                        phone VARCHAR(30),
                        CONSTRAINT email_validator CHECK ( email LIKE '%_@_%.com' ),
                        CONSTRAINT username_validator CHECK (LENGTH(username) > 3 AND LENGTH(username) < 65),
                        CONSTRAINT phone_validator CHECK( LENGTH(phone) > 3 AND LENGTH(phone) < 31 ),
                        CONSTRAINT only_one_user UNIQUE( username )
                   )
                    """)
    cursor.close()
    cursor: Any = db.cursor()
    cursor.execute("""
                CREATE TABLE if not exists movie_info (
                    movie_id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    imdb_id VARCHAR(20) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    type VARCHAR(255),
                    release_date DATE NOT NULL,
                    runtime INT,
                    description VARCHAR(5000),
                    genre VARCHAR(255),
                    imdbRating DECIMAL(3,1) NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES Users (user_id),
                    UNIQUE (user_id, imdb_id)
                )
                    """) #User_id is the user that inserted this movie over here
    cursor.close()
    cursor: Any = db.cursor()
    cursor.execute("""
                CREATE TABLE if not exists movie_people (
                    movie_id INT NOT NULL,
                    actors VARCHAR(128),
                    director VARCHAR(128),
                    writer VARCHAR(128),
                    FOREIGN KEY (movie_id) REFERENCES Movie_info ( movie_id )
                )
                    """) #This table is an extension of the movie_info table
    cursor.close()
    cursor: Any = db.cursor()
    cursor.execute("""
                CREATE TABLE if not exists comments (
                    comment_id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    text VARCHAR(1500) NOT NULL,
                    imdb_id VARCHAR(20),
                    date DATETIME DEFAULT NOW(),
                    FOREIGN KEY ( user_id ) REFERENCES Users ( user_id )
                )
                    """)
    cursor.close()
    cursor: Any = db.cursor()
    cursor.execute("""
                CREATE TABLE if not exists votes (
                    vote_id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    comment_id INT NOT NULL,
                    vote ENUM("UP", "DOWN") NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES Users (user_id),
                    FOREIGN KEY (comment_id) REFERENCES Comments (comment_id),
                    UNIQUE (user_id, comment_id)
                )
                    """) #User_id is the user that voted and comment_id is the id of the comment at which that vote was applied.
    cursor.close()
    SQLs: List[str] = [
            'CREATE INDEX ind1 ON users (username, password)',
            'CREATE INDEX ind2 ON movie_info (user_id, runtime)',
            'CREATE INDEX ind3 ON movie_info (user_id, imdbRating)',
            'CREATE INDEX ind4 ON movie_info (user_id, title)',
            'CREATE INDEX ind5 ON movie_info (imddb_id)'
            ] #These indexes will be responsible for speeding up somes queries
    for sql in SQLs: #This loop will produce the indexes.
        try:
            cursor: Any = db.cursor()
            cursor.execute(sql)
            cursor.close()
        except conn.errors.ProgrammingError:
            pass
        except Exception as err:
            print(err)
    db.close()

if __name__ == '__main__':
    run_database('Ichigo007*')
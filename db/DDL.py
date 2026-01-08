import mysql.connector as conn
from typing import Any

def run_database(password: str, username: str = 'root') -> None:

    db: Any = conn.connect(
        user = username,
        password = password,
        host = 'localhost'
    )
    cursor: Any = db.cursor()
    cursor.execute('CREATE DATABASE if not exists MoviesDB')
    cursor.close()
    db.close()
    db: Any = conn.connect(
        user = username,
        password = password,
        host = 'localhost',
        database = 'MoviesDB'
    )
    cursor: Any = db.cursor()
    cursor.execute("""
                    CREATE TABLE if not exists Users (
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
    try:
        cursor = db.cursor()
        cursor.execute('CREATE INDEX faster_user_verification_index ON Users (username, password)')
        cursor.close()
    except conn.errors.ProgrammingError:
        pass
    except Exception as err:
        print(err)
    finally:
        db.close()

if __name__ == '__main__':
    run_database('Ichigo007*')
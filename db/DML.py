from typing import Any, List, Tuple

def load_user(db: Any, username: str, password: str, email: str, phone: str) -> None:
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Users (username, password, email, phone) VALUES
                   (%s, %s, %s, %s)''', (username, password, email, phone))
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
    
    def cleanDate(string_date: str) -> str:

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
            INSERT INTO Movie_info (user_id, imdb_id, title, type, release_date, runtime, description, genre, imdbRating)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, imdb_id, title, type_, cleanDate(release_date), runtime, description, genre, imdbRating))
    db.commit()
    cursor.close()
    cursor: Any = db.cursor()
    cursor.execute('SELECT movie_id FROM Movie_info ORDER BY movie_id DESC LIMIT 1')
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
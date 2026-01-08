from typing import Any

def load_user(db: Any, username: str, password: str, email: str, phone: str) -> None:
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Users (username, password, email, phone) VALUES
                   (%s, %s, %s, %s)''', (username, password, email, phone))
    db.commit()
    cursor.close()
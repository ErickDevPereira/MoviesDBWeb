import requests
from typing import Dict, Any

def get_data_by_title(title: str) -> None | Dict[str, str | int | None | float]:
    """
    This function receives a title of a movie. If the status of the request is different from 200 (like when
    the server of the API is off or when you're without internet) the return will be None; if the status is 200, but
    that movie wasn't found on the API database then the returned value will also be None; If the status is 200 and that 
    movie is found, then the return will be the data about the movie as a dictionary.
    """
    def check_invalid_values(message: str) -> None | str:
        """
        This function receives a message as string and returns that message if it is not "N/A", but return None otherwise.
        """
        if message == 'N/A':
            return None
        return message

    if not isinstance(title, str):
        raise ValueError('THE TITLE MUST BE A STRING!')

    URL: str = 'http://www.omdbapi.com/'
    key: str = '118afbf0'
    response: requests.Response = requests.get(URL, params = {'apikey' : key, 't' : title})
    if response.status_code == 200:
        full_data: Any = response.json()
        if full_data['Response'] == 'True': #If status is 200, response can be either true or false: true if the movie was found, false otherwise.
            filtered_data: Dict[str, str | int | None | float] = {
                'imdbID': check_invalid_values(full_data['imdbID']),
                'Title': check_invalid_values(full_data['Title']),
                'Released': check_invalid_values(full_data['Released']),
                'Runtime': int(full_data['Runtime'].split()[0]) if check_invalid_values(full_data['Runtime']) is not None else None, # Initially, the data was on the format xyz min as string, now it will be xyz as int
                'Genre': check_invalid_values(full_data['Genre']),
                'Director': check_invalid_values(full_data['Director']),
                'Writer': check_invalid_values(full_data['Writer']),
                'Actors': check_invalid_values(full_data['Actors']),
                'Description': check_invalid_values(full_data['Plot']),
                'Language': check_invalid_values(full_data['Language']),
                'Image': check_invalid_values(full_data['Poster']),
                'imdbRating': float(full_data['imdbRating']) if check_invalid_values(full_data['imdbRating']) is not None else None,
                'Type': check_invalid_values(full_data['Type'])
            }
            return filtered_data
        return None #Movie not found, so None is returned
    return None #Response is different from 200, so None is returned.

if __name__ == '__main__':
    print(get_data_by_title('Elit Squad'))
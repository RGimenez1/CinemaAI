import json
from app.services.movie_service import search_movies


class CallableFunctions:
    """
    A class to handle callable functions with JSON string arguments.
    """

    def __init__(self):
        """
        Initialize the CallableFunctions class.
        """
        pass  # No parameters needed for initialization

    def _parse_params(self, params):
        """
        Parse the parameters string to a JSON dictionary.
        Assumes the input is always a valid JSON string.
        """
        try:
            return json.loads(params)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")

    async def movie_searcher(self, arguments):
        """
        Searches for movies based on the given arguments.
        Arguments are passed as a JSON string.
        """
        params = self._parse_params(arguments)
        title = params.get("title")
        genres = params.get("genres")
        year = params.get("year")
        director = params.get("director")
        cast_member = params.get("cast_member")

        movies = await search_movies(title, genres, year, director, cast_member)

        # Call the search_movies function with the resolved parameters
        # message_service.add_message(Roles.FUNCTION, json.dumps(movies))
        # await message_service.commit()

        movies = [movie.to_dict() for movie in movies]
        print(f"movies: {movies}")

        return movies

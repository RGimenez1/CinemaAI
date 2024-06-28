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

    def _parse_params(self, params: str) -> dict:
        """
        Parse the parameters string to a JSON dictionary.
        Assumes the input is always a valid JSON string.
        """
        try:
            return json.loads(params)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")

    async def movie_searcher(self, arguments: str):
        """
        Searches for movies based on the given arguments.
        Arguments are passed as a JSON string.
        """
        params = self._parse_params(arguments)
        print(f"Movie Searcher Arguments: {params}")
        title = params.get("title")
        genres = params.get("genres")
        year = params.get("year")
        director = params.get("director")
        cast_member = params.get("cast_member")
        countries = params.get("countries")
        imdb_rating = params.get("imdb_rating")
        oscars = params.get("oscars")
        best_actor = params.get("best_actor")

        movies = await search_movies(
            title,
            genres,
            year,
            director,
            cast_member,
            countries,
            imdb_rating,
            oscars,
            best_actor,
        )

        if not movies:
            return "No movies found. Ask the user if you could help find another movie."

        return [movie.to_dict() for movie in movies]

    async def execute_tool(self, function_name: str, arguments: str):
        """
        Executes the specified tool function with the given arguments.
        """
        try:
            # Dynamically get the method from the instance using function_name
            tool_function = getattr(self, function_name, None)
            if tool_function and callable(tool_function):
                # Call the tool function with the provided arguments
                return await tool_function(arguments)
            else:
                raise ValueError(f"Tool function '{function_name}' not found.")
        except Exception as e:
            return {"error": str(e)}

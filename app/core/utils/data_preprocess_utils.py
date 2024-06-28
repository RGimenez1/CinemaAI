from typing import Any


def clean_data(data: Any) -> Any:
    """
    Recursively clean data by converting empty strings to None. This function ensures
    that dictionaries and lists within the data are also processed to handle empty strings.

    Args:
        data (Any): The data to be cleaned. This can be of any type, but the function
                    specifically processes dictionaries, lists, and strings.

    Returns:
        Any: The cleaned data, with empty strings converted to None.
    """
    # If the data is a dictionary, recursively clean its values
    if isinstance(data, dict):
        return {k: clean_data(v) for k, v in data.items()}

    # If the data is a list, recursively clean its elements
    elif isinstance(data, list):
        return [clean_data(item) for item in data]

    # If the data is an empty string, convert it to None
    elif data == "":
        return None

    # Return the data unchanged if it does not match any of the above conditions
    return data

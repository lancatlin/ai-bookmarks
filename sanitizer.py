import re
from functools import wraps


def sanitize(text):
    """Sanitize a string by removing HTML tags, newlines, and trimming spaces."""
    if not isinstance(text, str):
        raise TypeError("Input needs to be a string")

    # Remove HTML tags using regular expression
    text = re.sub(r"<[^>]+>", "", text)

    # Replace newline characters with spaces
    text = text.replace("\n", " ").replace("\r", "")

    # Trim unnecessary spaces
    text = " ".join(text.split())

    return text


def sanitize_output(func):
    """A decorator to sanitize the string output of a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Call the original function and get its output
        output = func(*args, **kwargs)

        # Sanitize the output using the sanitize function
        return sanitize(output)

    return wrapper


@sanitize_output
def get_content():
    return "<p>Hello,\n\n\n World! </p> <br>"


if __name__ == "__main__":
    print(sanitize("\r\n<p>Hello \r\n   World!</p>    "))
    # Call the decorated function
    print(get_content())

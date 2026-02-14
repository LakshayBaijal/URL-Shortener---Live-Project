import string
from urllib.parse import urlparse

# characters allowed in short URL
CHARACTERS = string.ascii_letters + string.digits


# function to validate URL
def is_valid_url(url):

    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return False

        if parsed.netloc == "":
            return False

        return True

    except:
        return False


# function to generate short id from number
def encode_base62(number):

    base = len(CHARACTERS)

    if number == 0:
        return CHARACTERS[0]

    result = ""

    while number > 0:

        remainder = number % base
        result = CHARACTERS[remainder] + result
        number = number // base

    return result

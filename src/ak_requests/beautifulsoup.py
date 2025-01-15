import requests
from bs4 import BeautifulSoup


def soupify(res: requests.Response) -> BeautifulSoup:
    """Converts a response object into a BeautifulSoup object."""
    return BeautifulSoup(res.text, "html.parser")

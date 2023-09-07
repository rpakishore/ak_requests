from bs4 import BeautifulSoup
import requests

def soupify(res: requests.Response) -> BeautifulSoup:
    return BeautifulSoup(res.text, 'html.parser')
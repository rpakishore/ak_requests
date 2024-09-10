from requests.auth import HTTPBasicAuth

class Auth:
    def __init__(self) -> None:
        ...
    
    def __str__(self) -> str:
        return "Authentication for requests"
    
    def basic(self, username: str|bytes, password: str|bytes):
        HTTPBasicAuth(username=username, password=password)
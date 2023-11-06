import requests
from requests import Session
from requests.adapters import HTTPAdapter, Retry
import time
import random
from ak_requests.logger import Log
from typing import Literal
from bs4 import BeautifulSoup
from pathlib import Path
import re
import urllib.parse
from yt_dlp import YoutubeDL
import pickle

DEFAULT_TIMEOUT_s = 5 #seconds

class TimeoutHTTPAdapter(HTTPAdapter):
    #Courtesy of https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT_s
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)
    
class RequestsSession:
    MIN_REQUEST_GAP: float = 0.9 #seconds
    last_request_time: float = time.time()
    RAISE_ERRORS: bool = True
    
    def __init__(self, log: bool = False, retries: int = 5, 
                    log_level: Literal['debug', 'info', 'error'] = 'info') -> None:
        self.retries = retries
        self.log: Log | None = Log() if log else None
        self.set_loglevel(log_level)
        
        self.session: Session = requests.Session()
        self._set_default_headers()
        self._set_default_retry_adapter(retries)
        self.rate_limit_remaining = None
        self.rate_limit_reset = None
        
        self._info(f'Session initialized ({retries=}, {self.MIN_REQUEST_GAP=}, )')
        return None
    
    def check_rate_limit(self) -> None:
        if self.rate_limit_remaining is not None and self.rate_limit_reset is not None:
            remaining_time = self.rate_limit_reset - time.time()
            if remaining_time > 0:
                time.sleep(remaining_time)
                
    def update_rate_limit(self, response: requests.Response) -> None:
        if 'X-RateLimit-Remaining' in response.headers and 'X-RateLimit-Reset' in response.headers:
            self.rate_limit_remaining = int(response.headers['X-RateLimit-Remaining'])
            self.rate_limit_reset = int(response.headers['X-RateLimit-Reset'])

    def set_loglevel(self, level: Literal['debug', 'info', 'error'] = "info") -> None:
        if self.log is not None:
            match level.lower().strip():
                case 'debug':
                    self.log.setLevel(10)
                case 'info':
                    self.log.setLevel(20)
                case 'error':
                    self.log.setLevel(40)
        return None

    def _debug(self, message: str) -> None:
        if self.log:
            self.log.debug(message)
            
    def _error(self, message: str) -> None:
        if self.log:
            self.log.error(message)
    
    def _info(self, message: str) -> None:
        if self.log:
            self.log.info(message)
        
    def __repr__(self) -> str:
        return f"RequestsSession(log={self.log is not None})"
    
    def __str__(self) -> str:
        return f"RequestsSession Class. Logging set to {self.log is not None}"

    def _set_default_retry_adapter(self, max_retries: int) -> requests.Session:
        retries = Retry(total=max_retries,
                        backoff_factor=0.5,
                        status_forcelist=[429, 500, 502, 503, 504]
                        )
        self.session.mount('http://', TimeoutHTTPAdapter(max_retries=retries))
        self.session.mount('https://', TimeoutHTTPAdapter(max_retries=retries))
        
        self._debug('Default retry adapters loaded')
        return self.session
    
    def get(self, *args, **kwargs) -> requests.Response:
        try:
            min_req_gap: float = self.MIN_REQUEST_GAP
            elapsed_time: float = time.time() - self.last_request_time
            if elapsed_time < min_req_gap:
                time.sleep(min_req_gap - elapsed_time)
            self.last_request_time = time.time()
            self.check_rate_limit()
            response: requests.Response = self.session.get(*args, **kwargs)
            self._info(
                    f"GET request to {args}, Status: {response.status_code}, Response: {response.text[:100]}"
                )
            self.update_rate_limit(response)
            return response
        
        except requests.RequestException as e:
            self._handle_request_exception(e)
            return None # type: ignore
    
    def _handle_request_exception(self, exception: Exception):
        self._error(f"Request Exception: {exception}")
        # Raise or handle the exception as per your requirement
        if self.RAISE_ERRORS:
            raise exception
    
    def bulk_get(self, urls: list[str], *args, **kwargs) -> list[requests.Response]:
        duplicate_list: list[str] = urls[:]
        random.shuffle(duplicate_list)  #shuffle to prevent scrape detection
        
        req:dict = {}
        for url in duplicate_list:
            try:
                req[url] = self.get(url, *args, **kwargs)
            except Exception as e:
                if not self.RAISE_ERRORS:
                    req[url] = None
                else:
                    raise e
                
        return [req[url] for url in urls]
    
    def _set_default_headers(self) -> None:
        _header = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) '
                            'Gecko/20100101 Firefox/117.0'),
            'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,'
                        'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'),
            'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
            "Accept-Encoding": "gzip, deflate, br", 
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            }
        self.update_header(header=_header)
    
    def update_header(self, header: dict) -> requests.Session:
        self.session.headers.update(header)
        self._debug('session header updated')
        return self.session
    
    def update_cookies(self, cookies: list[dict]) -> requests.Session:
        self.session.cookies.update({c['name']: c['value'] for c in cookies})
        self._debug('session cookies updated')
        return self.session
    
    def soup(self, url: str, *args, **kwargs) -> tuple[BeautifulSoup, requests.Response]:
        res: requests.Response = self.get(url, *args, **kwargs)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup, res

    def bulk_soup(self, urls: list[str], *args, 
                  **kwargs) -> tuple[list[BeautifulSoup], list[requests.Response]]:
        ress: list[requests.Response] = self.bulk_get(urls, *args, **kwargs)
        soups = [BeautifulSoup(res.text, 'html.parser') for res in ress]
        return soups, ress
    
    def download(self, url: str, fifopath: str|Path, confirm_downloadble: bool = False,**kwargs) -> Path|None:
        """Downloads file from url

        Args:
            url (str): Url to download
            fifopath (str | Path): Filepath/Filename/FolderPath
            confirm_downloadble (bool, optional): Download only if `content-type` is downloadble. Defaults to False.

        Returns:
            Path|None: Downloaded filepath. `None` if not-downloadable.
        """
        
        # Confirm downloadble
        if confirm_downloadble:
            if not self.downloadble(url):
                return None

        # Get filename
        _fifopath: Path = Path(str(fifopath))
        if _fifopath.is_dir():
            filepath: Path = _fifopath / self._filename_from_url(url)
        else:
            filepath: Path = _fifopath
        
        # Download
        with self.get(url, stream=True,**kwargs) as r:
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        return filepath
    
    def downloadble(self, url: str) -> bool:
        """Ensures the `content-type` of specified url is downloadable

        Args:
            url (str): Download URL

        Returns:
            bool: If the url content is downloadble
        """
        headers = self.session.head(url, allow_redirects=True).headers
        content_type: str|None = headers.get('content-type')
        if content_type is None:
            return True
        elif content_type.lower() in {'text', 'html'}:
            return False
        return True
    
    def _filename_from_url(self, url: str) -> str:
        headers = self.session.head(url, allow_redirects=True).headers
        cd: str|None = headers.get('content-disposition')
        if cd:
            fname = re.findall('filename=(.+)', cd)
            if len(fname) != 0:
                return fname[0]
        
        name: str = url.rsplit('/', 1)[1]
        
        return urllib.parse.unquote_plus(name)
    
    def video(self, url: str, folderpath: Path = Path('.'), audio_only: bool=False) -> dict:
        #Get video info
        with YoutubeDL({}) as ydl:
            info = ydl.extract_info(url, download=False)

            video_info= ydl.sanitize_info(info)
        
        if audio_only:
            ydl_opts = {
                'format': 'm4a/bestaudio/best',
                'postprocessors': [{  # Extract audio using ffmpeg
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                }]
            }
        else:
            filename = folderpath.absolute() / '%(title)s.%(ext)s'
            ydl_opts = {
                'outtmpl':str(filename),
            }
            
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return video_info # type: ignore
    
    def save_session(self, file_path: str):
        """Serialize and save the session object to a file."""
        with open(file_path, 'wb') as file:
            pickle.dump(self.session, file)
        self._info(f'Session state saved to {file_path}')

    @classmethod
    def load_session(cls, file_path: str, log: bool = False, retries: int = 5,
                    log_level: Literal['debug', 'info', 'error'] = 'info') -> 'RequestsSession':
        """Load a serialized session object from a file."""
        instance = cls(log=log, retries=retries, log_level=log_level)
        with open(file_path, 'rb') as file:
            instance.session = pickle.load(file)
        instance._info(f'Session state loaded from {file_path}')
        return instance
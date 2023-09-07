import requests
from requests import Session
from requests.adapters import HTTPAdapter, Retry
import time
import random
from ak_requests.logger import Log
from typing import Literal

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
    
    def __init__(self, log: bool = False, retries: int = 5, 
                    log_level: Literal['debug', 'info', 'error'] = 'info') -> None:
        self.retries = retries
        self.log: Log | None = Log() if log else None
        self.set_loglevel(log_level)
        
        self.session: Session = requests.Session()
        self._set_default_headers()
        self._set_default_retry_adapter(retries)
        
        self._info(f'Session initialized ({retries=}, {self.MIN_REQUEST_GAP=}, )')
        return None
    
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
        min_req_gap: float = self.MIN_REQUEST_GAP
        elapsed_time: float = time.time() - self.last_request_time
        if elapsed_time < min_req_gap:
            time.sleep(min_req_gap - elapsed_time)
        self.last_request_time = time.time()
        return self.session.get(*args, **kwargs)
    
    def bulk_get(self, urls: list[str], *args, **kwargs) -> list[requests.Response]:
        duplicate_list: list[str] = urls[:]
        random.shuffle(duplicate_list)  #shuffle to prevent scrape detection
        
        req:dict = {}
        for url in duplicate_list:
            req[url] = self.get(url, *args, **kwargs)
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

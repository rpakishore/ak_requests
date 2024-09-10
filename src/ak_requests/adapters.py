from requests.adapters import HTTPAdapter, Retry

class TimeoutHTTPAdapter(HTTPAdapter):
    DEFAULT_TIMEOUT_s = 5 #seconds
    #Courtesy of https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
    def __init__(self, max_retries: int=5, *args, **kwargs):
        retry_adapter = Retry(total=max_retries,
                        backoff_factor=0.5,
                        status_forcelist=[429, 500, 502, 503, 504]
                        )
        self.timeout = self.DEFAULT_TIMEOUT_s
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(max_retries=retry_adapter, *args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)
from ak_requests.request import RequestsSession
from requests.exceptions import RequestException, RetryError
from unittest.mock import Mock
import pytest

class TestRequestsSession:
    @pytest.fixture(scope="module")
    def requests_session(self):
        session = RequestsSession(log=False, retries=2)
        session.MIN_REQUEST_GAP = 0.1   #Limit gap for test purposes
        return session
    
    def test_get_http(self, requests_session):
        res = requests_session.get('https://httpbin.org/get')
        data: dict = res.json()
        assert data.get('url') == 'https://httpbin.org/get'
        assert res.status_code == 200
        assert res.headers.get('Content-Type') == 'application/json'
        assert res.is_redirect is False
        

    def test_status_codes(self, requests_session):
        def _check_status(code):
            assert requests_session.get(f'https://httpbin.org/status/{code}').status_code == code
        _check_status(200)
        _check_status(300)
        _check_status(400)
    
    def test_check_retry(self, requests_session):
        with pytest.raises(RetryError) as _:
            requests_session.get(f'https://httpbin.org/status/500')

    def test_cookies(self,requests_session):
        send_cookie: dict = {'id':'test_ak_requests'}
        requests_session.get('https://httpbin.org/cookies/set', params=send_cookie)
        cookies: dict = requests_session.get("http://httpbin.org/cookies").json()
        assert cookies == {'cookies': send_cookie}
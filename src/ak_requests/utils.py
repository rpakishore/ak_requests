import requests


def latest_useragent(browser: str = "chrome") -> str:
    """Returns the latest useragent for the specified browser based on daily list [published here](https://jnrbsn.github.io/user-agents/user-agents.json)"""
    try:
        useragents: list[str] = requests.get(
            "https://jnrbsn.github.io/user-agents/user-agents.json"
        ).json()
        for useragent in useragents:
            if browser.casefold() in useragent.casefold():
                return useragent
    except Exception as e:
        print(str(e))
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0"

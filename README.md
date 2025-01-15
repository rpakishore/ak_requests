<!--- Heading --->
<div align="center">
  <h1>ak_requests</h1>
  <p>
    Requests package with QOL improvements and anti-bot detection measures
  </p>
<h4>
    <a href="https://rpakishore.github.io/ak_requests/">Documentation</a>
  </h4>
</div>
<br />

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/rpakishore/ak_requests)
![GitHub last commit](https://img.shields.io/github/last-commit/rpakishore/ak_requests)
[![tests](https://github.com/rpakishore/ak_requests/actions/workflows/test.yml/badge.svg)](https://github.com/rpakishore/ak_requests/actions/workflows/test.yml)
<!-- [![tests](https://github.com/rpakishore/ak_requests/actions/workflows/test.yml/badge.svg)](https://github.com/rpakishore/ak_requests/actions/workflows/test.yml) -->

<!-- Table of Contents -->
<h2>Table of Contents</h2>

- [1. About the Project](#1-about-the-project)
  - [1.1. Features](#11-features)
- [2. Getting Started](#2-getting-started)
  - [2.1. Installation](#21-installation)
- [3. Usage](#3-usage)
  - [3.1. Create and use session](#31-create-and-use-session)
  - [3.2. Beautifulsoup](#32-beautifulsoup)
  - [3.3. Download files](#33-download-files)
  - [3.4. Other Functionality](#34-other-functionality)
- [4. Roadmap](#4-roadmap)
- [5. License](#5-license)
- [6. Contact](#6-contact)

<!-- About the Project -->
## 1. About the Project

`ak_requests` is a Python package that provides an interface for automating requests tasks using `requests` package. It comes with quality of life improvements like retires, custom redirects, spacing out requests and shuffling requests to not trigger anti-bot measures.

<!-- Features -->
### 1.1. Features

- Bulk requests handling
- Retry strategies including exponential back-off
- Built-in retries and timeouts
- Can log processes to file
- Handles downloads of files/videos
- Implemented default rate-limiting checks and process
- Session objects are serialized to be able to save/load sessions from file
- Can choose to handle exceptions or skip it completely with `RAISE_EXCEPTIONS` attribute
- Can support both basic `.basic_auth()` and OAuth `.oauth2_auth()` authentications.
- Improve rate-limiting with built-in APIs for dynamically adjusting request frequencies based on feedback (e.g., from Retry-After headers) and automatically spacing requests accordingly.

<!-- Getting Started -->
## 2. Getting Started


<!-- Installation -->
### 2.1. Installation

```bash
pip install ak_requests@git+https://github.com/rpakishore/ak_requests
```

<!-- Usage -->
## 3. Usage

### 3.1. Create and use session

```python
from ak_requests import RequestsSession

# Initialize session
session = RequestsSession(log=False, retries=5, log_level='error', timeout=10) 

## Can update session level variables
session.MIN_REQUEST_GAP = 1.5   # seconds, Change min time bet. requests
session.RAISE_ERRORS = False    # raises RequestErrors, else returns None; defaults to True

# Update custom header
session.update_header({'Connection': 'keep-alive'})

# set cookies
session.update_cookies([{'name':'has_recent_activity', 'value':'1'}])

# Get requests
res = session.get('https://reqres.in/api/users?page=2', data={}, proxies = {} ) # Can accept any requests parameters

# Make bulk requests
urls = ['https://reqres.in/api/users?page=2', 'https://reqres.in/api/unknown']
responses = session.bulk_get(urls)

```


### 3.2. Beautifulsoup

```python
from ak_requests import soupify
res = session.get('https://reqres.in/api/users?page=2')
soup = soupify(res)

## or 
soup, res = session.soup('https://reqres.in/api/users?page=2')

## Also works for bulk requests
soups, ress = session.bulk_soup(urls)

```

### 3.3. Download files

```python
# Check if file is downloadble
session.downloadble('https://www.youtube.com/watch?v=9bZkp7q19f0')  #False

session.downloadble('http://google.com/favicon.ico') #True

session.download(
  url = 'http://google.com/favicon.ico',  #URL to download
  fifopath='C:\\', #Can be folderpath, filename or filepath. If existing folder specified - will extract filename from url contents
  confirm_downloadble = False #Will return `None`, if url not downloadble
)

# Download videos
from pathlib import Path
video_info = session.video(url='https://www.youtube.com/watch?v=BaW_jenozKc', 
              folderpath=Path('.'),
              audio_only=False) #Downloads the video to specified path and returns dict of video info

```

### 3.4. Other Functionality

```python
# Save/Restore session to/from file
## Save the session state to a file
session.save_session('session_state.pkl')

## Later, you can load the session state back
restored_session = RequestsSession.load_session('session_state.pkl')

# Authentication
session.setup_auth_basic(username="johndoe", password="12345678") ## basic auth
session.setup_auth_oauth2(token='x0-xxxxxxxxxxxxxxxxxxxxxxxx')    ## OAuth authentication
```

<!-- Roadmap -->
## 4. Roadmap

- **Proxy Support**: Allow support for rotating proxy lists to manage a large volume of requests without hitting rate limits or triggering anti-bot measures. Integrate features like automatic proxy testing and failover in case of a broken proxy.
- **Asynchronous Requests**: Implement asynchronous request handling using asyncio or aiohttp. This can significantly enhance performance when dealing with multiple concurrent requests, especially for I/O-bound tasks.
- **Response Caching**: Add a caching layer for GET requests to avoid redundant network requests and speed up frequently accessed data retrieval. Allow users to configure the caching mechanism, cache duration, and invalidation strategies.
- **Request Preprocessing and Postprocessing**: Introduce hooks for preprocessing and postprocessing of requests and responses. Users could modify request headers, log specific details, or automatically retry certain status codes like 429.
- **File Upload Support**: Enable multipart/form-data requests for uploading files, which could expand the functionality to handle file transfers in both directions.
- **Support for Additional Auth Schemes**: Beyond basic and OAuth2, consider adding support for other authentication methods, like token-based, bearer tokens, and cookie-based authentication, to broaden compatibility with different APIs.
- **Session Management Enhancements**: Improve session handling by introducing automatic session refresh or re-authentication mechanisms, especially for OAuth tokens with limited lifespans.
- **Download Manager with Resumable Downloads**: Enhance the file download feature to support resumable downloads for large files. This can improve robustness when downloading large datasets or videos over unreliable networks.
- **Customizable User-Agent Spoofing**: Provide built-in options for easily rotating or randomizing User-Agent strings to bypass common anti-bot mechanisms. A customizable header interface might also enhance flexibility.
- **Extended Logging and Monitoring**: Introduce more detailed and configurable logging options, such as logging retries, rate limits hit, request/response times, and any exceptions caught. This could help track the performance and reliability of the request handling process.
- **Improved Error Handling**: Implement more sophisticated error classification to differentiate between recoverable and non-recoverable errors. Offer users the ability to handle or ignore specific HTTP status codes and exceptions.
- **Interactive Progress Bars**: For file downloads or bulk requests, adding progress indicators or real-time updates for long-running tasks could improve the user experience.
- **Built-in CLI Tool**: Create a command-line interface for ak_requests, enabling users to perform basic request tasks like GET, POST, or bulk downloads from the terminal without writing Python code.

<!-- License -->
## 5. License

See LICENSE for more information.

<!-- Contact -->
## 6. Contact

Arun Kishore - [@rpakishore](mailto:pypi@rpakishore.co.in)

Project Link: [https://github.com/rpakishore/ak_requests](https://github.com/rpakishore/ak_requests)
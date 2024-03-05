<!--- Heading --->
<div align="center">
  <h1>ak_requests</h1>
  <p>
    Requests package with QOL improvements and anti-bot detection measures
  </p>
<h4>
    <a href="https://github.com/rpakishore/ak_requests/">View Demo</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/ak_requests">Documentation</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/ak_requests/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/ak_requests/issues/">Request Feature</a>
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
    - [2.1.1. Production](#211-production)
    - [2.1.2. Development](#212-development)
- [3. Usage](#3-usage)
- [4. Roadmap](#4-roadmap)
- [5. License](#5-license)
- [6. Contact](#6-contact)
- [7. Acknowledgements](#7-acknowledgements)

<!-- About the Project -->
## 1. About the Project

`ak_requests` is a Python package that provides an interface for automating requests tasks using `requests` package. It comes with quality of life improvements like retires, custom redirects, spacing out requests and shuffling requests to not trigger anti-bot measures 

<!-- Features -->
### 1.1. Features

- Bulk requests handling
- Built-in retries and timeouts
- Can log processes to file
- Handles downloads of files/videos
- Implemented default rate-limiting checks and process
- Session objects are serialized to be able to save/load sessions from file
- Can choose to handle exceptions or skip it completely with `RAISE_EXCEPTIONS` attribute
- Can support both basic `.basic_auth()` and OAuth `.oauth2_auth()` authentications.

<!-- Getting Started -->
## 2. Getting Started


<!-- Installation -->
### 2.1. Installation

#### 2.1.1. Production

Download the repo and install with flit

```bash
pip install flit
flit install --deps production
```

Alternatively, you can use pip

```bash
pip install ak_requests
```

#### 2.1.2. Development

Install with flit

```bash
  flit install --pth-file
```

<!-- Usage -->
## 3. Usage

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

# use beautifulsoup
from ak_requests import soupify
res = session.get('https://reqres.in/api/users?page=2')
soup = soupify(res)

## or 
soup, res = session.soup('https://reqres.in/api/users?page=2')

## Also works for bulk requests
soups, ress = session.bulk_soup(urls)

# Download files
## Check if file is downloadble
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

# Save/Restore session to/from file
## Save the session state to a file
session.save_session('session_state.pkl')

## Later, you can load the session state back
restored_session = RequestsSession.load_session('session_state.pkl')

# Authentication
session.basic_auth(username="johndoe", password="12345678") ## basic auth
session.oauth2_auth(token='x0-xxxxxxxxxxxxxxxxxxxxxxxx')    ## OAuth authentication
```

<!-- Roadmap -->
## 4. Roadmap

- [ ] Proxy
- [ ] Asynchronous Requests
- [ ] Response Caching
- [ ] Request Preprocessing and Postprocessing
- [ ] File Upload Support

<!-- License -->
## 5. License

See LICENSE for more information.

<!-- Contact -->
## 6. Contact

Arun Kishore - [@rpakishore](mailto:pypi@rpakishore.co.in)

Project Link: [https://github.com/rpakishore/ak_requests](https://github.com/rpakishore/ak_requests)

<!-- Acknowledgments -->
## 7. Acknowledgements

- [Awesome README Template](https://github.com/Louis3797/awesome-readme-template/blob/main/README-WITHOUT-EMOJI.md)
- [Shields.io](https://shields.io/)
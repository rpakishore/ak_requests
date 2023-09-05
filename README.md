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
<!-- Table of Contents -->
<h2>Table of Contents</h2>

- [1. About the Project](#1-about-the-project)
  - [1.1. Features](#11-features)
- [2. Getting Started](#2-getting-started)
  - [2.1. Installation](#21-installation)
    - [2.1.1. Production](#211-production)
    - [2.1.2. Development](#212-development)
- [3. Usage](#3-usage)
  - [3.1. Development](#31-development)
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

<!-- Getting Started -->
## 2. Getting Started


<!-- Installation -->
### 2.1. Installation

#### 2.1.1. Production

Install with flit

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
session = RequestsSession(log=False, retries=5, log_level='error') 

# Update custom header
session.update_header({'Connection': 'keep-alive'})

# set cookies
session.update_cookies([{'name':'has_recent_activity', 'value':'1'}])

# Get requests
session.get('https://reqres.in/api/users?page=2', data={}, proxies = {} ) # Can accept any requests parameters

# Change min time bet. requests
session.MIN_REQUEST_GAP = 1.5 # seconds

# Make bulk requests
urls = ['https://reqres.in/api/users?page=2', 'https://reqres.in/api/unknown']
responses = session.bulk_get(urls)

```

### 3.1. Development

1. Open the project directory in vscode
2. Update the app name under `pyproject.toml`
3. Change the folder name from `src\template_python` to `src\<app_name>`, and propate the changes to the subfolders.
4. Review the dependencies under `pyproject.toml` and remove as needed.
5. Remove unneeded dependencies from `src\<app_name>\`

<!-- Roadmap -->
## 4. Roadmap

- [ ] Add beautifulsoup integration
- [ ] Proxy

<!-- License -->
## 5. License

See LICENSE for more information.

<!-- Contact -->
## 6. Contact

Arun Kishore - [@rpakishore](mailto:pypi@rpakishore.co.in)

Project Link: [https://github.com/rpakishore/ak_requests](https://github.com/rpakishore/ak_requests)

<!-- Acknowledgments -->
## 7. Acknowledgements

Use this section to mention useful resources and libraries that you have used in your projects.

- [Awesome README Template](https://github.com/Louis3797/awesome-readme-template/blob/main/README-WITHOUT-EMOJI.md)
- [Shields.io](https://shields.io/)
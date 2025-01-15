"""
```mermaid
graph TD
    subgraph "Client Application Layer"
        Client["Client Application"]
        RequestsSession["RequestsSession Interface"]:::core
    end

    subgraph "Core Features Layer"
        CoreFeatures["Core Request Handler"]:::core
        BulkRequests["Bulk Requests"]:::core
        SessionMgmt["Session Management"]:::core
    end

    subgraph "Extension Features Layer"
        BSParser["BeautifulSoup Parser"]:::extension
        FileDownload["File Downloads"]:::extension
        VideoDownload["Video Downloads"]:::extension
    end

    subgraph "Safety Layer"
        RateLimit["Rate Limiting"]:::safety
        RetryMech["Retry Mechanism"]:::safety
        AntiBotSystem["Anti-Bot Detection"]:::safety
        Logger["Logging System"]:::safety
    end

    subgraph "External Services Layer"
        HTTPEndpoints["HTTP/HTTPS Endpoints"]:::external
        AuthServices["Authentication Services"]:::external
        FileServers["File Servers"]:::external
    end

    %% Connections
    Client --> RequestsSession
    RequestsSession --> CoreFeatures
    RequestsSession --> BulkRequests
    RequestsSession --> SessionMgmt

    CoreFeatures --> BSParser
    CoreFeatures --> FileDownload
    CoreFeatures --> VideoDownload

    BSParser & FileDownload & VideoDownload --> RateLimit
    RateLimit --> RetryMech
    RetryMech --> AntiBotSystem
    
    AntiBotSystem --> HTTPEndpoints
    AntiBotSystem --> AuthServices
    AntiBotSystem --> FileServers

    Logger -.- CoreFeatures
    Logger -.- BSParser
    Logger -.- RateLimit
    Logger -.- RetryMech
    Logger -.- AntiBotSystem

    %% Click Events
    click CoreFeatures "https://github.com/rpakishore/ak_requests/blob/main/src/ak_requests/request.py"
    click BSParser "https://github.com/rpakishore/ak_requests/blob/main/src/ak_requests/beautifulsoup.py"
    click Logger "https://github.com/rpakishore/ak_requests/blob/main/src/ak_requests/logger.py"
    click RequestsSession "https://github.com/rpakishore/ak_requests/blob/main/src/ak_requests/__init__.py"

    %% Styling
    classDef core fill:#2374ab,stroke:#000,stroke-width:1px,color:white
    classDef extension fill:#ff7f50,stroke:#000,stroke-width:1px,color:white
    classDef safety fill:#2ecc71,stroke:#000,stroke-width:1px,color:white
    classDef external fill:#95a5a6,stroke:#000,stroke-width:1px,color:white

    %% Legend
    subgraph Legend
        L1["Core Components"]:::core
        L2["Extension Features"]:::extension
        L3["Safety Features"]:::safety
        L4["External Services"]:::external
    end

```

.. include:: ../../README.md
"""

from ak_requests.beautifulsoup import soupify
from ak_requests.request import RequestsSession

# Caching-Proxy

Caching Proxy is a CLI tool that starts a caching proxy server.
It forwards incoming HTTP requests to an origin server

If the same request is made again, the cached response is returned instead of forwarding the request to the origin server.

Project based on <https://roadmap.sh/projects/caching-server> challenge

## How to Run the Project

Requirements

- Python 3.8+
- pip
- virtualenv
- Redis

---

### 1. Clone the repository

```bash
git clone https://github.com/xenoqd/Caching-Proxy.git
cd Caching-Proxy
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Linux / macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run development server

```bash
caching-proxy --port 8000 --origin http://httpbin.org
```

## Features

CLI tool to start a caching proxy server

Example

```bash
caching-proxy --port 8000 --origin http://exampleserverurl
```

Ability to clear cache in Redis via CLI

Example

```bash
caching-proxy --clear-cache
```

Adds `X-Cache` header to responses:

`HIT` — response served from cache

`MISS` — response fetched from origin

Example

```bash
2026-01-12 18:04:33,027 | INFO | CACHE MISS → forwarding to origin
```

```bash
2026-01-12 18:06:11,634 | INFO | CACHE HIT → cache:GET:http://httpbin.org/get
```

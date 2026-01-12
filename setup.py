from setuptools import setup, find_packages

setup(
    name="caching-proxy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "httpx",
        "redis",
    ],
    entry_points={
        "console_scripts": [
            "caching-proxy=caching_proxy.cli:main",
        ],
    },
)

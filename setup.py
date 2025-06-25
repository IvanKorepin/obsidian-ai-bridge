from setuptools import setup, find_packages

setup(
    name="obsidian2perplexity",
    version="0.1.0",
    description="Proxy server for relaying requests from " \
    "Obsidian AI chat plugin to Perplexity with CORS support.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/IvanKorepin/obsidian2perplexity",
    author="Ivan Korepin",
    author_email="korepin404r@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "toml",
        "httpx",
        "click"
    ],
    entry_points={
        "console_scripts": [
            "obsidian2perplexity=obsidian2perplexity.cli:main"
        ]
    },
    include_package_data=True,
    python_requires=">=3.8",
)

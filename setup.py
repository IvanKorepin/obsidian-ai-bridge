from setuptools import setup, find_packages

setup(
    name="obsidian-ai-bridge",
    version="0.4.0",
    description="Universal AI proxy server supporting multiple AI services (Perplexity, Gemini) for Obsidian Copilot",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/IvanKorepin/obsidian-ai-bridge",
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
            "obsidian-ai-bridge=obsidian_ai_bridge.cli:main"
        ]
    },
    package_data={
        "obsidian_ai_bridge": ["config.default.toml"],
    },
    include_package_data=True,
    python_requires=">=3.8",
)

# Obsidian to Perplexity Proxy

**Works with the [Obsidian Copilot plugin](https://github.com/logancyang/obsidian-copilot).**

**Русская версия:** [README.rus.md](README.rus.md)

**Note:** This utility only rewrites HTTP headers to bypass CORS. It does not read, store, or analyze the request body, and does not collect or retain any data from requests.

A Python-based proxy server that relays requests from Obsidian to Perplexity, handling CORS issues. The project is containerized with Docker and supports both local development and production deployment.

## Features
- FastAPI-based proxy for Perplexity API
- Handles CORS for Obsidian integration
- Configurable via TOML file (dev/prod)
- Docker and devcontainer support

## Installation

You can install the utility directly from PyPI:
```bash
pip install obsidian2perplexity
```

After installation, the command `obsidian2perplexity` will be available in your terminal.

> **See [docs/configuration.md](docs/configuration.md) for platform-specific installation and usage instructions (Linux, Windows, macOS, Docker, devcontainer, systemd, etc).**

## Quick Start (Local)

1. **Install the package:**
   ```bash
   pip install obsidian2perplexity
   ```
2. **Prepare configuration:**
   Place your `config.default.toml` in the current directory or specify its path with the `--config-path` option.
3. **Run the server:**
   ```bash
   obsidian2perplexity --host 0.0.0.0 --port 8080
   ```
   By default, the server will look for `config.default.toml` in the current directory or package.

## Docker Usage

1. **Build the image:**
   ```bash
   docker build -t obsidian2perplexity .
   ```
2. **Run the container:**
   ```bash
   docker run -p 8080:8080 obsidian2perplexity
   ```
   You can mount your config file if needed:
   ```bash
   docker run -p 8080:8080 -v $(pwd)/config.default.toml:/app/config.default.toml obsidian2perplexity
   ```

## Devcontainer Usage

1. **Open the project in VS Code.**
2. **Reopen in Container** using the "Remote - Containers" extension.
3. **The devcontainer will automatically install dependencies and set up the environment.**
4. **To run the server inside the devcontainer:**
   ```bash
   python -m obsidian2perplexity.cli --host 0.0.0.0 --port 8080
   ```
   or use the entrypoint:
   ```bash
   obsidian2perplexity --host 0.0.0.0 --port 8080
   ```

## Configuration File

The proxy is configured via a TOML file (by default `config.default.toml`). Example:

```toml
[routing]
# The API endpoint for Perplexity's chat completions.
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
# Specifies the origins allowed for CORS requests, ensuring compatibility between Obsidian and Perplexity.
ALLOWED_ORIGINS = "app://obsidian.md"

[server]
host = "0.0.0.0"
port = 8080
# TIMEOUT = 30                  # Timeout duration for API requests in seconds.
# LOG_LEVEL = "info"            # Logging level (e.g., debug, info, warning, error).
```

- **[routing]**: routing and CORS settings.
- **[server]**: server launch parameters (host, port, etc.).
- You can create separate files for dev/prod environments.

## Configuration Documentation
- [docs/configuration.md](docs/configuration.md)

## License
MIT

## Uninstallation

To remove the utility:

- **pip (any OS):**
  ```bash
  pip uninstall obsidian2perplexity
  ```
- **Docker:**
  - Remove the image:
    ```bash
    docker rmi obsidian2perplexity
    ```
  - Remove containers (if any):
    ```bash
    docker ps -a | grep obsidian2perplexity
    docker rm <container_id>
    ```
- **Devcontainer (VS Code):**
  - Remove the devcontainer from the VS Code UI or delete the `.devcontainer` folder.

For more details, see your platform's package and container management documentation.


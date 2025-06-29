<h1 style="text-align: center;"> Obsidian to Perplexity Proxy </h1>

**Works with the [Obsidian Copilot plugin](https://github.com/logancyang/obsidian-copilot).**

**Russian version:** [README.rus.md](README.rus.md)

## What it does

The Copilot plugin for Obsidian allows you to connect to APIs of many popular AI services, such as OpenAI, Gemini, DeepSeek, and others. Naturally, provided that you have a subscription to these models and the corresponding API tokens.
Unfortunately, the plugin does not support the popular Perplexity service.
Obsidian2Perplexity solves this problem. O2P is a simple and lightweight proxy server that sits between Obsidian-Copilot and Perplexity, transforming the headers of your HTTPS requests so that they are understood by the Perplexity API and returns responses.

O2P can be deployed on your server or hosting and provide connection from any device, or on your computer where Obsidian is running.

> **Privacy Notice:** The utility only modifies request headers and does not read, collect, or store the request body content. No user data is logged or saved.

## Features
- Installation on server or local machine
- Works with or without reverse proxy
- SSL support
- Handles CORS for Obsidian integration
- Configurable via TOML file
- Docker and devcontainer support for development

## Installation

Install the utility from PyPI:
```bash
pip install obsidian2perplexity
```

After installation, the command `obsidian2perplexity` will be available in your terminal.

## Quick Start (Local)

1. Install the package:
   ```bash
   pip install obsidian2perplexity
   ```

2. Run the server:
   ```bash
   obsidian2perplexity --host 127.0.0.1 --port 8787
   ```

> See [documentation](docs/configuration.md) for more detailed installation and configuration instructions for different environments (Linux, Windows, macOS, Docker, devcontainer).

3. Install the Copilot plugin for Obsidian according to the [official documentation](https://github.com/logancyang/obsidian-copilot)

4. Go to plugin settings
![Go to settings](/docs/img/copilot_configure_step1_eg.png)

5. Go to the Model tab
![Model tab](/docs/img/copilot_configure_step2_eng.png)

6. Scroll down to the end of the pre-installed models

7. Click the "Add custom model" button
![Model tab](/docs/img/copilot_configure_step3_eng.png)

8. Fill out the form
![Model form](/docs/img/copilot_configure_step4.png)
   1) Perplexity model name ([List of available models according to Perplexity](https://www.perplexity.ai/search/what-models-does-the-perplexity-api-support-MCb_.seRSF2SbY91Wh6QjQ))
   2) Select "Open AI Format"
   3) Host parameters where Obsidian2Perplexity is deployed
      3.1) For local installation ```http://localhost:8787/```
      3.2) For server installation ```https://YOUR_IP_ADDRESS:8787```

      > **Note 1:** Host address and port can be set when launching the utility ```obsidian2perplexity --host YOUR_IP --port YOUR_PORT```

      > **Note 2:** Make sure the selected port is open for connections.
      
   4) Enter your API token from your Perplexity account

   5) Check "Enable CORS"
   6) Click "Verify" to make sure everything works. If configured correctly, a success message will appear in the corner of the screen
   ![Successful connection](/docs/img/copilot_configure_success.png)

   Congratulations! Your system is now successfully configured

## Configuration

See detailed [configuration guide](docs/configuration.md) with examples and usage scenarios.

## License
MIT

## Uninstallation

- **pip (any OS):**
  ```bash
  pip uninstall obsidian2perplexity
  ```


For more details, see your platform's package and container management documentation.


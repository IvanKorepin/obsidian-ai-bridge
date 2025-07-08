<h1 style="text-align: center;"> Obsidian AI Bridge </h1>

**Universal AI proxy server for Obsidian Copilot plugin**

**Russian version:** [README.rus.md](README.rus.md)

## What it does

The Copilot plugin for Obsidian allows you to connect to APIs of many popular AI services, such as OpenAI, DeepSeek, and others. However, some popular services like Perplexity and Google Gemini are not directly supported due to API differences and CORS restrictions.

**Obsidian AI Bridge** solves this problem by providing a universal proxy server that:
- **Bridges API format differences** between Obsidian and AI services
- **Handles CORS restrictions** that prevent direct browser connections
- **Supports multiple AI services**: Perplexity for chat completions and Google Gemini for embeddings
- **Transforms requests and responses** to match expected formats

The proxy can be deployed on your server or locally on your computer where Obsidian is running.

> **Privacy Notice:** The utility only transforms request/response formats and handles routing. No user data is logged, stored, or modified beyond format conversion.

## Supported Services

- **Perplexity API**: Chat completions and reasoning models
- **Google Gemini**: Text embedding models (geographic restrictions may apply)

## Features
- **Universal endpoint handling**: `/perplexity/*` routes to Perplexity, `/gemini/embeddings` to Gemini
- **pip package installation**: Easy installation and updates
- **CLI interface**: Simple command-line configuration
- **Flexible deployment**: Local, server, or containerized
- **SSL support**: HTTPS with custom certificates
- **CORS handling**: Full cross-origin request support
- **Configurable**: TOML configuration files
- **Logging**: Detailed request/response logging for debugging

## Installation

Install the utility from PyPI:
```bash
pip install obsidian-ai-bridge
```

After installation, the command `obsidian-ai-bridge` will be available in your terminal.

## Quick Start (Local)

1. **Install the package:**
   ```bash
   pip install obsidian-ai-bridge
   ```

2. **Run the server:**
   ```bash
   # Basic usage (defaults to localhost:8000)
   obsidian-ai-bridge
   
   # Custom host and port
   obsidian-ai-bridge --host 127.0.0.1 --port 8787
   
   # With SSL certificates
   obsidian-ai-bridge --host 0.0.0.0 --port 443 --ssl-cert cert.pem --ssl-key key.pem
   ```

3. **Available endpoints:**
   - `POST /perplexity/*` - Proxies to Perplexity API (all paths supported)
   - `POST /gemini/embeddings` - Proxies to Google Gemini Embedding API
   - `GET /health` - Health check endpoint

> See [documentation](docs/configuration.md) for more detailed installation and configuration instructions for different environments (Linux, Windows, macOS, Docker, devcontainer).

## Configuration with Obsidian Copilot

### For Perplexity (Chat Models)

1. Install the Copilot plugin for Obsidian according to the [official documentation](https://github.com/logancyang/obsidian-copilot)

2. Go to plugin settings
![Go to settings](/docs/img/copilot_configure_step1_eng.png)

3. Go to the Model tab
![Model tab](/docs/img/copilot_configure_step2_eng.png)

4. Scroll down to the end of the pre-installed models

5. Click the "Add custom model" button
![Model tab](/docs/img/copilot_configure_step3_eng.png)

6. **Configure Perplexity model:**
![Model form](/docs/img/copilot_configure_step4.png)
   1) **Model name**: Choose from [available Perplexity models](https://docs.perplexity.ai/docs/model-cards) (e.g., `llama-3.1-sonar-small-128k-online`, `llama-3.1-sonar-large-128k-online`)
   2) **Format**: Select "Open AI Format"
   3) **Host URL**: 
      - Local: `http://localhost:8787/perplexity`
      - Server: `https://YOUR_DOMAIN/ai/perplexity`
   4) **API Token**: Your Perplexity API key from [perplexity.ai](https://www.perplexity.ai/settings/api)
   5) **Enable CORS**: ✅ Check this option
   6) **Click "Verify"** to test the connection

### For Google Gemini (Embedding Models)

7. **Add Gemini Embedding model:**
   1) **Model name**: `text-embedding-004` or other [Gemini embedding models](https://ai.google.dev/gemini-api/docs/embeddings)
   2) **Format**: Select "Open AI Format"  
   3) **Host URL**:
      - Local: `http://localhost:8787/gemini`
      - Server: `https://YOUR_DOMAIN/ai/gemini`
   4) **API Token**: Your Google AI API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   5) **Enable CORS**: ✅ Check this option
   6) **Click "Verify"** to test the connection

> **Note:** Google Gemini API may be restricted in some regions (e.g., Russia). Use VPN if needed.

8. **Success confirmation:**
   ![Successful connection](/docs/img/copilot_configure_success.png)

   Congratulations! Your system is now successfully configured for both chat and embedding models.

## Command Line Options

```bash
obsidian-ai-bridge [OPTIONS] [CONFIG_PATH]

Options:
  --host TEXT      Host to bind (default: localhost)
  --port INTEGER   Port to run on (default: 8000)
  --ssl-cert TEXT  Path to SSL certificate file
  --ssl-key TEXT   Path to SSL key file
  --help           Show help message

Examples:
  obsidian-ai-bridge                                    # Run on localhost:8000
  obsidian-ai-bridge --host 0.0.0.0 --port 8787       # Custom host/port
  obsidian-ai-bridge config.toml --host 0.0.0.0       # Use config file
```

## Configuration

See detailed [configuration guide](docs/configuration.md) with examples and usage scenarios.

## License
MIT

## Uninstallation

- **pip (any OS):**
  ```bash
  pip uninstall obsidian-ai-bridge
  ```


For more details, see your platform's package and container management documentation.


# Configuration Guide for obsidian2perplexity

This document describes several ways to configure the obsidian2perplexity proxy for use with the Obsidian AI plugin.

## Configuration File: `config.default.toml`

The proxy is configured via a TOML file, typically named `config.default.toml` or `config.dev.toml`.

- **How to create:**
  1. Create a file named `config.default.toml` (or `config.dev.toml`) in your working directory.
  2. Use the following template as a starting point:
     ```toml
     [routing]
     PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
     ALLOWED_ORIGINS = "app://obsidian.md"

     [server]
     HOST = "0.0.0.0"
     PORT = 8080
     # SSL_CERTFILE = "/path/to/fullchain.pem"
     # SSL_KEYFILE = "/path/to/privkey.pem"
     ```
- **Where to place:**
  - Place the config file in the same directory where you run the `obsidian2perplexity` command, or specify its path with the `--config-path` argument.
  - Example:
    ```bash
    obsidian2perplexity config.default.toml
    ```
  - If not specified, the utility will search for `config.default.toml` in the current directory and in the package directory.

## 1. running on a Remote Server Without SSL (Using Reverse Proxy, e.g., Nginx)

- **Recommended for production.**
- The proxy runs with HTTP only, and SSL termination is handled by a reverse proxy (such as Nginx).
- Example Nginx configuration:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate     /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8080;  # or your proxy port
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
- Start the proxy without SSL:
  ```bash
  obsidian2perplexity --host 127.0.0.1 --port 8080
  ```

## 2. Running on a Remote Server With SSL (Without Reverse Proxy)

- The proxy itself handles HTTPS connections.
- You must provide paths to your SSL certificate and private key (PEM format) and ensure the user running the utility has read access to these files.
- **Warning:** Running the proxy with direct access to SSL certificates is less secure than using a reverse proxy. Use only if you understand the risks.
- Example:
  ```bash
  obsidian2perplexity --host 0.0.0.0 --port 8080 --ssl-cert /path/to/fullchain.pem --ssl-key /path/to/privkey.pem
  ```
- Make sure the certificate and key files are readable by the user running the proxy.

## 3. Local Installation (Same Machine as Obsidian)

- For local use, you can run the proxy without SSL:
  ```bash
  obsidian2perplexity --host 127.0.0.1 --port 8080
  ```
- In the Obsidian AI plugin, set the proxy endpoint to `http://127.0.0.1:8080`.

---

# Installation and Autostart Instructions

## Linux
1. **Install:**
   ```bash
   pip install obsidian2perplexity
   ```
2. **Autostart (systemd):**
   Create a file `/etc/systemd/system/obsidian2perplexity.service`:
   ```ini
   [Unit]
   Description=Obsidian2Perplexity Proxy
   After=network.target

   [Service]
   ExecStart=/usr/local/bin/obsidian2perplexity --host 127.0.0.1 --port 8080
   Restart=always
   User=youruser

   [Install]
   WantedBy=multi-user.target
   ```
   Then run:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable obsidian2perplexity
   sudo systemctl start obsidian2perplexity
   ```

## Windows
1. **Install:**
   ```powershell
   pip install obsidian2perplexity
   ```
2. **Autostart:**
   - Create a shortcut to run `obsidian2perplexity` and place it in the Startup folder, or use Task Scheduler to run the command at login.

## macOS
1. **Install:**
   ```bash
   pip install obsidian2perplexity
   ```
2. **Autostart (launchd):**
   - Create a `plist` file in `~/Library/LaunchAgents/` to run the proxy at login. Example:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.obsidian2perplexity.proxy</string>
       <key>ProgramArguments</key>
       <array>
           <string>/usr/local/bin/obsidian2perplexity</string>
           <string>--host</string>
           <string>127.0.0.1</string>
           <string>--port</string>
           <string>8080</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
   </dict>
   </plist>
   ```
   Then load it with:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.obsidian2perplexity.proxy.plist
   ```

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

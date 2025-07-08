# Configuration Guide for obsidian-ai-bridge

obsidian-ai-bridge has two ways of configuration:

1. **Via command line parameters**: you can specify host, port, ssl-cert and ssl-key directly when launching the utility:
   ```bash
   obsidian-ai-bridge --host 0.0.0.0 --port 8080 --ssl-cert /path/to/fullchain.pem --ssl-key /path/to/privkey.pem
   ```
   If you don't specify these parameters, values from the configuration file or default values will be used.

2. **Via configuration file**: create a `config.toml` file (or `config.dev.toml`) in the working directory. The file path can be specified as a positional argument after the package name:
   ```bash
   obsidian-ai-bridge config.default.toml
   ```
   If the path is not specified, the utility will search for `config.toml` in the current directory and in the package directory.

   Example template:
   ```toml
   [routing]
   PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions" # Perplexity API URL (usually no need to change)
   ALLOWED_ORIGINS = "app://obsidian.md" # Allowed origins for CORS (usually no need to change)

   [server]
   HOST = "0.0.0.0"
   PORT = 8080
   # SSL_CERTFILE = "/path/to/fullchain.pem"
   # SSL_KEYFILE = "/path/to/privkey.pem"
   ```
   - **PERPLEXITY_API_URL** — Perplexity API address to which requests will be proxied. Usually no need to change.
   - **ALLOWED_ORIGINS** — list of allowed origins for CORS (e.g., for working with Obsidian). Usually no need to change.

## 1. Running on a Remote Server Without SSL (via reverse proxy, e.g., Nginx)

**Recommended for production.**

This method is the most secure because, on one hand, it uses SSL encryption, and on the other hand, it doesn't require giving the obsidian-ai-bridge application access to your SSL certificate and private key.

The proxy works only via HTTP, and SSL termination is handled by an external reverse proxy (e.g., Nginx).

Example Nginx configuration:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate     /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8787;  # specify the port configured for obsidian-ai-bridge here
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
### Start the proxy without SSL:
  ```bash
  obsidian-ai-bridge --host 127.0.0.1 --port 8787 # Specify the port configured for your reverse proxy here
  ```

## 2. Running on a Remote Server With SSL (Without Reverse Proxy)

Obsidian AI Bridge itself handles HTTPS connections.
You must provide paths to your SSL certificate and private key (PEM format) and ensure the user running the utility has read access to these files.

**Warning:** Running the proxy with direct access to SSL certificates is less secure than using a reverse proxy. Use only if you understand the risks.
Example:
  ```bash
  obsidian-ai-bridge --host 0.0.0.0 --port 8787 --ssl-cert /path/to/fullchain.pem --ssl-key /path/to/privkey.pem
  ```
Make sure the certificate and key files are readable by the user running the proxy.

## 3. Local Installation (Same Machine as Obsidian)

For local use, you can run the proxy without SSL:
  ```bash
  obsidian-ai-bridge --host 127.0.0.1 --port 8080
  ```
In the Copilot plugin settings at step 8, specify endpoint: `http://127.0.0.1:8787`

---

# Installation and Autostart Instructions

## Linux
1. **Installation:**
   ```bash
   pip install obsidian-ai-bridge
   ```
2. **Autostart (systemd):**
   Create file `/etc/systemd/system/obsidian-ai-bridge.service`:
   ```ini
   [Unit]
   Description=Obsidian AI Bridge Proxy
   After=network.target

   [Service]

   # Example launch on address http://127.0.0.1:8787
   ExecStart=/usr/local/bin/obsidian-ai-bridge --host 127.0.0.1 --port 8787

   Restart=always
   User=youruser

   [Install]
   WantedBy=multi-user.target
   ```
   Then run:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable obsidian-ai-bridge
   sudo systemctl start obsidian-ai-bridge
   ```

## Windows
1. **Installation:**
   ```powershell
   pip install obsidian-ai-bridge
   ```
2. **Autostart:**
   - Create a shortcut to run `obsidian-ai-bridge` and place it in the Startup folder, or use Task Scheduler to run the command at login.

## macOS
1. **Installation:**
   ```bash
   pip install obsidian-ai-bridge
   ```
2. **Autostart (launchd):**
   - Create a `plist` file in `~/Library/LaunchAgents/` to run the proxy at login. Example:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.obsidian-ai-bridge.proxy</string>
       <key>ProgramArguments</key>
       <array>
           <string>/usr/local/bin/obsidian-ai-bridge</string>
           <string>--host</string>
           <string>127.0.0.1</string>
           <string>--port</string>
           <string>8787</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
   </dict>
   </plist>
   ```
   Then load it with:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.obsidian-ai-bridge.proxy.plist
   ```

---

### Important for macOS users

Binding to addresses like `127.0.0.3` and others different from `127.0.0.1` does not work on macOS by default, even if you add them to `/etc/hosts`. The system only supports `127.0.0.1` (loopback) and `0.0.0.0` (all interfaces).

**Recommended:**
- Use `--host 127.0.0.1` for local access
- Or `--host 0.0.0.0` to listen on all interfaces

Example:
```bash
obsidian-ai-bridge --host 127.0.0.1 --port 8787
```

Adding `127.0.0.3` to `/etc/hosts` only affects DNS, but does not make the address available for binding.


### Docker Installation
1. **Clone the repository or download the image:**
   - For local build:
     ```bash
     git clone https://githubIvanKorepin/obsidian-ai-bridge.git
     cd obsidian-ai-bridge
     docker build -t obsidian-ai-bridge .
     ```

2. **Create configuration file (optional):**
   - Place `config.toml` or `config.dev.toml` in a convenient directory on your machine.

3. **Run the container:**
   - For production (example with config mounting and port forwarding):
     ```bash
     docker run -d \
       --name obsidian-ai-bridge \
       -p 8787:8787 \
       -v /path/to/config.toml:/app/config.toml \
       obsidian-ai-bridge
     ```
   - For development (with live reload, if supported):
     ```bash
     docker-compose -f docker-compose.dev.yml up
     ```
   - You can specify launch parameters directly:
     ```bash
     docker run -d \
       --name obsidian-ai-bridge \
       -p 8080:8080 \
       obsidian-ai-bridge --host 0.0.0.0 --port 8080
     ```

4. **Check functionality:**
   - Open in browser: [http://localhost:8787](http://localhost:8787) (or the port you specified).

**Notes:**
- For SSL certificates use volume mounting:
  ```bash
  -v /path/to/fullchain.pem:/app/fullchain.pem
  -v /path/to/privkey.pem:/app/privkey.pem
  ```
  and add parameters `--ssl-cert /app/fullchain.pem --ssl-key /app/privkey.pem` to the launch command.
- For environment variable configuration use `--env-file` flag or `-e`.

**Example docker-compose.yml:**
```yaml
version: "3"
services:
  obsidian-ai-bridge:
    image: obsidian-ai-bridge
    ports:
      - "8787:8787"
    volumes:
      - ./config.toml:/app/config.toml
    restart: unless-stopped
```

## Running and Debugging in Devcontainer

If you use [Devcontainer](https://code.visualstudio.com/docs/devcontainers/containers) (e.g., via VS Code), setting up and running obsidian-ai-bridge for development and debugging is maximally simplified:

1. **Open project in VS Code** — if `.devcontainer` folder exists, the editor will suggest opening the project in a container.
2. **Devcontainer will automatically install dependencies** and activate virtual environment.
3. **Running server for debugging:**
   - Open terminal inside the container.
   - Start server with live reload (if supported):
     ```bash
     uvicorn obsidian-ai-bridge.main:app --reload --host 0.0.0.0 --port 8787
     ```
     or use your launch command.
   - For passing environment variables or configs use volume mounting or `.env` files.
4. **Port forwarding:**  
   Devcontainer automatically forwards ports specified in `.devcontainer/devcontainer.json` (e.g., 8787). You'll be able to open the server in host browser at [http://localhost:8787](http://localhost:8787).
5. **Code debugging:**  
   You can use VS Code's built-in Python debugger — set breakpoints and run debugging session.



## Uninstallation

- **pip (any OS):**
  ```bash
  pip uninstall obsidian-ai-bridge
  ```
- **Docker:**
  - Remove the image:
    ```bash
    docker rmi obsidian-ai-bridge
    ```
  - Remove containers (if any):
    ```bash
    docker ps -a | grep obsidian-ai-bridge
    docker rm <container_id>
    ```
- **Devcontainer (VS Code):**
  - Remove the devcontainer from the VS Code UI or delete the `.devcontainer` folder.

For more details, see your platform's package and container management documentation.

For more details, see your platform's package and container management documentation.

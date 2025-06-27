# Руководство по настройке obsidian2perplexity

В obsidian2perplexity есть два способа конфигурирования:

1. **Через параметры командной строки**: вы можете указать host, port, ssl-cert и ssl-key прямо при запуске утилиты:
   ```bash
   obsidian2perplexity --host 0.0.0.0 --port 8080 --ssl-cert /path/to/fullchain.pem --ssl-key /path/to/privkey.pem
   ```
   Если вы не указываете эти параметры, будут использованы значения из конфигурационного файла или значения по умолчанию.

2. **Через конфигурационный файл**: создайте файл `config.default.toml` (или `config.dev.toml`) в рабочей директории. Путь к файлу можно указать как позиционный аргумент после названия пакета:
   ```bash
   obsidian2perplexity config.default.toml
   ```
   Если путь не указан, утилита будет искать `config.default.toml` в текущей директории и в директории пакета.

   Пример шаблона:
   ```toml
   [routing]
   PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions" # URL API Perplexity (менять не требуется)
   ALLOWED_ORIGINS = "app://obsidian.md" # Разрешённые источники для CORS (обычно менять не требуется)

   [server]
   HOST = "0.0.0.0"
   PORT = 8080
   # SSL_CERTFILE = "/path/to/fullchain.pem"
   # SSL_KEYFILE = "/path/to/privkey.pem"
   ```
   - **PERPLEXITY_API_URL** — адрес API Perplexity, на который будут проксироваться запросы. Обычно менять не требуется.
   - **ALLOWED_ORIGINS** — список разрешённых источников для CORS (например, для работы с Obsidian). Обычно менять не требуется.

## 1. Запуск на удалённом сервере без SSL (через reverse proxy, например, Nginx)

- **Рекомендуется для продакшена.**
- Прокси работает только по HTTP, а SSL-терминация осуществляется через внешний reverse proxy (например, Nginx).
- Пример конфига Nginx:

```nginx
server {
    listen 443 ssl;
    server_name ваш-домен.рф;

    ssl_certificate     /etc/letsencrypt/live/ваш-домен.рф/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ваш-домен.рф/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8080;  # или ваш порт прокси
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
- Запуск прокси без SSL:
  ```bash
  obsidian2perplexity --host 127.0.0.1 --port 8080
  ```

## 2. Запуск на удалённом сервере с SSL (без reverse proxy)

- Прокси сам обрабатывает HTTPS-соединения.
- Необходимо указать пути к SSL-сертификату и приватному ключу (PEM) и убедиться, что пользователь, от имени которого запускается утилита, имеет права на чтение этих файлов.
- **Внимание:** запуск прокси с прямым доступом к SSL-сертификатам менее безопасен, чем через reverse proxy. Используйте только если понимаете риски.
- Пример:
  ```bash
  obsidian2perplexity --host 0.0.0.0 --port 8080 --ssl-cert /path/to/fullchain.pem --ssl-key /path/to/privkey.pem
  ```
- Проверьте, что файлы сертификата и ключа доступны на чтение пользователю, запускающему прокси.

## 3. Установка на локальной машине (там же, где Obsidian)

- Для локального использования можно запускать прокси без SSL:
  ```bash
  obsidian2perplexity --host 127.0.0.1 --port 8080
  ```
- В настройках плагина Obsidian AI укажите endpoint: `http://127.0.0.1:8080`

---

# Инструкция по установке и автозапуску

## Linux
1. **Установка:**
   ```bash
   pip install obsidian2perplexity
   ```
2. **Автозапуск (systemd):**
   Создайте файл `/etc/systemd/system/obsidian2perplexity.service`:
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
   Затем выполните:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable obsidian2perplexity
   sudo systemctl start obsidian2perplexity
   ```

## Windows
1. **Установка:**
   ```powershell
   pip install obsidian2perplexity
   ```
2. **Автозапуск:**
   - Создайте ярлык для запуска `obsidian2perplexity` и поместите его в папку автозагрузки, либо используйте Task Scheduler для запуска при входе в систему.

## macOS
1. **Установка:**
   ```bash
   pip install obsidian2perplexity
   ```
2. **Автозапуск (launchd):**
   - Создайте файл plist в `~/Library/LaunchAgents/` для запуска прокси при входе в систему. Пример:
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
   Затем загрузите его:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.obsidian2perplexity.proxy.plist
   ```

## Удаление утилиты

- **pip (любая ОС):**
  ```bash
  pip uninstall obsidian2perplexity
  ```
- **Docker:**
  - Удалить образ:
    ```bash
    docker rmi obsidian2perplexity
    ```
  - Удалить контейнеры (если есть):
    ```bash
    docker ps -a | grep obsidian2perplexity
    docker rm <container_id>
    ```
- **Devcontainer (VS Code):**
  - Удалите devcontainer через интерфейс VS Code или удалите папку `.devcontainer`.

Подробнее см. документацию по управлению пакетами и контейнерами вашей платформы.

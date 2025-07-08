# Руководство по настройке obsidian-ai-bridge

В obsidian-ai-bridge есть два способа конфигурирования:

1. **Через параметры командной строки**: вы можете указать host, port, ssl-cert и ssl-key прямо при запуске утилиты:
   ```bash
   obsidian-ai-bridge --host 0.0.0.0 --port 8080 --ssl-cert /path/to/fullchain.pem --ssl-key /path/to/privkey.pem
   ```
   Если вы не указываете эти параметры, будут использованы значения из конфигурационного файла или значения по умолчанию.

2. **Через конфигурационный файл**: создайте файл `config.toml` (или `config.dev.toml`) в рабочей директории. Путь к файлу можно указать как позиционный аргумент после названия пакета:
   ```bash
   obsidian-ai-bridge config.default.toml
   ```
   Если путь не указан, утилита будет искать `config.toml` в текущей директории и в директории пакета.

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

**Рекомендуется для продакшена.** 

Этот метод является наиболее безопасным т.к., с одной стороны, он использует шифрование SSL, а с другой - не требует предоставлять приложению obsidian-ai-bridge доступ к вашему сертификату и закрытому ключу SSL.

Прокси работает только по HTTP, а SSL-терминация осуществляется через внешний reverse proxy (например, Nginx).

Пример конфига Nginx:

```nginx
server {
    listen 443 ssl;
    server_name ваш-домен.рф;

    ssl_certificate     /etc/letsencrypt/live/ваш-домен.рф/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ваш-домен.рф/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8787;  # укажите здесь порт, на который настроен obsidian-ai-bridge
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
### Запуск прокси без SSL:
  ```bash
  obsidian-ai-bridge --host 127.0.0.1 --port 8787 # Укажите здесь порт, на который настроен Ваш reverse proxy
  ```

## 2. Запуск на удалённом сервере с SSL (без reverse proxy)

Obsidian AI Bridge сам обрабатывает HTTPS-соединения.
Необходимо указать пути к SSL-сертификату и приватному ключу (PEM) и убедиться, что пользователь, от имени которого запускается утилита, имеет права на чтение этих файлов.

**Внимание:** запуск прокси с прямым доступом к SSL-сертификатам менее безопасен, чем через reverse proxy. Используйте только если понимаете риски.
Пример:
  ```bash
  obsidian-ai-bridge --host 0.0.0.0 --port 8787 --ssl-cert /path/to/fullchain.pem --ssl-key /path/to/privkey.pem
  ```
Проверьте, что файлы сертификата и ключа доступны на чтение пользователю, запускающему прокси.

## 3. Установка на локальной машине (там же, где Obsidian)

Для локального использования можно запускать прокси без SSL:
  ```bash
  obsidian-ai-bridge --host 127.0.0.1 --port 8080
  ```
В настройках плагина Copilot на шаге 8 укажите endpoint: `http://127.0.0.1:8787`

---

# Инструкция по установке и автозапуску

## Linux
1. **Установка:**
   ```bash
   pip install obsidian-ai-bridge
   ```
2. **Автозапуск (systemd):**
   Создайте файл `/etc/systemd/system/obsidian-ai-bridge.service`:
   ```ini
   [Unit]
   Description=Obsidian AI Bridge Proxy
   After=network.target

   [Service]

   # Пример запуска на адресе http://127.0.0.1:8787
   ExecStart=/usr/local/bin/obsidian-ai-bridge --host 127.0.0.1 --port 8787

   Restart=always
   User=youruser

   [Install]
   WantedBy=multi-user.target
   ```
   Затем выполните:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable obsidian-ai-bridge
   sudo systemctl start obsidian-ai-bridge
   ```

## Windows
1. **Установка:**
   ```powershell
   pip install obsidian-ai-bridge
   ```
2. **Автозапуск:**
   - Создайте ярлык для запуска `obsidian-ai-bridge` и поместите его в папку автозагрузки, либо используйте Task Scheduler для запуска при входе в систему.

## macOS
1. **Установка:**
   ```bash
   pip install obsidian-ai-bridge
   ```
2. **Автозапуск (launchd):**
   - Создайте файл plist в `~/Library/LaunchAgents/` для запуска прокси при входе в систему. Пример:
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
   Затем загрузите его:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.obsidian-ai-bridge.proxy.plist
   ```

---

### Важно для пользователей macOS

Привязка (bind) к адресам вроде `127.0.0.3` и других отличных от `127.0.0.1` на macOS не работает по умолчанию, даже если добавить их в `/etc/hosts`. Система поддерживает только `127.0.0.1` (loopback) и `0.0.0.0` (все интерфейсы).

**Рекомендуется:**
- Используйте `--host 127.0.0.1` для локального доступа
- Или `--host 0.0.0.0` для прослушивания на всех интерфейсах

Пример:
```bash
obsidian-ai-bridge --host 127.0.0.1 --port 8787
```

Добавление `127.0.0.3` в `/etc/hosts` влияет только на DNS, но не делает адрес доступным для bind.


### Установка в Docker 
1. **Склонируйте репозиторий или скачайте образ:**
   - Для локальной сборки:
     ```bash
     git clone https://github.com/IvanKorepin/obsidian-ai-bridge.git
     cd obsidian-ai-bridge
     docker build -t obsidian-ai-bridge .
     ```

2. **Создайте файл конфигурации (опционально):**
   - Поместите `config.toml` или `config.dev.toml` в удобную директорию на вашей машине.

3. **Запустите контейнер:**
   - Для продакшена (пример с монтированием конфига и пробросом порта):
     ```bash
     docker run -d \
       --name obsidian-ai-bridge \
       -p 8787:8787 \
       -v /path/to/config.toml:/app/config.toml \
       obsidian-ai-bridge
     ```
   - Для разработки (с live reload, если поддерживается):
     ```bash
     docker-compose -f docker-compose.dev.yml up
     ```
   - Можно указать параметры запуска напрямую:
     ```bash
     docker run -d \
       --name obsidian-ai-bridge \
       -p 8080:8080 \
       obsidian-ai-bridge --host 0.0.0.0 --port 8080
     ```

4. **Проверьте работу:**
   - Откройте в браузере: [http://localhost:8787](http://localhost:8787) (или порт, который указали).

**Примечания:**
- Для SSL-сертификатов используйте volume-монтирование:
  ```bash
  -v /path/to/fullchain.pem:/app/fullchain.pem
  -v /path/to/privkey.pem:/app/privkey.pem
  ```
  и добавьте параметры `--ssl-cert /app/fullchain.pem --ssl-key /app/privkey.pem` к команде запуска.
- Для настройки переменных окружения используйте флаг `--env-file` или `-e`.

**Пример docker-compose.yml:**
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

## Запуск и отладка в Devcontainer

Если вы используете [Devcontainer](https://code.visualstudio.com/docs/devcontainers/containers) (например, через VS Code), настройка и запуск obsidian-ai-bridge для разработки и отладки максимально упрощены:

1. **Откройте проект в VS Code** — при наличии `.devcontainer` папки редактор предложит открыть проект в контейнере.
2. **Devcontainer автоматически установит зависимости** и активирует виртуальное окружение.
3. **Запуск сервера для отладки:**
   - Откройте терминал внутри контейнера.
   - Запустите сервер с live reload (если поддерживается):
     ```bash
     uvicorn obsidian-ai-bridge.main:app --reload --host 0.0.0.0 --port 8787
     ```
     или используйте вашу команду запуска.
   - Для передачи переменных окружения или конфигов используйте volume-монтирование или `.env` файлы.
4. **Проброс портов:**  
   Devcontainer автоматически пробрасывает порты, указанные в `.devcontainer/devcontainer.json` (например, 8787). Вы сможете открыть сервер в браузере хоста по адресу [http://localhost:8787](http://localhost:8787).
5. **Отладка кода:**  
   Можно использовать встроенный отладчик VS Code для Python — установите breakpoint и запустите отладочную сессию.



## Удаление утилиты

- **pip (любая ОС):**
  ```bash
  pip uninstall obsidian-ai-bridge
  ```
- **Docker:**
  - Удалить образ:
    ```bash
    docker rmi obsidian-ai-bridge
    ```
  - Удалить контейнеры (если есть):
    ```bash
    docker ps -a | grep obsidian-ai-bridge
    docker rm <container_id>
    ```
- **Devcontainer (VS Code):**
  - Удалите devcontainer через интерфейс VS Code или удалите папку `.devcontainer`.

Подробнее см. документацию по управлению пакетами и контейнерами вашей платформы.

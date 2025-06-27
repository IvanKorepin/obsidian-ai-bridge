# Obsidian to Perplexity Proxy

**Работает совместно с плагином [Obsidian Copilot](https://github.com/logancyang/obsidian-copilot).**

**English version:** [README.md](README.md)

> **Внимание к приватности:** Утилита лишь изменяет заголовки запросов и не читает, не собирает и не хранит содержимое тела запросов. Никакие пользовательские данные не логируются и не сохраняются.

Python-прокси для пересылки запросов от Obsidian к Perplexity с поддержкой CORS. Проект контейнеризован (Docker), поддерживает локальную разработку и продакшн.

## Возможности
- Прокси на FastAPI для Perplexity API
- Корректная работа CORS для интеграции с Obsidian
- Гибкая настройка через TOML-файл (dev/prod)
- Поддержка Docker и devcontainer

## Установка

Установите утилиту из PyPI:
```bash
pip install obsidian2perplexity
```

После установки команда `obsidian2perplexity` будет доступна в терминале.

> **См. [docs/configuration.rus.md](docs/configuration.rus.md) для инструкций по установке и запуску на разных платформах (Linux, Windows, macOS, Docker, devcontainer, systemd и др.).**

## Быстрый старт (локально)

1. **Установите пакет:**
   ```bash
   pip install obsidian2perplexity
   ```
2. **Подготовьте конфиг:**
   Поместите `config.default.toml` в рабочую директорию или укажите путь к нему как позиционный аргумент:
   ```bash
   obsidian2perplexity config.default.toml
   ```
3. **Запустите сервер:**
   ```bash
   obsidian2perplexity --host 0.0.0.0 --port 8080
   ```
   По умолчанию утилита ищет `config.default.toml` в текущей директории или в пакете.

## Использование с Docker

1. **Соберите образ:**
   ```bash
   docker build -t obsidian2perplexity .
   ```
2. **Запустите контейнер:**
   ```bash
   docker run -p 8080:8080 obsidian2perplexity
   ```
   Можно смонтировать свой конфиг:
   ```bash
   docker run -p 8080:8080 -v $(pwd)/config.default.toml:/app/config.default.toml obsidian2perplexity
   ```

## Devcontainer

1. **Откройте проект в VS Code.**
2. **Reopen in Container** через "Remote - Containers".
3. **Devcontainer автоматически установит зависимости и подготовит окружение.**
4. **Запуск сервера внутри devcontainer:**
   ```bash
   python -m obsidian2perplexity.cli --host 0.0.0.0 --port 8080
   ```
   или используйте entrypoint:
   ```bash
   obsidian2perplexity --host 0.0.0.0 --port 8080
   ```

## Конфигурация

См. подробное [руководство по настройке](docs/configuration.rus.md) с примерами и вариантами использования.

Прокси настраивается через TOML-файл (по умолчанию `config.default.toml`). Пример:

```toml
[routing]
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions" # URL API Perplexity (обычно менять не требуется)
ALLOWED_ORIGINS = "app://obsidian.md" # Разрешённые источники для CORS (обычно менять не требуется)

[server]
HOST = "0.0.0.0"
PORT = 8080
# SSL_CERTFILE = "/path/to/fullchain.pem"
# SSL_KEYFILE = "/path/to/privkey.pem"
```

- **[routing]**: настройки маршрутизации и CORS.
- **[server]**: параметры запуска сервера (host, port и др.).
- Можно создавать отдельные файлы для dev/prod окружений.

## Лицензия
MIT

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

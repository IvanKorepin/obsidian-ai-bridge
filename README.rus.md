<h1 style="text-align: center;"> Obsidian AI Bridge </h1>

**Универсальный AI-прокси сервер для плагина Obsidian Copilot**

**English version:** [README.md](README.md)

## Что оно делает

Плагин Copilot для Obsidian позволяет подключаться к API многих популярных AI-сервисов, таких как OpenAI, DeepSeek и другие. Однако некоторые популярные сервисы, такие как Perplexity и Google Gemini, не поддерживаются напрямую из-за различий в API и ограничений CORS.

**Obsidian AI Bridge** решает эту проблему, предоставляя универсальный прокси-сервер, который:
- **Преодолевает различия в форматах API** между Obsidian и AI-сервисами
- **Обрабатывает ограничения CORS**, которые препятствуют прямым подключениям из браузера
- **Поддерживает несколько AI-сервисов**: Perplexity для чат-моделей и Google Gemini для эмбеддингов
- **Преобразует запросы и ответы** для соответствия ожидаемым форматам

Прокси может быть развернут на вашем сервере или локально на компьютере, где запущен Obsidian.

> **Примечание о конфиденциальности:** Утилита только преобразует форматы запросов/ответов и обрабатывает маршрутизацию. Никакие пользовательские данные не логируются, не сохраняются и не изменяются, кроме преобразования формата.

## Поддерживаемые сервисы

- **Perplexity API**: Чат-модели и модели рассуждений
- **Google Gemini**: Модели текстовых эмбеддингов (могут применяться географические ограничения)

## Возможности
- **Универсальная обработка эндпоинтов**: маршруты `/perplexity/*` направляются в Perplexity, `/gemini/embeddings` в Gemini
- **Установка pip-пакета**: Простая установка и обновления
- **CLI интерфейс**: Простая настройка через командную строку
- **Гибкое развертывание**: Локально, на сервере или в контейнере
- **Поддержка SSL**: HTTPS с пользовательскими сертификатами
- **Обработка CORS**: Полная поддержка кросс-доменных запросов
- **Настраиваемость**: Конфигурационные файлы TOML
- **Логирование**: Подробное логирование запросов/ответов для отладки

## Установка

Установите утилиту из PyPI:
```bash
pip install obsidian-ai-bridge
```

После установки команда `obsidian-ai-bridge` будет доступна в терминале.

## Быстрый старт (локально)

1. **Установите пакет:**
   ```bash
   pip install obsidian-ai-bridge
   ```

2. **Запустите сервер:**
   ```bash
   # Базовое использование (по умолчанию localhost:8000)
   obsidian-ai-bridge
   
   # Пользовательский хост и порт
   obsidian-ai-bridge --host 127.0.0.1 --port 8787
   
   # С SSL сертификатами
   obsidian-ai-bridge --host 0.0.0.0 --port 443 --ssl-cert cert.pem --ssl-key key.pem
   ```

3. **Доступные эндпоинты:**
   - `POST /perplexity/*` - Проксирует в Perplexity API (поддерживаются все пути)
   - `POST /gemini/embeddings` - Проксирует в Google Gemini Embedding API
   - `GET /health` - Эндпоинт проверки работоспособности

> См. [документацию](docs/configuration.rus.md) для более подробных инструкций по установке и настройке в разных окружениях (Linux, Windows, macOS, Docker, devcontainer).

## Настройка с Obsidian Copilot

### Для Perplexity (чат-модели)

1. Установите плагин Copilot для Obsidian согласно [официальной документации](https://github.com/logancyang/obsidian-copilot)

2. Перейдите в настройки плагина
![Переход в настройки](/docs/img/copilot_configure_step1_rus.png)

3. Перейдите на вкладку Model
![Вкладка Model](/docs/img/copilot_configure_step2_rus.png)

4. Прокрутите страницу вниз до конца предустановленных моделей

5. Нажмите кнопку "Add custom model"
![Вкладка Model](/docs/img/copilot_configure_step3_rus.png)

6. **Настройте модель Perplexity:**
![Форма Model](/docs/img/copilot_configure_step4.png)
   1) **Название модели**: Выберите из [доступных моделей Perplexity](https://docs.perplexity.ai/docs/model-cards) (например, `llama-3.1-sonar-small-128k-online`, `llama-3.1-sonar-large-128k-online`)
   2) **Формат**: Выберите "Open AI Format"
   3) **URL хоста**: 
      - Локально: `http://localhost:8787/perplexity`
      - На сервере: `https://YOUR_DOMAIN/ai/perplexity`
   4) **API токен**: Ваш API-ключ Perplexity с [perplexity.ai](https://www.perplexity.ai/settings/api)
   5) **Enable CORS**: ✅ Установите эту галочку
   6) **Нажмите "Verify"** для проверки подключения

### Для Google Gemini (модели эмбеддингов)

7. **Добавьте модель эмбеддингов Gemini:**
   1) **Название модели**: `text-embedding-004` или другие [модели эмбеддингов Gemini](https://ai.google.dev/gemini-api/docs/embeddings)
   2) **Формат**: Выберите "Open AI Format"
   3) **URL хоста**:
      - Локально: `http://localhost:8787/gemini`
      - На сервере: `https://YOUR_DOMAIN/ai/gemini`
   4) **API токен**: Ваш API-ключ Google AI из [Google AI Studio](https://aistudio.google.com/app/apikey)
   5) **Enable CORS**: ✅ Установите эту галочку
   6) **Нажмите "Verify"** для проверки подключения

> **Примечание:** Google Gemini API может быть ограничен в некоторых регионах (например, в России). При необходимости используйте VPN.

8. **Подтверждение успеха:**
   ![Успешное подключение](/docs/img/copilot_configure_success.png)

   Поздравляем! Ваша система теперь успешно настроена для использования как чат-моделей, так и моделей эмбеддингов.

## Параметры командной строки

```bash
obsidian-ai-bridge [ОПЦИИ] [ПУТЬ_К_КОНФИГУ]

Опции:
  --host TEXT      Хост для привязки (по умолчанию: localhost)
  --port INTEGER   Порт для запуска (по умолчанию: 8000)
  --ssl-cert TEXT  Путь к файлу SSL-сертификата
  --ssl-key TEXT   Путь к файлу SSL-ключа
  --help           Показать справочное сообщение

Примеры:
  obsidian-ai-bridge                                    # Запуск на localhost:8000
  obsidian-ai-bridge --host 0.0.0.0 --port 8787       # Пользовательский хост/порт
  obsidian-ai-bridge config.toml --host 0.0.0.0       # Использование файла конфигурации
```

## Конфигурация

См. подробное [руководство по настройке](docs/configuration.rus.md) с примерами и вариантами использования.

## Лицензия
MIT

## Удаление утилиты

- **pip (любая ОС):**
  ```bash
  pip uninstall obsidian-ai-bridge
  ```

Подробнее см. документацию по управлению пакетами и контейнерами вашей платформы.

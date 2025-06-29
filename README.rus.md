<h1 style="text-align: center;"> Obsidian to Perplexity Proxy </h1>

**Работает совместно с плагином [Obsidian Copilot](https://github.com/logancyang/obsidian-copilot).**

**English version:** [README.md](README.md)

## Что оно делает

Плагин Copilot для Obsidian позволяет подключаться к API многих популярных AI-сервисов, таких как OpenAI, Gemini, DeepSeek и другие. Естественно, при условии, что у вас есть подписка на эти модели и соответсвующие API-токены.
К сожалению, плагин не поддерживает популярный сервис Perplexity.
Obsidian2Perplexity решает эту проблему. O2P это простой и легкий прокси-сервер, который встает между Obsidian-Copilot и Perplexity преобразует заголовки Ваших https-запросов, так, чтобы их понимал Perplexity API и возвращает ответы.

O2P может быть развернут на вашем сервере или хостинге и обеспечивать подключение с любых устройств, либо на вашем компьютере, где запущен Obsidian. 

> **Внимание к приватности:** Утилита лишь изменяет заголовки запросов и не читает, не собирает и не хранит содержимое тела запросов. Никакие пользовательские данные не логируются и не сохраняются.

## Возможности
- Установка на сервером или локальной машине
- Работа совместно с reverse proxy или без него
- Поддержка SSL
- Корректная работа CORS для интеграции с Obsidian
- Гибкая настройка через TOML-файл
- Поддержка Docker и devcontainer для разработки

## Установка

Установите утилиту из PyPI:
```bash
pip install obsidian2perplexity
```

После установки команда `obsidian2perplexity` будет доступна в терминале.

## Быстрый старт (локально)

1. Установите пакет:
   ```bash
   pip install obsidian2perplexity
   ```

2. Запустите сервер:
   ```bash
   obsidian2perplexity --host 127.0.0.1 --port 8787
   ```

> См. [инструкцию](docs/configuration.rus.md) для более тонкой установке и настройке в разных окружениях (Linux, Windows, macOS, Docker, devcontainer).

3. Установите плагин Copilot для Obsidian согласно [официальной документации](https://github.com/logancyang/obsidian-copilot)

4. Перейдите в настройки плагина
![Переход в настройки](/docs/img/copilot_configure_step1_rus.png)

5. Перейдите на вкладку 
![Вкладка Model](/docs/img/copilot_configure_step2_rus.png)

6. Прокурутите страницу несного вниз до конца предустановленных моделей

7. Нажмите кнопку "Add custom model"
![Вкладка Model](/docs/img/copilot_configure_step3_rus.png)

8. Заполните форму
![Форма Model](/docs/img/copilot_configure_step4.png)
   1) Название модели Perplexity ([Список доступных моделей по мнению саого Perplexity](https://www.perplexity.ai/search/kakie-modeli-podderzhivaet-api-MCb_.seRSF2SbY91Wh6QjQ))
   2) Выберете пункт "Open AI Format"
   3) Параметры хоста, на котором развернут Obsidian2Perplexity
      3.1) Для локальной установки ```http://localhost:8787/```
      3.2) Для установки на сервере ```https://YOUR_IP_ADDRESS:8787```

      > **Примечание 1:** Адрес хоста и порт можно задать при запуске утилиты ```obsidian2perplexity --host YOUR_IP --port YOUR_PORT```

      > **Примечание 2:** Убедитесь, что выбранный прот открыт для подключения.
      
   4) Введите Ваш API-token от вашего аккаунта Perplexity

   5) Установите галочку "Enable CORS" 
   6) Нажмите на кнопку "Verify", чтобы убедиться, что все работает. Если все настроено верно, то в углу экрана появится сообщение об успешном подключении
   ![Успешное подключение](/docs/img/copilot_configure_success.png)

   Поздравляю! Теперь ваша система успешно настроена
   ```

## Конфигурация

См. подробное [руководство по настройке](docs/configuration.rus.md) с примерами и вариантами использования.

## Лицензия
MIT

## Удаление утилиты

- **pip (любая ОС):**
  ```bash
  pip uninstall obsidian2perplexity
  ```

Подробнее см. документацию по управлению пакетами и контейнерами вашей платформы.

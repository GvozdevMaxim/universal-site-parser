Universal News Parser

Universal News Parser — это гибкий парсер новостных сайтов на Python, который работает на основе XPath-выражений, хранящихся в базе данных. Позволяет легко подключать новые сайты без изменения кода, просто обновив таблицу resource.

Возможности

    Парсинг новостей с любых сайтов через XPath

    Получение: ссылки, заголовка, текста статьи, даты публикации

    Преобразование относительных ссылок в абсолютные

    Хранение данных в MySQL (таблица items)

    Простая настройка через таблицу resource

    Docker-сборка: MySQL + Python

Технологии

    Python 3.12

    beautifulsoup4 4.12.3

    lxml 5.2.1

    fake-useragent 1.5.1

    requests 2.32.2

    mysql-connector-python 8.3.0

    dateparser 1.2.0

    tzlocal 5.2

    MySQL 8.0

    Docker 24.x

    Docker Compose 2.x

Установка и запуск

    Клонировать проект:

git clone https://github.com/your_username/universal-news-parser.git
cd universal-news-parser

    Создать файл .env на основе шаблона:

cp .env.example .env

    Запустить проект:

docker-compose up --build

При первом запуске:

    Поднимется MySQL с таблицами и данными

    Парсер автоматически выполнит парсинг и выведет результат в консоль

Структура базы данных

Таблица resource:

    resource_name — Название источника

    resource_url — Ссылка на раздел с новостями

    top_tag — XPath до ссылок на статьи

    bottom_tag — XPath до содержимого статьи

    title_cut — XPath до заголовка

    date_cut — XPath до даты публикации

Таблица items:

    res_id — ID источника (resource.id)

    link — Абсолютная ссылка на новость

    title — Заголовок новости

    content — Текст статьи

    nd_date — UNIX-время публикации

    s_date — UNIX-время добавления

    not_date — Дата публикации (человеко-читаемый формат)

Пример вывода парсера

1.SITE_ID = 1
2.LINK = https://www.nur.kz/society/123456
3.TITLE: Новый закон принят в Казахстане
4.CONTENT: Полный текст статьи...
5.DATETIME: 2024-10-17
6.UNIXTIME: 1729166500
7.ADDTIME: 1729167000

init.sql

Проект включает файл init.sql, который:

    Создаёт таблицы resource и items

    Вставляет демо-данные для сайта nur.kz

init.sql выполняется автоматически при первом запуске контейнера MySQL.

Структура проекта

universal-news-parser/
├── parser.py
├── database.py
├── utils.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── init.sql
├── .env.example
└── README.md

Автор

GitHub: @GvozdevMaxim

Лицензия

Проект распространяется под лицензией MIT. Разрешено использовать для портфолио, обучения и коммерческих целей.
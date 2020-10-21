# Сервис Foodgram
Выпускная работа курса "Python-разработчик" Яндекс.Практикум.


## Описание
**Foodgram** - это онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.



## Установка и запуск приложения

1. Выполнить установку [docker-ce](https://docs.docker.com/engine/install/) и [docker-compose](https://docs.docker.com/compose/install/)

2. Склонировать репозиторий проекта:

    ```bash
   git clone https://github.com/olgoncharov/foodgram-project.git
   cd foodgram-project
    ```

3. В директории `docker` создать файл `.env` из шаблона `.env.template`:

    ```bash
    cp docker/.env.template docker/.env
    ```

   и установить в нем следующие переменные:
   
   |  Название переменной            | Описание  |
   |---------------------------------|-----------|
   | DJANGO_SUPERUSER_NAME          | Имя суперпользователя, который будет создан при первом запуске приложения |
   | DJANGO_SUPERUSER_EMAIL          | E-mail суперпользователя |
   | DJANGO_SUPERUSER_PASSWORD          | Пароль суперпользователя |
   | HOST_IP          | IP-адрес сервера |
   | HOST_DOMAIN          | Доменное имя сервера (не обязателен для заполнения|
   | POSTGRES_DB          | Имя базы данных PostgreSQL  |
   | POSTGRES_USER          | Пользователь PostgreSQL |
   | POSTGRES_PASSWORD          | Пароль пользователя PostgreSQL |
   | SECRET_KEY          | Секретный ключ для шифрования данных. Произвольный набор символов |

4. В директории проекта выполнить команду:
    ```bash
    docker-compose up -d
    ```
   
 После старта всех контейнеров сервис будет доступен по адресам
 `http://<HOST_IP>:8000/` и `http://<HOST_DOMAIN>:8000/` (если в конфигурации был задан`HOST_DOMAIN`)
 
 Админка доступна по адресу `http://<HOST_IP>:8000/admin/` (`http://<HOST_DOMAIN>:8000/admin/`). Для входа использовать логин и пароль, указанный в переменных `DJANGO_SUPERUSER_NAME` и `DJANGO_SUPERUSER_PASSWORD`

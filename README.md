# api_yamdb
### Описание
API сервиса Yamdb. Позволяет читать и добавлять отзывы о различных произведениях искусства: книгах, фильмах, музыке и не только. Спсисок произведений расширяется администраторами. Дает вызможность выставлять рейтинг произведениям и смотреть их текущий рейтинг на данном ресурсе.
### Технологии
- Python 3.7
- django 2.2.16
- djangorestframework 3.12.4
- djangorestframework-simplejwt 4.7.2
- django-filter 21.1
### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- Выполните миграции. В папке с файлом manage.py выполните команду:
```
 python3.manage.py migtate (windows: py.manage.py migtate)
 ```
- Перенесите в базу данных тестовые данные из csv файлов, используя команду
```
 python3.manage.py db_filling (windows: py.manage.py db_filling)
 ```
- Запустите сервер разработчика. В папке с файлом manage.py выполните команду:
```
python3 manage.py runserver (windows: py manage.py runserver)
```
### Администрирование и особенности
- Для администрирования проекта создайте суперпользователя. В папке с файлом manage.py выполните команду:
```
python3 manage.py createsuperuser (windows: py manage.py createsuperuser)
```
- Админ-зона расположена по относительному адреу /admin/
- Добавлений новых произведений (titles) доступно только суперпользователю и администраторам
### Работа с API
- Зарегистрируйте нового пользователя отправив post запрос на относительный эндпоинт api/v1/auth/signup/. В теле post запроса передайте параметры "username" и "email".
- На переданный email вы получите confirmation_code.
- Получите токен для пользователя отправив post запрос на относительный эндпоинт api/v1/auth/token/, передав username и confirmation_code.
```
curl --location --request POST 'http://127.0.0.1:8000/api/v1/auth/token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "newuser",
    "confirmation_code": "****"
}'
```
- Примеры запросов для получения списка произведений/информации о конкретном произведении
```
curl --location --request GET 'http://127.0.0.1:8000/api/v1/titles/' \
--header 'Authorization: Bearer <ваш токен>' \
--data-raw ''
```
```
curl --location --request GET 'http://127.0.0.1:8000/api/v1/titles/1/' \
--header 'Authorization: Bearer <ваш токен>' \
--data-raw ''
```
- Пример post запроса для оставления отзыва о произведении
```
curl --location --request POST 'http://127.0.0.1:8000/api/v1/titles/1/review/' \
--header 'Authorization: Bearer <ваш токен>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text": "замечательное произведение",
    "score": 10
}'
```
- Полный список возможных эндпоинтов и видов запросов доступен по относительному эндпоинту redoc/

### Авторы в алфавитном порядке:
- Дмитрий Вдонин
- Дмитрий Мисюра
- Майдари Цыденов





### Description
Yamdb service API. Allows you to read and add reviews about various pieces of art: books, films, music and more. The list of art objects is expanded by administrators. Allows you to rate arts and see their current rating on this resource.
### Technologies
- Python 3.7
- django 2.2.16
- djangorestframework 3.12.4
- djangorestframework-simplejwt 4.7.2
- django-filter 21.1
### Running a project in dev mode
- Install and activate the virtual environment
- Install dependencies from requirements.txt file
```
pip install -r requirements.txt
``` 
-  Run the migrations. In the folder with the manage.py file, run the command:

```
 python3.manage.py migtate (windows: py.manage.py migtate)
 ```
- Transfer test data from csv files to the database using the command

```
 python3.manage.py db_filling (windows: py.manage.py db_filling)
 ```
- Start the developer server. In the folder with the manage.py file, run the command:

```
python3 manage.py runserver (windows: py manage.py runserver)
```
### Administration and Features
- Create a superuser to administer the project. In the folder with the manage.py file, run the command:

```
python3 manage.py createsuperuser (windows: py manage.py createsuperuser)
```
- The admin area is located at the relative address /admin/
- Adding new arts (titles) is available only to the superuser and administrators
### Working with the API
- Register a new user by sending a post request to the relative endpoint api/v1/auth/signup/. In the body of the post request, pass the "username" and "email" parameters.
- You will receive a confirmation_code to the email you sent.
- Get a token for the user by sending a post request to the relative endpoint api/v1/auth/token/, passing username and confirmation_code.
```
curl --location --request POST 'http://127.0.0.1:8000/api/v1/auth/token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "newuser",
    "confirmation_code": "****"
}'
```
- Examples of requests for obtaining a list of works/information about a specific piece of art
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
- An example of a post request for leaving feedback on a piece of art
```
curl --location --request POST 'http://127.0.0.1:8000/api/v1/titles/1/review/' \
--header 'Authorization: Bearer <ваш токен>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text": "Great one!",
    "score": 10
}'
```
-  complete list of possible endpoints and types of requests is available at the relative endpoint redoc/

### Authors in alphabetical order:
- Dmitry Vdonin
- Dmitry Misyura
- Maidari Tsydenov

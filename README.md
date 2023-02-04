# Проект «YaMDb API»

### Описание

    Проект YaMDb собирает отзывы пользователей на произведения.  
        Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.  
        Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос),  
    разрешённые типы запросов, права доступа и дополнительные параметры, когда это необходимо.  
        Добавлять произведения, категории и жанры может только администратор.  
        Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку  
    в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения  
    — рейтинг (целое число).<br/>  
        Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.  

### Технологии:
    ![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
    ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
    ![DRF](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
    ![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)

### Используемые пакеты:
    * requests==2.26.0
    * Django==3.2
    * djangorestframework==3.12.4
    * PyJWT==2.1.0
    * pytest==6.2.4
    * pytest-django==4.4.0
    * pytest-pythonpath==0.7.3
    * djangorestframework-simplejwt==5.2.2
    * django-filter==22.1
    * python-dotenv==0.21.1

### Установка

1. Клонировать репозиторий:

   ```python
   git clone ...
   ```

2. Перейти в папку с проектом:

   ```python
   cd api_yamdb/
   ```

3. Установить виртуальное окружение для проекта:

   ```python
   python -m venv venv
   ```

4. Активировать виртуальное окружение для проекта:

   ```python
   # для OS Lunix и MacOS
   source venv/bin/activate
   # для OS Windows
   source venv/Scripts/activate
   ```

5. Установить зависимости:

   ```python
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Выполнить миграции на уровне проекта:

   ```python
   cd yatube_api
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

7. Запустить проект:
   ```python
   python manage.py runserver
   ```

### Дополнительно

* Каждый ресурс описан в документации проекта:
   ```
   http://127.0.0.1:8000/redoc/
   ```

* ПО для тестирования API:
   ```
   https://www.postman.com/
   ```

### Примеры запросов

* Пример POST-запроса 
    Регистрация нового пользователя и получение `confirmation_code`. Доступно без токена.
    `POST http://127.0.0.1:8000/api/v1/auth/signup/`
    ```json
    {
        "email": "user@example.com",
        "username": "string"
    }
    ```
* Пример ответа:
    ```json
    {
        "email": "string",
        "username": "string"
    }
    ```
* Получение JWT-токена в обмен на `username` и `confirmation_code`. Доступно без токена.
    `POST http://127.0.0.1:8000/api/v1/auth/token/`
    ```json
    {
        "username": "string",
        "confirmation_code": "string"
    }
    ```
* Пример ответа:
    ```json
    {
        "token": "string"
    }
    ```

### Авторы проекта
* Артем Вахрушев  
* Роман Дячук  
* Руслан Шамсияров  

# studensts_test
studensts_test
## Требования
* python 3.10
* Django 4.2.1
* djangorestframework 3.14.0
## Установка
1. Скопировать **example.env** в **.env** и заполнить
2. Создать и активировать виртуальное окружение
```
virtualenv venv
source venv/bing/actinvate
```
2. Установить зависимости
```
pip install -r requirements.txt
```
3. Создать и применить миграции
```
python manage.py makemigrations
python manage.py migrate
```
4. Создать сюперпользователя
```
python manage.py createsuperuser
```
5. Заполнить через админку необходимые дикты

## Описание
* Документация в проекте - drf_spectacular (OpenAPI 3)
* Админка /admin
* Апишка /api
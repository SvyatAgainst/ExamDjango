Для квалицификационного экзамена в Сириусе с Django
## Для начала создайте виртуальное окружение:

``` python
python3 -m venv venv
```

После этого активируйте:

```bash 
source /venv/bin/activate
```

Затем установите библиотеки, файл библиотек находится [здесь](https://github.com/SvyatAgainst/ExamDjango/blob/main/requirements.txt).
Команда для установки библиотек:

``` python
pip install -r requirements.txt
```
## Затем создайте проект django:

``` python
django-admin startproject --имя вашего проекта-- .
```

(Точка, чтобы создать в текущей директории, но необязательно), если без точки, то перейдите в директорию, где лежит manage.py
## После этого создайте приложение:

``` python
python manage.py startapp --имя вашего приложения--
```

Далее нужно добавить приложение в setting.py проекта:  ['--имя приложения--'](https://github.com/SvyatAgainst/ExamDjango/blob/main/exam/settings.py#43)

## После этого создаём модель с валидацией (таблицу): примеры таких моделей лежат в [models.py приложении](https://github.com/SvyatAgainst/ExamDjango/blob/main/product/models.py)

> P.S. Валидацию проводить желательно со всеми типами полей в модели. Но после валидации очень важно писать эти строки:

```

def save(self, *args, **kwargs):

self.full_clean()

super().save(*args, **kwargs)

```

Если модель написана, то нужно применить миграцию:

``` python
python manage.py makemigrations

python manage.py showmigrations #Чтобы увидеть миграции

python manage.py migrate
```

## Создаём админ-панель

После создания и мигрирования моделей, нужно создать админку этой модели, как можно догадаться, [пример находится здесь](https://github.com/SvyatAgainst/ExamDjango/blob/main/product/admin.py)

Дальше, чтобы протестировать модель и её валидацию, нужно создать пользователя для admin-панели:

```python
python manage.py createsuperuser
```

> При создании пользователя будет предложен автоматический вариант имени пользователя. После выбора имени, нужен пароль и почта (можно выдумать)

## Для теста можно запустить сервер командой:

``` python
python manage.py runserver

python manage.py runserver 8000 ### Если не работает первый вариант, попробуйте указать конкретный порт
```

## Далее, настройте окружение

Для настройки окружения создайте новый файл [.env](https://github.com/SvyatAgainst/ExamDjango/blob/main/.env). <- Тут пример, но по факту вы можете добавить больше данных, чтобы защитить их. Затем в settings измените получение данных, которые лежат в env:

``` python
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# PORT = os.getenv('PORT', 8000) # Если хочется побольше данных в окружении)
```

Если не установили dotenv:

``` python
pip install dotenv
```

## Добавляем метрики

Чтобы добавить метрики, нужно создать [файл метриков в приложении](https://github.com/SvyatAgainst/ExamDjango/blob/main/product/middleware.py). Файл метриков лежит в примере, но важно учитывать базовую структуру метрики:
``` python
class MetricMiddleware:
	def __init__(self, response):
		self.get_response = response
		...
	def __call__(self, request):
		response = self.get_response(request)
		status_code = response.status_code
		...
		return response
```

Метрики потом обязательно добавить в список [middleware проекта](https://github.com/SvyatAgainst/ExamDjango/blob/main/exam/settings.py#55):
``` python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'product.middleware.MetricMiddleware' # Название вашего файла и класса метрик
]
```

## После этого, собираем статику

Для сбора статики на экзамене был предложен простой способ с помощью библиотеки whitenoise, если не установили:

``` python
pip install whitenoise
```

Затем, добавляем whitenoise в [список middleware проекта](https://github.com/SvyatAgainst/ExamDjango/blob/main/exam/settings.py#46-56), чтобы позволить ему грузить статику:

``` python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    'whitenoise.middleware.WhiteNoiseMiddleware', #<- ОН НАХОДИТСЯ ЗДЕСЬ!!!!4
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'product.middleware.MetricMiddleware'
]
```

Затем, ВАЖНО, добавить путь в [конце файла settings](https://github.com/SvyatAgainst/ExamDjango/blob/main/exam/settings.py#124), куда будет собираться статика:

``` python
# STATIC_URL = 'static/' # Это уже лежит в файле

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Нужно добавить только ЭТО
```

Самый важный этап остался для статики - собрать её, команда ниже:

``` python
python manage.py collectstatic
```

## Теперь надо сделать  тесты, в нашем случае на экзамен надо тест endpoint

В файле [views.py](https://github.com/SvyatAgainst/ExamDjango/blob/main/product/views.py) нужно добавить функцию, которая будет возвращать JSON (структура json не обязательно в таком виде, но она рабочая):

``` python
from django.http import JsonResponse
from .models import *

def health_check(request):
    return JsonResponse({'status': 'ok'})
```

Затем, переходим в файл [tests.py](https://github.com/SvyatAgainst/ExamDjango/blob/main/product/tests.py). Там нужно написать тест, но он будет внизу:

``` python
from django.test import TestCase, Client

class HealthCheckTest(TestCase):
    def test_ping_endpoint(self):
        client = Client()
        response = client.get('/ping/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})
```

Дальше нужно добавить url в [urls.py](https://github.com/SvyatAgainst/ExamDjango/blob/main/product/urls.py), который создаётся в продукте:

``` python
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.product_list, name='product_list'),
    path('ping/', views.health_check, name='ping')
]
```

> ВАЖНО! Если есть файл маршрутизации, его нужно включить в [маршрутизацию проекта](https://github.com/SvyatAgainst/ExamDjango/blob/main/exam/urls.py):
``` python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')) # Включение марщрутизации на уровне проекта
]
```

Чтобы показать тестирование, нужно сделать команду:

``` python
python manage.py test
```

После этого должно вывести сообщение "OK".
### Статика собрана. Работа на 8 баллов выполнена!

# На 10 баллов нужно сделать Frontend часть проекта.


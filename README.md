# ExamDjango
Для квалицификационного экзамена в Сириусе с Django

## Для начала создайте виртуальное окружение:
```python3 -m venv venv```

После этого активируйте:
```source /venv/bin/activate```

Затем установите библиотеки, файл библиотек находится [здесь](https://github.com/SvyatAgainst/ExamDjango/blob/main/requirements.txt)
Команда для установки библиотек: 

```pip install -r requirements.txt```

## Затем создайте проект django: 

```django-admin startproject --имя вашего проекта-- .```
 (Точка, чтобы создать в текущей директории, но необязательно), если без точки, то перейдите в директорию, где лежит manage.py

## После этого создайте приложение:

```python manage.py startapp --имя вашего приложения--```

Далее нужно добавить приложение в setting.py проекта: ['--имя приложения--'](https://github.com/SvyatAgainst/ExamDjango/blob/main/exam/settings.py#43)

## После этого создаём модель с валидацией (таблицу): примеры таких моделей лежат в [models.py приложении](https://github.com/SvyatAgainst/ExamDjango/blob/main/product/models.py)

### P.S. Валидацию проводить желательно со всеми типами полей в модели. Но после валидации очень важно писать эти строки:
```
def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
```

Если модель написана, то нужно применить миграцию:
```markdown
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

### При создании пользователя будет предложен автоматический вариант имени пользователя. После выбора имени, нужен пароль и почта (можно выдумать)

## Для теста можно запустить сервер командой:

```python
python manage.py runserver 
python manage.py runserver 8000 ### Если не работает первый вариант, попробуйте указать конкретный порт
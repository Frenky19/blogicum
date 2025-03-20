# Блогикум — Платформа для ведения блога

https://frenky19.pythonanywhere.com/

Социальная платформа для публикации постов с расширенными возможностями управления контентом.

## 🛠 Технологический стек

### Бэкенд
- **Язык**: Python 3.9+
- **Фреймворк**: Django 3.2+
  - ORM для работы с БД
  - Встроенная аутентификация
  - Админ-панель
  - DTL-шаблонизация
  - CSRF/XSS защита
  - Пагинация ('django.core.paginator')

### Фронтенд
- HTML5 + Django Template Language
- CSS + Bootstrap
- JavaScript:
  - Динамические лайки
  - Валидация форм
  - Анимации

### База данных
- SQLite

## 🚀 Особенности проекта

### Основные функции
- 📝 Создание постов с отложенной публикацией
- 🔐 Ролевая модель доступа:
  - Пользователи: CRUD для своих постов/комментариев
  - Админы: Полный контроль через админку
- 💬 Система комментариев с модерацией
- ❤️ Лайки с AJAX-обновлением
- 📂 Категории и локации (только для админов)
- 📊 Пагинация (10 элементов на странице)

### Безопасность
- Хеширование паролей
- Защита от CSRF/XSS
- Режим DEBUG только для разработки

## 🖥 Установка

1. Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/frenky19/blogicum.git
```
```bash
cd blogicum
```

2. Создать и активировать виртуальное окружение:

```bash
python -m venv env
```
```bash
source env/bin/activate  # Linux
source env/scripts/activate  # Windows
```

3. Установить зависимости:

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

4. Выполнить миграции:

```bash
python manage.py migrate
```

5. Запустить проект:

```bash
python manage.py runserver
```

## 🗂 Структура проекта

### Основные страницы

| Страница             | Функционал                          |
|----------------------|-------------------------------------|
| Главная              | Лента постов с пагинацией           |
| Детали поста         | Полный текст + комментарии          |
| Профиль пользователя | Статистика + список постов автора   |
| Создание поста       | Форма с расширенными настройками    |
| Админ-панель         | Управление контентом и пользователями |

### Модели данных

```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    ... другие поля

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ... другие поля
```

## 📈 Производительность

    Оптимизированные SQL-запросы через select_related и prefetch_related

    Кэширование шаблонов

    # Асинхронная обработка тяжелых задач (Celery + Redis в планах)

## Автор  
[Андрей Головушкин / Andrey Golovushkin](https://github.com/Frenky19)
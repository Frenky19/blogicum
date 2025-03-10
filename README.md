Проект Блогикум.
Бэкенд:
    Язык программирования: Python
    
    Фреймворк: Django — основа проекта. Использованы ключевые компоненты:
        - ORM (Object-Relational Mapping): Для взаимодействия с базой данных без написания SQL-запросов.
        - Аутентификация и авторизация: Встроенная система пользователей, сессии.
        - Админ-панель: Готовая CRM для управления контентом, пользователями и настройками.
        - Шаблонизатор: Генерация HTML на сервере с использованием синтаксиса Django Template Language (DTL), поддержка наследования шаблонов.
        - Маршрутизация: URL-диспетчеризация с помощью urls.py.
        - Миграции: Автоматическое создание и применение миграций для изменения структуры БД.

    Дополнительные модули Django:
        - Защита от CSRF-атак, XSS-уязвимостей через экранирование переменных в шаблонах.

Фронтенд:
    HTML: Семантическая верстка, интеграция с DTL-тегами (циклы, условия, переменные).

    CSS: bootstrap CSS для стилизации.

    JavaScript:
        - Динамические лайки.
        - Обработка событий (клики, отправка форм), анимации.

    Интеграция фронта и бэкенда: Передача данных через контекст шаблонов, формы Django для валидации и рендеринга.

База данных:
    - СУБД: SQLite.
    - Схема данных: Определена через Django-модели (models.py).

Инструменты и инфраструктура:
    - Версионный контроль: Git, хостинг кода - GitHub.
    - Деплой: Pythonanywhere.
    - Менеджер пакетов: Pip, виртуальное окружение (venv).
    - Статика: Сборка через collectstatic.
    - Безопасность: Настройки SECRET_KEY, DEBUG=False в продакшене, хеширование паролей.

Дополнительные технологии:
    - Тестирование: Модульные тесты с pytest. Тестирование views и моделей.


Примеры реализованных функций:
    - Комментарии: Формы Django с валидацией, сохранение в БД через ORM.
    - Пагинация: Использование django.core.paginator для разбиения постов на страницы.


Реализовано 3 основные страницы (главная, описание, правила). Также ссылки на регистацию и авторизацию. В случае авторизированного клиента - ссылка для написания поста.

После создания любого объекта любые действия с удалением/изменением достпуны только для его создателя, либо для админа (в админ панеле). 

Настроено администрирование проекта, где админ может взаимодействовать с объектами моделей блога и пользователя.

На главной странице настроено отображение списка постов, отсортированных по времени публикации (от новых к старым), настроена пагинация по 10 элементов.

На индивидуальной карточке поста настроены ссылки на следующие страницы:
- страница автора поста (профиль);
- страница категории, к которой принадлежит пост;
- детальная страница поста с подробной информацией;
- в случае неавторизированного клиента - сслыка на страница авторизации для того, чтобы иметь возможность поставить/убрать свой лайк;
- если клиент авторизирован - иконка лайка становится кликабельной и изменяет цвет в зависимоти от того лайкнут пост или нет;
- изображение к посту, если оно есть.
- на детальной странице поста авторизированный пользователь может оставить комментарий
- автор комментария может удалить или отредактировать комментарий

На странице создания поста можно:
- выбрать уровень доступа к нему (опубликован или нет);
- написать заголовок;
- загрузить изображение (опционально);
- написать текст;
- установить дату публикации (можно сделать отложенную публикацию, пост будет опубликован в заданное время без дополнительных манипцляций);
- выбрать местоположение к которой относиться пост (предоставляются на выбор, новые может добавить только админ);
- выбрать категорию к которой относится пост (предоставляются на выбор, новые может добавить только админ).

На странице профиля пользователя отображается подробная информация:
- имя пользователя (можно указать при редактировании профиля, недоступно при регистрации);
- дата регистрации (устанавливается автоматически);
- роль пользователя (права доступа);
- сслыка на редактирование профиля;
- ссылка на изменение пароля;
- список постов, принадлежащих этому пользователю, с пагинацией по 10 элементов (как на главной странице).


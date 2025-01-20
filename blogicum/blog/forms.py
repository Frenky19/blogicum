from django import forms

from .models import Comment, Post, User


class ProfileEditForm(forms.ModelForm):
    """
    Форма редактирования профиля пользователя.

    Она основана на модели 'User' (стандартная модель Django для пользователей)
    и позволяет пользователю редактировать основные поля профиля, такие как:
    - username: Имя пользователя;
    - first_name: Имя;
    - last_name: Фамилия;
    - email: Email-адрес.

    В классе Meta указаны:
    - model: Связанная модель, на основе которой создаётся форма ('User');
    - fields: Поля, которые будут представлены в форме;
    - widgets: Кастомные виджеты для изменения внешнего вида полей:
        - username: Текстовое поле с классом CSS 'form-control';
        - first_name: Текстовое поле с классом CSS 'form-control';
        - last_name: Текстовое поле с классом CSS 'form-control';
        - email: Поле для ввода email-адреса с классом CSS 'form-control'.
    """

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class PostCreateForm(forms.ModelForm):
    """
    Форма для создания и редактирования объекта модели 'Post'.

    Она предоставляет возможность пользователю заполнить поля,
    необходимые для создания публикации, такие как:
    - title: Заголовок публикации;
    - image: Изображение, связанное с публикацией;
    - text: Основной текст публикации;
    - pub_date: Дата и время публикации (поддерживается выбор будущего времени
      для отложенных публикаций);
    - location: Местоположение, связанное с публикацией;
    - category: Категория публикации.

    В классе Meta содержится:
    - model: Связанная модель 'Post';
    - fields: Указаны поля модели, которые будут представлены в форме;
    - widgets: Настроены виджеты для каждого поля, чтобы изменить их внешний
            вид и поведение:
        - title: Обычное текстовое поле с классом CSS 'form-control'
            для стилизации;
        - text: Текстовое поле для ввода многострочного текста ('textarea') с
          классом CSS `form-control` и параметром 'rows=5' для регулировки
            высоты;
        - image: Поле для загрузки изображения с возможностью очистки
            ('ClearableFileInput'),
          стилизованное с использованием класса CSS 'form-control';
        - location: Поле для выбора местоположения на основе выпадающего
            списка ('Select'), с классом CSS 'form-select';
        - pub_date: Поле для выбора даты и времени, настроенное как
          'datetime-local', с классом CSS 'form-control datetimepicker'.
    """

    class Meta:
        model = Post
        exclude = ['created_at', 'author']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'pub_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker',
                'type': 'datetime-local'
            }),
        }


class CommentForm(forms.ModelForm):
    """
    Форма для добавления комментариев.

    Эта форма используется для ввода текста комментария, основанного
    на модели 'Comment' с полем 'text'.

    Поле настройки:
    - text: Текстовое поле для ввода комментария. Оно использует виджет
        'Textarea' для предоставления многострочного текстового ввода и
        дополнительных атрибутов:
        - class: Указан класс CSS 'form-control' для стилизации.
        - rows: Указан атрибут 'rows=4', который регулирует высоту текстового
            поля в строках.
    """

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
        }

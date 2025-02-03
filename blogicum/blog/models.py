from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import Truncator

from abstract.models import PublishedModel
from blog.constants import LIMIT_OF_SYMBOLS


User = get_user_model()


class Category(PublishedModel):
    """
    Модель представляет категорию, использующуюся для группировки объектов.

    Атрибуты:
        - title (CharField): Заголовок категории. Используется для
                            отображения и идентификации категории.
                            Ограничено 256 символами.
        - description (TextField): Полное описание категории.
                                Может содержать более подробную информацию.
        - slug (SlugField): Уникальный идентификатор категории, который
                            используется в URL. Должен быть уникальным и
                            может содержать только буквы латиницы, цифры,
                            дефис и подчёркивание.

    Метаданные:
        - verbose_name (str): Человеко-читаемое имя
                            для единственного объекта - "категория".
        - verbose_name_plural (str): Человеко-читаемое имя
                                для набора объектов - "Категории".

    Методы:
        - __str__: Возвращает строковое представление объекта,
                совпадающее с его заголовком.
    """

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        ),
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return Truncator(self.title).words(LIMIT_OF_SYMBOLS)


class Location(PublishedModel):
    """
    Модель представляет местоположение, используемое в системе.

    Атрибуты:
        - name (CharField): Название места, ограниченное 256 символами.
            Используется для идентификации и отображения местоположений.

    Метаданные:
        - verbose_name (str): Человеко-читаемое имя для
                            единственного объекта - "местоположение".
        - verbose_name_plural (str): Человеко-читаемое имя для
                                    набора объектов - "Местоположения".

    Методы:
        - __str__: Возвращает строковое представление объекта,
                совпадает с его названием места.
    """

    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return Truncator(self.name).words(LIMIT_OF_SYMBOLS)


class Post(PublishedModel):
    """
    Модель представляет публикацию, которая может содержать данные о посте.

    Атрибуты модели:
    - title (CharField): Заголовок публикации, обязательное поле с
        ограничением на длину до 256 символов.
    - image (ImageField): Опциональное поле для добавления изображения.
        Файлы загружаются в папку posts/.
    - text (TextField): Основной текст публикации.
    - pub_date (DateTimeField): Дата и время публикации.
        Если указать значение из будущего, публикация станет "отложенной".
    - author (ForeignKey): Автор публикации. Связывается с моделью User. При
        удалении пользователя удаляются также все его публикации.
    - location (ForeignKey): Опциональное поле для указания местоположения,
        связанное с моделью Location. При удалении местоположения оно
        становится NULL.
    - category (ForeignKey): Категория публикации, связанная с моделью
        Category. Опциональное поле.
      При удалении категории поле становится NULL (on_delete=models.SET_NULL).

    Метаданные (Meta):
    - verbose_name: Читаемое название модели в единственном числе —
        "публикация".
    - verbose_name_plural: Читаемое название модели во множественном числе —
        "Публикации".
    - ordering: По умолчанию публикации сортируются в обратном порядке по дате
        публикации (-pub_date).
    - default_related_name: Имя, используемое при автоматическом создании
        обратной связи между моделями.

    Методы:
    - __str__: Возвращает сокращённый до заданного количества символов
        (LIMIT_OF_SYMBOLS) заголовок публикации.
    """

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    image = models.ImageField(
        upload_to='posts/',
        null=True, blank=True,
        verbose_name="Изображение"
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — можно '
            'делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    likes = models.ManyToManyField(
        User, related_name="liked_posts", blank=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']
        default_related_name = '%(class)ss'

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return Truncator(self.title).words(LIMIT_OF_SYMBOLS)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.pk})


class Comment(PublishedModel):
    """
    Модель комментария к публикации.

    Наследуется от PublishedModel, что добавляет возможности управления
    статусом публикации (например, атрибут is_published).

    Атрибуты:
        text (TextField): Текст комментария, ограниченный 256 символами.
        comment_post (ForeignKey): Связь с моделью Post. Указывает, к какому
        посту принадлежит комментарий.
        author (ForeignKey): Связь с моделью User. Указывает автора
            комментария.

    Метаданные:
        ordering: Указывает стандартный порядок сортировки по дате создания
            (created_at).
        verbose_name: Читаемое название модели в единственном числе.
        verbose_name_plural: Читаемое название модели во множественном числе.

    Методы:
        __str__(): Возвращает строковое представление комментария в виде
            усечённого  текста длиной LIMIT_OF_SYMBOLS слов для краткости
            отображения.
    """

    text = models.TextField(max_length=256, verbose_name='Комментарий',)
    comment_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='comments'
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return Truncator(
            f'Комментарий автора {self.author} к посту {self.comment_post}, '
            f'содержание: {self.text}'
        ).words(LIMIT_OF_SYMBOLS)

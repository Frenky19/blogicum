from django.db import models


class PublishedModel(models.Model):
    """
    Абстрактная модель, применяемая в моделях приложения blog.

    Атрибуты:
        is_published: BooleanField -- Определяет, будет ли объект отображаться
                                на сайте. По умолчанию установлено в `True`.
                                Полезно для временного скрытия записи.
        created_at: DateTimeField -- Дата и время создания объекта.
                            Устанавливается автоматически при создании объекта.
                            Используется для отслеживания создания объектов.

    Метаданные:
        abstract: bool -- Определяет модель как абстрактную, что означает,
                что она сама не будет представлять таблицу в базе данных.
                Используется для наследования другими моделями.
    """

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True

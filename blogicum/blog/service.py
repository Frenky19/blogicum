from django.core.paginator import Paginator
from django.db.models import Count
from django.utils.timezone import now

from .models import Post


def paginate(queryset, request, items_per_page):
    """
    Выполняет пагинацию для переданного QuerySet.

    Распределяет объекты из QuerySet на страницы и возвращает объект текущей
    страницы.

    Параметры:
        - queryset (QuerySet): Набор данных (QuerySet), который нужно разбить
            на страницы.
        - request (HttpRequest, optional): Объект HTTP-запроса, из которого
            извлекается номер страницы.
        - items_per_page (int): Количество объектов, отображаемых на одной
            странице. По умолчанию используется значение POSTS_LIMIT.

    Возвращает:
        - Page: Объект текущей страницы, предоставляемый 'Paginator.get_page()'
    """
    return Paginator(
        queryset, items_per_page).get_page(request.GET.get('page'))


def get_filtered_posts(
        posts=None, apply_filter=True, apply_annotation=True
):
    """
    Получает и обрабатывает список публикаций (QuerySet) с применением
    фильтров и аннотаций.

    Функция обрабатывает переданный QuerySet публикаций, применяя:
    - Фильтр по дате публикации (только публикации с 'pub_date' не позже
      текущего времени), статусу опубликованности публикации
      ('is_published=True'), а также опубликованности категории
      ('category__is_published=True'), если флаг 'apply_filter' установлен в
        'True'.
    - Аннотацию для подсчета количества комментариев к публикации
      ("Count('comments')"), если флаг `apply_annotation` установлен в 'True'.
    Затем добавляются связи для связанных моделей ('select_related') для
    оптимизации запросов.

    Args:
        posts (QuerySet): QuerySet публикаций, который нужно обработать.
            По умолчанию используется 'Post.objects'.
        apply_filter (bool): Флаг, указывающий, нужно ли применять
            вышеописанные фильтры к QuerySet. По умолчанию 'True'.
        apply_annotation (bool): Флаг, указывающий, нужно ли добавлять
            аннотацию, подсчитывающую количество комментариев. По умолчанию
            'True'.

    Returns:
        QuerySet: Обработанный QuerySet публикаций с примененными фильтрами,
                  аннотациями (если указано), связанной выборкой и
                  отсортированный по убыванию даты публикации.
    """
    posts = posts or Post.objects.all()
    time_now = now()
    if apply_filter:
        posts = posts.filter(
            pub_date__lte=time_now,
            is_published=True,
            category__is_published=True)
    if apply_annotation:
        posts = posts.annotate(comment_count=Count('comments'))
    return posts.select_related(
        'category', 'location', 'author'
    ).order_by('-pub_date')

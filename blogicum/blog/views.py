from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from .constants import POSTS_LIMIT
from .forms import CommentForm, PostCreateForm, ProfileEditForm
from .mixins import AuthorRequiredMixin
from .models import Category, Comment, Post, User
from .service import get_filtered_posts, paginate


def profile(request, username):
    """
    Отображает страницу профиля пользователя с его публикациями.

    Функция генерирует страницу профиля для указанного пользователя,
    извлекая связанные публикации. Если текущий пользователь не совпадает
    с профилем запрошенного пользователя или пользователь не аутентифицирован,
    к публикациям применяются стандартные фильтры (например, отображаются
    только опубликованные посты). Результат работы функции передается
    в пагинатор и отображается в шаблоне профиля.

    Args:
        request (HttpRequest): Объект HTTP-запроса.
        username (str): Имя пользователя (username), для которого
                        отобразится профиль.

    Returns:
        HttpResponse: Сгенерированный HTML-ответ с данными профиля
                      и перечнем публикаций, разделенных на страницы.
    """
    user = get_object_or_404(User, username=username)
    post = user.post.all()
    if request.user != user or not request.user.is_authenticated:
        post = get_filtered_posts(posts=user.post.all())
    page_obj = paginate(post, request, POSTS_LIMIT)
    return render(request, 'blog/profile.html', {
        'profile': user,
        'page_obj': page_obj,
    })


@login_required
def edit_profile(request):
    """
    Позволяет аутентифицированным пользователям редактировать свой профиль.

    Эта функция проверяет, что текущий пользователь пытается редактировать
    только свой собственный профиль. Если другой пользователь пытается
    получить доступ к этой странице, он перенаправляется на страницу своего
    профиля. Пользователь может поменять данные своего профиля через форму.
    После успешного изменения данных, пользователь перенаправляется на
    обновлённую страницу профиля.

    Параметры:
        request (HttpRequest): HTTP-запрос, полученный от клиента.
        username (str): Имя пользователя, чей профиль редактируется.

    Возвращает:
        HttpResponse или HttpResponseRedirect:
            - Если пользователь отправил валидную форму, он перенаправляется
                на страницу своего профиля.
            - В случае GET-запроса или ошибки в форме отображается страница с
                формой редактирования профиля.
    """
    form = ProfileEditForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'blog/user.html', {'form': form})


@login_required
def change_password_view(request, username):
    """
    Позволяет аутентифицированным пользователям менять пароль от аккаунта.

    Эта функция проверяет, что текущий пользователь пытается изменить пароль
    только для собственного аккаунта. Если другой пользователь пытается
    получить доступ к функциональности смены пароля, он будет перенаправлен
    на страницу своего профиля. Форма смены пароля предоставляется в случае
    GET-запроса, а в случае успешной обработки POST-запроса пароль
    пользователя будет обновлён, и он будет перенаправлен на страницу
    подтверждения успешной смены пароля.

    Параметры:
        request (HttpRequest): HTTP-запрос, полученный от клиента.
        username (str): Имя пользователя, чей пароль изменяется.

    Возвращает:
        HttpResponse или HttpResponseRedirect:
            - В случае GET-запроса отображается страница с формой смены пароля.
            - Если пользователь отправил валидную форму через POST-запрос,
                выполняется перенаправление на страницу подтверждения успешной
                смены пароля.
            - Если пользователь пытается изменить пароль другого аккаунта, он
                перенаправляется на страницу профиля.
    """
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect('blog:profile', username=user.username)
    form = PasswordChangeForm(user, request.POST or None)
    if form.is_valid():
        user = form.save()
        return redirect(
            'registration:password_change_done',
            username=user.username
        )
    return render(request, 'change_password.html', {'form': form})


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания новых постов блога.

    Это представление выполняет следующие функции:
    1. Пользователь должен быть аутентифицирован (требуется LoginRequiredMixin)
    2. Позволяет пользователю создать новый объект 'Post' с помощью формы
        'PostCreateForm'.
    3. Автоматически связывает создаваемый пост с текущим аутентифицированным
        пользователем.
    4. После успешного создания перенаправляет пользователя на его профиль.

    Атрибуты класса:
    - model: Модель, которую представляет данный класс 'Post'.
    - form_class: Форма, используемая для создания новых объектов.
    - template_name: HTML-шаблон для отображения страницы создания поста.

    Методы:
    - form_valid: Связывает созданный пост с автором, используя текущего
        аутентифицированного пользователя.
    - get_success_url: Определяет URL для перенаправления после успешного
        создания поста.
    """

    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        """
        Вызывается, если предоставленная в форме информация валидна.

        Связывает создаваемый объект Post с текущим аутентифицированным
        пользователем в поле 'author'. После этого вызывает стандартную
        реализацию метода 'form_valid'.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного создания поста.

        Пользователь будет перенаправлен на страницу своего профиля
        (используется имя автора поста в параметре 'username').
        """
        username = self.object.author.username
        return reverse('blog:profile', kwargs={'username': username})


class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """
    Представление для редактирования существующего поста.

    Это представление предназначено для обновления модели 'Post'. Пользователь
    должен быть аутентифицирован, и только автор поста может его редактировать.
    Если текущий пользователь не является автором поста, он будет
    перенаправлен на страницу этого поста.

    Атрибуты класса:
    - model: Определяет модель, с которой работает представление 'Post'.
    - form_class: Форма, которая будет использоваться для обновления объекта
        'Create'.
    - template_name: Шаблон HTML, используемый для отображения страницы
        редактирования поста.

    Методы:
    - get_success_url: Возвращает URL для перенаправления после успешного
        редактирования поста (страница этого поста).
    """

    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create.html'


@login_required
def delete_post(request, post_id):
    """
    Удаление поста.

    Это представление обрабатывает процесс удаления поста. Пользователь должен
    быть аутентифицирован, чтобы иметь доступ к этой функции. Только автор
    поста или пользователь с правами админа (staff) может удалить пост. Если
    текущий пользователь не соответствует этим критериям, он будет
    перенаправлен на страницу этого поста.

    Аргументы:
        request (HttpRequest): HTTP-запрос от клиента.
        pk (int): Первичный ключ поста, который требуется удалить.

    Поведение:
        - Если пользователь не является автором поста и не обладает статусом
            staff, то происходит перенаправление на страницу этого поста.
        - Если запрос отправлен с методом POST, пост удаляется, после чего
            происходит перенаправление на главную страницу блога.
        - Если запрос отправлен с методом GET, возвращается форма для
            подтверждения действия.
    Возвращает:
        HttpResponse: Ответ с отрисованной формой для GET-запроса или
            перенаправление на другую страницу после действий.
    """
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post.pk)
    if request.method == "POST":
        post.delete()
        return redirect('blog:index')
    form = PostCreateForm(instance=post)
    return render(request, 'blog/create.html', {'form': form})


class PostDetailView(DetailView):
    """
    Представление для отображения деталей конкретного объекта модели Post.

    Этот класс-представление (CBV) наследуется от DetailView Django и отвечает
    за отображение подробной информации об определённом посте. Включает логику
    фильтрации, которая зависит от того, аутентифицирован пользователь или нет,
    а также от статуса публикации поста и его связанной категории.

    Атрибуты:
        model (Model): Модель, связанная с этим представлением. В данном
            случае это модель Post.
        template_name (str): Имя шаблона, используемого для отображения
            деталей поста.

    Методы:
        get_queryset():
            Возвращает отфильтрованный QuerySet постов в зависимости от статуса
            аутентификации пользователя. Аутентифицированные пользователи могут
            видеть посты, написанные ими, опубликованные посты, посты в
            опубликованных категориях или посты с прошедшей датой публикации.
            Неаутентифицированные пользователи могут видеть только
            опубликованные посты в опубликованных категориях с прошедшей датой
            публикации.

        get_object():
            Получает конкретный объект Post на основе параметра 'post_id' из
            URL. Если пользователь аутентифицирован, сначала проверяется, есть
            ли пост, связанный с этим пользователем. Если нет, возвращается
            ошибка 404 для постов, которые не опубликованы или не
            соответствуют другим критериям доступности.

        get_context_data(**kwargs):
            Добавляет дополнительные данные в контекст, передаваемый в шаблон.
            Включает форму для добавления комментария (CommentForm) и список
            комментариев, связанных с постом.
    """

    model = Post
    template_name = 'blog/detail.html'

    def get_object(self):
        posts = super().get_queryset()
        post_id = self.kwargs.get('post_id')
        user = self.request.user
        if self.request.user.is_authenticated:
            posts = posts.filter(id=post_id, author=user).first()
            if posts:
                return posts
        return get_object_or_404(
            get_filtered_posts(
                posts, apply_filter=True,
                apply_annotation=False
            ),
            id=post_id
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


@login_required
def add_comment(request, post_id):
    """
    Обработчик для добавления комментария к посту.

    Этот метод позволяет аутентифицированным пользователям добавлять
    комментарии к конкретному посту. Пользователь перенаправляется на страницу
    с формой, где он может ввести текст комментария. После успешной отправки
    формы комментарий сохраняется и привязывается к соответствующему посту и
    автору (текущему пользователю).

    Параметры:
        request (HttpRequest): Стандартный объект запроса Django, содержащий
            данные о запросе пользователя.
        post_id (int): Первичный ключ поста, к которому пользователь хочет
        добавить комментарий.

    Логика:
        Если метод запроса — POST, проверяется корректность отправленной формы:
            1. Если форма валидна:
                - Новый комментарий создаётся, но не сохраняется сразу
                    ('commit=False').
                - Дополнительные поля (comment_post и author) добавляются к
                    объекту комментария.
                - Сохранённый комментарий связывается с выбранным постом и
                    текущим автором (пользователем).
                - Пользователь перенаправляется на детальную страницу поста
                    через 'redirect'.
            2. Если форма не валидна, остаётся текущая форма с ошибками.
        - Если метод запроса — GET, пользователю отображается пустая форма для
            добавления комментария.

    Шаблон:
        Используется шаблон `'blog/comment.html' для отображения страницы с
        формой добавления комментария. Шаблон должен содержать форму 'form'
        для ввода комментария и информацию о посте 'post'.

    Исключительные случаи:
        - Если пост с указанным PK не существует, генерируется ошибка 404 с
            использованием 'get_object_or_404'.
        - Если пользователь не аутентифицирован, метод автоматически
            перенаправит его на страницу входа через декоратор
            '@login_required'.

    Возвращает:
        HttpResponse: Отображает страницу с формой для добавления комментария
        или перенаправляет на детальную страницу поста после успешного
        добавления комментария.
    """
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.comment_post = post
        comment.author = request.user
        comment.save()
        return redirect('blog:post_detail', post_id=post.pk)
    return render(request, 'blog/comment.html', {'form': form, 'post': post})


def edit_comment(request, post_id, comment_id):
    """
    Обработчик для редактирования или удаления комментария.

    Этот метод позволяет автору комментария редактировать или удалять свой
    комментарий, связанный с определённым постом. Попытки редактирования или
    удаления другим пользователем будут игнорироваться, и пользователь будет
    перенаправляться на страницу этого поста.

    Параметры:
        request (HttpRequest): Объект запроса, содержащий данные о текущем
            запросе HTTP.
        post_id (int): Первичный ключ поста, к которому относится комментарий.
        comment_id (int): Первичный ключ комментария, который нужно
            отредактировать или удалить.

    Логика:
        - Пытается найти пост по 'post_id' и комментарий по 'comment_id',
            связанными друг с другом. Если не найдено, возвращается 404.
        - Проверяет, является ли текущий пользователь (request.user) автором
            комментария: Если нет, происходит редирект на страницу поста.
        - Если запрос связан с удалением ('/delete_comment/' в пути):
            - В случае метода POST' комментарий удаляется, и пользователь
                перенаправляется на страницу поста.
            - В случае метода 'GET' возвращается страница подтверждения
                удаления.
        - Если запрос связан с редактированием:
                - Если форма валидна, изменения сохраняются, и пользователь
                    перенаправляется обратно на страницу поста.
            - При методе 'GET' отображается форма с текущим содержимым
                комментария.

    Шаблон:
        Использует шаблон 'blog/comment.html', где отображается либо форма
        редактирования комментария, либо информация для подтверждения удаления.

    Возвращает:
        HttpResponse: Содержит страницу с формой редактирования/удаления
        комментария или редирект на детальную страницу поста.
    """
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, comment_post=post)
    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post.pk)
    if '/delete_comment/' in request.path:
        if request.method == 'POST':
            comment.delete()
            return redirect('blog:post_detail', post_id=post.pk)
        return render(request, 'blog/comment.html', {
            'comment': comment,
        })
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post.pk)
    return render(request, 'blog/comment.html', {
        'form': form,
        'comment': comment,
    })


def category_posts(request, category_slug):
    """
    Отображения списка постов, связанных с заданной категорией.

    Эта функция извлекает категорию на основе предоставленного 'category_slug'
    и проверяет, опубликована ли она. Затем она фильтрует посты, связанные с
    данной категорией, с учетом опубликованных постов, аннотируя их количеством
    комментариев и сортируя по дате публикации в порядке убывания.
    Отфильтрованные данные представляются через пагинацию.

    Аргументы:
        request (HttpRequest): Объект HTTP-запроса Django.
        category_slug (str): Слаг категории, по которому происходит поиск в
            базе данных.

    Логика выполнения:
        1. Получение объекта категории:
            - Используется функция 'get_object_or_404' для получения категории
                из модели 'Category' на основе слага.
            - Проверяется, что категория опубликована ('is_published=True').
                Если категория не найдена или не опубликована, возвращается
                ошибка 404.

        2. Извлечение постов:
            - Вызывается функция 'get_filtered_posts', чтобы получить
                опубликованные посты.
            - Происходит фильтрация по категории.

        3. Пагинация:
            - Посты разбиваются на страницы с фиксированным количеством постов
                (указано в переменной 'POSTS_LIMIT').
            - Объект 'page_obj' формируется через 'Paginator.get_page()'.

        4. Контекст:
            - Создается словарь 'context', содержащий текущую категорию и
                объект пагинации 'page_obj'.

        5. Рендеринг:
            - Шаблон 'blog/category.html' заполняется контекстом и
                возвращается в виде HTTP-ответа.

    Используемые параметры:
        - 'is_published' у модели 'Category' проверяет, опубликована ли
            категория.

    Возвращает:
        HttpResponse: Сформированный HTTP-ответ с отрендеренным шаблоном.

    Исключения:
        - Возвращает 404, если категория с указанным слагом не найдена или не
            опубликована.
    """
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = get_filtered_posts(posts=category.post.all())
    page_obj = paginate(posts, request, POSTS_LIMIT)
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category.html', context)


def index(request):
    """
    Отображение главной страницы.

    Эта функция извлекает все опубликованные посты из базы данных с помощью
    'get_filtered_posts()' и выполняет следующие шаги:
    1. Сортирует посты по дате публикации в порядке убывания ('pub_date').
    2. Добавляет к каждому посту аннотацию 'comment_count', содержащую
        количество комментариев через 'Count('comments')'.
    3. Реализует постраничную навигацию (пагинацию) с помощью 'Paginator', где
        количество постов на странице определяется глобальной переменной
        'POSTS_LIMIT'.
    4. Извлекает номер текущей страницы из параметров GET-запроса ('page'),
        передает объект текущей страницы в контекст шаблона и рендерит
        HTML-страницу.

    Аргументы:
        request (HttpRequest): Объект HTTP-запроса, содержащий информацию о
            запросе, включая параметры GET.

    Переменные:
        posts (QuerySet): Список опубликованных постов с добавленным
            количеством комментариев.
        page_obj (Page): Объект текущей страницы, содержащий посты для
            отображения.

    Шаблон:
        blog/index.html: HTML-шаблон, который используется для отображения
            главной страницы блога.

    Контекст:
        page_obj (Page): Объект текущей страницы, который передается в шаблон.
            Содержит посты для отображения на этой странице и дополнительную
            информацию о пагинации.

    Возвращает:
        HttpResponse: Рендерит и возвращает главную страницу блога с постами и
            пагинацией.
    """
    posts = get_filtered_posts()
    page_obj = paginate(posts, request, POSTS_LIMIT)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)

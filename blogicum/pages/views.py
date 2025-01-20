from django.shortcuts import render


def page_not_found(request, exception):
    """
    Обрабатывает ошибку 404 (Page Not Found).

    Эта функция вызывается автоматически, если пользователь пытается обратиться
    по несуществующему URL. Она возвращает HTML-страницу, созданную для
    обработки ошибки 404.

    Args:
        request: Объект HTTP-запроса.
        exception: Исключение, описывающее причину ошибки.

    Returns:
        HttpResponse: Сгенерированный HTML с кодом состояния 404.
    """
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """
    Обрабатывает ошибку 403, связанную с отказом проверки CSRF-токена.

    Эта функция вызывается, если CSRF-токен отсутствует, поврежден или не
    совпадает с ожидаемым значением. В ответ возвращается кастомизированная
    страница с кодом состояния 403 и сообщением об ошибке.

    Args:
        request: Объект HTTP-запроса.
        reason (str, optional): Сообщение, описывающее причину ошибки.

    Returns:
        HttpResponse: Сгенерированный HTML с кодом состояния 403.
    """
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """
    Обрабатывает ошибку 500 (Internal Server Error).

    Эта функция вызывается автоматически, если на сервере происходит
    внутренняя ошибка, в результате которой сервер не может обработать запрос.
    Она возвращает кастомизированную HTML-страницу для ошибки 500.

    Args:
        request: Объект HTTP-запроса.

    Returns:
        HttpResponse: Сгенерированный HTML с кодом состояния 500.
    """
    return render(request, 'pages/500.html', status=500)

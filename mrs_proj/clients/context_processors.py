def add_query_params_to_context(request):
    """
    Добавляет текущие параметры запроса в контекст шаблона.
    """
    # Получаем текущие параметры запроса GET
    query_params = request.GET.copy()

    # Удаляем параметр страницы, чтобы он не мешал при формировании ссылок
    if 'page' in query_params:
        del query_params['page']

    return {'query_params': query_params.urlencode()}

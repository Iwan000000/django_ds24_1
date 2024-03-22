from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Количество элементов на странице
    page_size_query_param = 'page_size'  # Параметр для установки количества элементов на странице через запрос
    max_page_size = 100  # Максимальное количество элементов на странице

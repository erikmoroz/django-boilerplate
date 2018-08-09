from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
    max_page_size = settings.REST_FRAMEWORK['MAX_PAGE_SIZE']
    page_query_param = 'page'
    page_size_query_param = 'page_size'


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    max_page_size = 10000
    page_query_param = 'page'
    page_size_query_param = 'page_size'

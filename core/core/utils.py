from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Кастомный обработчик исключений для API.
    """
    # Сначала вызываем стандартный обработчик исключений
    response = exception_handler(exc, context)
    
    # Если стандартный обработчик не вернул ответ, обрабатываем исключение самостоятельно
    if response is None:
        logger.error(f"Необработанное исключение: {exc}")
        return Response(
            {"error": "Произошла внутренняя ошибка сервера."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Добавляем дополнительную информацию к ответу
    if isinstance(response.data, dict):
        # Если ответ - словарь, добавляем статус и код
        response.data['status'] = 'error'
        response.data['code'] = response.status_code
    
    return response 
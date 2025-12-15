"""
Custom exception handlers for Email API
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for REST framework
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Log the exception
    logger.error(f"Exception occurred: {str(exc)}", exc_info=True)
    
    # If response is None, it's an unhandled exception
    if response is None:
        return Response(
            {
                'success': False,
                'message': 'An internal server error occurred',
                'detail': str(exc)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Customize the response format
    if isinstance(response.data, dict):
        response.data = {
            'success': False,
            'message': 'Request failed',
            'errors': response.data
        }
    
    return response




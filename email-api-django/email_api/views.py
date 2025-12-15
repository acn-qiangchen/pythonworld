"""
API Views for Email Service
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
import logging

from .serializers import (
    EmailSerializer,
    EmailResponseSerializer,
    HealthCheckSerializer,
    ServiceInfoSerializer
)
from .email_service import get_email_service, EmailSendError

logger = logging.getLogger(__name__)


class ServiceInfoView(APIView):
    """
    API root endpoint - Service information
    """
    def get(self, request):
        """Get service information"""
        data = {
            'service': 'Email API',
            'version': '1.0.0',
            'status': 'running',
            'framework': 'Django REST Framework'
        }
        serializer = ServiceInfoSerializer(data)
        return Response(serializer.data)


class HealthCheckView(APIView):
    """
    Health check endpoint
    """
    def get(self, request):
        """Check service health and AWS SES connectivity"""
        try:
            email_service = get_email_service()
            is_healthy = email_service.check_health()
            
            if is_healthy:
                # Get statistics if available
                statistics = email_service.get_send_statistics()
                
                data = {
                    'status': 'healthy',
                    'service': 'email-api',
                    'ses_connection': 'ok',
                    'statistics': statistics if statistics else {}
                }
                serializer = HealthCheckSerializer(data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data = {
                    'status': 'unhealthy',
                    'service': 'email-api',
                    'ses_connection': 'failed'
                }
                serializer = HealthCheckSerializer(data)
                return Response(serializer.data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return Response(
                {
                    'status': 'unhealthy',
                    'service': 'email-api',
                    'ses_connection': 'error',
                    'error': str(e)
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class SendEmailView(APIView):
    """
    Send email endpoint
    """
    def post(self, request):
        """
        Send an email via AWS SES
        
        Request body:
        {
            "to_email": "recipient@example.com",
            "subject": "Email subject",
            "body": "Email body content",
            "from_email": "sender@example.com",  // optional
            "body_html": "<html>...</html>"      // optional
        }
        """
        # Validate request data
        serializer = EmailSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'message': 'Validation error',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get validated data
            validated_data = serializer.validated_data
            to_email = validated_data['to_email']
            subject = validated_data['subject']
            body = validated_data['body']
            from_email = validated_data.get('from_email')
            body_html = validated_data.get('body_html')
            
            logger.info(f"Received email request to: {to_email}")
            
            # Send email using AWS SES
            email_service = get_email_service()
            message_id = email_service.send_email(
                to_email=to_email,
                subject=subject,
                body=body,
                from_email=from_email,
                body_html=body_html
            )
            
            logger.info(f"Email sent successfully. Message ID: {message_id}")
            
            response_data = {
                'success': True,
                'message': 'Email sent successfully',
                'message_id': message_id
            }
            response_serializer = EmailResponseSerializer(response_data)
            
            return Response(response_serializer.data, status=status.HTTP_200_OK)
            
        except EmailSendError as e:
            logger.error(f"Failed to send email: {str(e)}")
            return Response(
                {
                    'success': False,
                    'message': f'Failed to send email: {str(e)}',
                    'message_id': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response(
                {
                    'success': False,
                    'message': f'An unexpected error occurred: {str(e)}',
                    'message_id': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




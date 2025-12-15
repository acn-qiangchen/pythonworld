"""
Tests for Email API
"""
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, MagicMock


class ServiceInfoViewTest(APITestCase):
    """Test service info endpoint"""
    
    def test_service_info(self):
        """Test GET /api/"""
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['service'], 'Email API')
        self.assertEqual(response.data['framework'], 'Django REST Framework')


class HealthCheckViewTest(APITestCase):
    """Test health check endpoint"""
    
    @patch('email_api.views.get_email_service')
    def test_health_check_healthy(self, mock_get_service):
        """Test health check when service is healthy"""
        mock_service = MagicMock()
        mock_service.check_health.return_value = True
        mock_service.get_send_statistics.return_value = {}
        mock_get_service.return_value = mock_service
        
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')
    
    @patch('email_api.views.get_email_service')
    def test_health_check_unhealthy(self, mock_get_service):
        """Test health check when service is unhealthy"""
        mock_service = MagicMock()
        mock_service.check_health.return_value = False
        mock_get_service.return_value = mock_service
        
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data['status'], 'unhealthy')


class SendEmailViewTest(APITestCase):
    """Test send email endpoint"""
    
    @patch('email_api.views.get_email_service')
    def test_send_email_success(self, mock_get_service):
        """Test successful email sending"""
        mock_service = MagicMock()
        mock_service.send_email.return_value = 'test-message-id-123'
        mock_get_service.return_value = mock_service
        
        data = {
            'to_email': 'recipient@example.com',
            'subject': 'Test Subject',
            'body': 'Test body content',
            'from_email': 'sender@example.com'
        }
        
        response = self.client.post('/api/v1/send-email/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message_id'], 'test-message-id-123')
    
    def test_send_email_validation_error(self):
        """Test email sending with invalid data"""
        data = {
            'to_email': 'invalid-email',  # Invalid email format
            'subject': 'Test Subject',
            'body': 'Test body'
        }
        
        response = self.client.post('/api/v1/send-email/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
    
    def test_send_email_missing_fields(self):
        """Test email sending with missing required fields"""
        data = {
            'to_email': 'recipient@example.com'
            # Missing subject and body
        }
        
        response = self.client.post('/api/v1/send-email/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])




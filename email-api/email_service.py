"""
Email Service Module
Handles email sending via AWS SES
"""
import boto3
from botocore.exceptions import ClientError, BotoCoreError
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


class EmailSendError(Exception):
    """Custom exception for email sending errors"""
    pass


class EmailService:
    """Service class for sending emails via AWS SES"""
    
    def __init__(self):
        """Initialize AWS SES client"""
        try:
            # Get AWS configuration from environment variables
            aws_region = os.getenv('AWS_REGION', 'us-east-1')
            
            # Initialize SES client
            # AWS credentials can be provided via:
            # 1. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
            # 2. AWS credentials file (~/.aws/credentials)
            # 3. IAM role (when running on EC2/ECS)
            self.ses_client = boto3.client('ses', region_name=aws_region)
            
            # Get default sender email from environment
            self.default_sender = os.getenv('DEFAULT_SENDER_EMAIL')
            
            if not self.default_sender:
                logger.warning("DEFAULT_SENDER_EMAIL not set. Sender email must be provided in requests.")
            
            logger.info(f"Email service initialized with AWS region: {aws_region}")
            
        except Exception as e:
            logger.error(f"Failed to initialize AWS SES client: {str(e)}")
            raise EmailSendError(f"Failed to initialize email service: {str(e)}")
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        from_email: Optional[str] = None,
        body_html: Optional[str] = None
    ) -> str:
        """
        Send an email via AWS SES
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body (plain text)
            from_email: Sender email address (must be verified in SES)
            body_html: Optional HTML version of email body
            
        Returns:
            Message ID from AWS SES
            
        Raises:
            EmailSendError: If email sending fails
        """
        try:
            # Use provided sender or default
            sender = from_email or self.default_sender
            
            if not sender:
                raise EmailSendError("No sender email address provided and DEFAULT_SENDER_EMAIL not configured")
            
            # Prepare email body
            body_data = {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': body,
                }
            }
            
            # Add HTML body if provided
            if body_html:
                body_data['Html'] = {
                    'Charset': 'UTF-8',
                    'Data': body_html,
                }
            
            # Send email
            logger.info(f"Sending email from {sender} to {to_email}")
            
            response = self.ses_client.send_email(
                Source=sender,
                Destination={
                    'ToAddresses': [to_email],
                },
                Message={
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': subject,
                    },
                    'Body': body_data,
                }
            )
            
            message_id = response['MessageId']
            logger.info(f"Email sent successfully. MessageId: {message_id}")
            
            return message_id
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            logger.error(f"AWS SES ClientError: {error_code} - {error_message}")
            
            # Provide user-friendly error messages
            if error_code == 'MessageRejected':
                raise EmailSendError(f"Email rejected by SES: {error_message}")
            elif error_code == 'MailFromDomainNotVerifiedException':
                raise EmailSendError(f"Sender email domain not verified in SES: {sender}")
            elif error_code == 'ConfigurationSetDoesNotExistException':
                raise EmailSendError("SES configuration set does not exist")
            else:
                raise EmailSendError(f"AWS SES error: {error_message}")
                
        except BotoCoreError as e:
            logger.error(f"BotoCoreError: {str(e)}")
            raise EmailSendError(f"AWS connection error: {str(e)}")
            
        except Exception as e:
            logger.error(f"Unexpected error sending email: {str(e)}")
            raise EmailSendError(f"Unexpected error: {str(e)}")
    
    def check_health(self) -> bool:
        """
        Check if AWS SES service is accessible
        
        Returns:
            True if service is healthy, False otherwise
        """
        try:
            # Try to get account sending quota as a health check
            response = self.ses_client.get_send_quota()
            logger.info(f"SES Health Check - Max24HourSend: {response.get('Max24HourSend', 'N/A')}")
            return True
        except Exception as e:
            logger.error(f"SES health check failed: {str(e)}")
            return False
    
    def get_send_statistics(self) -> dict:
        """
        Get AWS SES sending statistics
        
        Returns:
            Dictionary with sending statistics
        """
        try:
            quota = self.ses_client.get_send_quota()
            return {
                'max_24_hour_send': quota.get('Max24HourSend'),
                'max_send_rate': quota.get('MaxSendRate'),
                'sent_last_24_hours': quota.get('SentLast24Hours')
            }
        except Exception as e:
            logger.error(f"Failed to get send statistics: {str(e)}")
            return {}


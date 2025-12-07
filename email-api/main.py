"""
Email API Service
A RESTful API service that sends emails using AWS SES
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uvicorn
import logging
from email_service import EmailService, EmailSendError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Email API Service",
    description="A RESTful API for sending emails via AWS SES",
    version="1.0.0"
)

# Initialize email service
email_service = EmailService()


class EmailRequest(BaseModel):
    """Email request model"""
    to_email: EmailStr = Field(..., description="Recipient email address")
    subject: str = Field(..., min_length=1, max_length=200, description="Email subject")
    body: str = Field(..., min_length=1, description="Email body content")
    from_email: Optional[EmailStr] = Field(None, description="Sender email address (must be verified in SES)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "to_email": "recipient@example.com",
                "subject": "Hello from Email API",
                "body": "This is a test email sent via AWS SES",
                "from_email": "sender@example.com"
            }
        }


class EmailResponse(BaseModel):
    """Email response model"""
    success: bool
    message: str
    message_id: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "service": "Email API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Verify AWS SES connection
        is_healthy = email_service.check_health()
        if is_healthy:
            return {
                "status": "healthy",
                "service": "email-api",
                "ses_connection": "ok"
            }
        else:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "status": "unhealthy",
                    "service": "email-api",
                    "ses_connection": "failed"
                }
            )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "service": "email-api",
                "error": str(e)
            }
        )


@app.post("/api/v1/send-email", response_model=EmailResponse, status_code=status.HTTP_200_OK)
async def send_email(email_request: EmailRequest):
    """
    Send an email via AWS SES
    
    Args:
        email_request: Email details including recipient, subject, and body
        
    Returns:
        EmailResponse with success status and message ID
        
    Raises:
        HTTPException: If email sending fails
    """
    try:
        logger.info(f"Received email request to: {email_request.to_email}")
        
        # Send email using AWS SES
        message_id = email_service.send_email(
            to_email=email_request.to_email,
            subject=email_request.subject,
            body=email_request.body,
            from_email=email_request.from_email
        )
        
        logger.info(f"Email sent successfully. Message ID: {message_id}")
        
        return EmailResponse(
            success=True,
            message="Email sent successfully",
            message_id=message_id
        )
        
    except EmailSendError as e:
        logger.error(f"Failed to send email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send email: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )


# Email API Service

A RESTful API service built with Python FastAPI that sends emails using AWS Simple Email Service (SES). This application is containerized and ready to deploy.

## Features

- ✅ RESTful API with FastAPI
- ✅ Email sending via AWS SES
- ✅ Docker containerization
- ✅ Health check endpoint
- ✅ Request validation with Pydantic
- ✅ Comprehensive error handling
- ✅ Structured logging
- ✅ Non-root container user for security

## Prerequisites

1. **AWS Account** with SES access
2. **Verified email address** in AWS SES (required for sending emails)
3. **AWS credentials** (Access Key ID and Secret Access Key)
4. **Docker** (for containerized deployment)

## AWS SES Setup

Before using this application, you need to set up AWS SES:

1. **Verify your sender email address:**
   - Go to AWS SES Console
   - Navigate to "Verified identities"
   - Click "Create identity"
   - Verify your email address or domain

2. **Move out of SES Sandbox (Optional but recommended):**
   - By default, SES is in sandbox mode (can only send to verified addresses)
   - Request production access to send to any email address
   - Go to SES Console → Account dashboard → Request production access

3. **Create IAM credentials:**
   - Create an IAM user with `AmazonSESFullAccess` policy
   - Generate Access Key ID and Secret Access Key

## Installation & Setup

### Option 1: Run with Docker (Recommended)

1. **Clone or create the project:**
```bash
cd email-api
```

2. **Create environment file:**
```bash
cp .env.example .env
```

3. **Edit `.env` file with your AWS credentials:**
```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
DEFAULT_SENDER_EMAIL=verified-sender@yourdomain.com
```

4. **Build Docker image:**
```bash
docker build -t email-api:latest .
```

5. **Run the container:**
```bash
docker run -d \
  --name email-api \
  -p 8000:8000 \
  --env-file .env \
  email-api:latest
```

### Option 2: Run Locally (Development)

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set environment variables:**
```bash
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=your_access_key_here
export AWS_SECRET_ACCESS_KEY=your_secret_key_here
export DEFAULT_SENDER_EMAIL=verified-sender@yourdomain.com
```

4. **Run the application:**
```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### 1. Health Check
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "email-api",
  "ses_connection": "ok"
}
```

### 2. Root Endpoint
```bash
GET /
```

**Response:**
```json
{
  "service": "Email API",
  "status": "running",
  "version": "1.0.0"
}
```

### 3. Send Email
```bash
POST /api/v1/send-email
```

**Request Body:**
```json
{
  "to_email": "recipient@example.com",
  "subject": "Hello from Email API",
  "body": "This is a test email sent via AWS SES",
  "from_email": "sender@example.com"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Email sent successfully",
  "message_id": "010001234567890a-12345678-1234-1234-1234-123456789abc-000000"
}
```

**Response (Error):**
```json
{
  "detail": "Failed to send email: Sender email domain not verified in SES"
}
```

## Usage Examples

### Using cURL

```bash
# Send an email
curl -X POST "http://localhost:8000/api/v1/send-email" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "recipient@example.com",
    "subject": "Test Email",
    "body": "This is a test email from the Email API service",
    "from_email": "verified-sender@yourdomain.com"
  }'
```

### Using Python requests

```python
import requests

url = "http://localhost:8000/api/v1/send-email"
payload = {
    "to_email": "recipient@example.com",
    "subject": "Test Email",
    "body": "This is a test email from the Email API service",
    "from_email": "verified-sender@yourdomain.com"
}

response = requests.post(url, json=payload)
print(response.json())
```

### Using httpie

```bash
http POST localhost:8000/api/v1/send-email \
  to_email=recipient@example.com \
  subject="Test Email" \
  body="This is a test email" \
  from_email=verified-sender@yourdomain.com
```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Docker Commands

```bash
# Build image
docker build -t email-api:latest .

# Run container
docker run -d --name email-api -p 8000:8000 --env-file .env email-api:latest

# View logs
docker logs email-api

# Follow logs
docker logs -f email-api

# Stop container
docker stop email-api

# Remove container
docker rm email-api

# Run with custom port
docker run -d --name email-api -p 9000:8000 --env-file .env email-api:latest
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `AWS_REGION` | AWS region for SES | Yes | us-east-1 |
| `AWS_ACCESS_KEY_ID` | AWS access key | Yes | - |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Yes | - |
| `DEFAULT_SENDER_EMAIL` | Default sender email | No | - |
| `LOG_LEVEL` | Logging level | No | INFO |

## Security Considerations

1. **Never commit `.env` file** - Contains sensitive credentials
2. **Use IAM roles** when running on AWS (EC2/ECS) instead of access keys
3. **Restrict IAM permissions** - Only grant necessary SES permissions
4. **Use HTTPS** in production with reverse proxy (nginx/traefik)
5. **Rate limiting** - Consider adding rate limiting for production
6. **Container runs as non-root user** for security

## Troubleshooting

### Email not sending

1. **Check if sender email is verified in SES**
   - Go to SES Console → Verified identities
   
2. **Check if account is in sandbox mode**
   - Sandbox mode only allows sending to verified addresses
   
3. **Check AWS credentials**
   - Ensure credentials have SES permissions

4. **Check logs**
   ```bash
   docker logs email-api
   ```

### Connection errors

1. **Check AWS region**
   - Ensure region matches where your SES is configured

2. **Check network connectivity**
   - Container needs internet access to reach AWS APIs

## Production Deployment

For production deployment, consider:

1. **Use environment-specific configurations**
2. **Set up monitoring and alerting**
3. **Implement rate limiting**
4. **Use a reverse proxy (nginx/traefik)**
5. **Enable HTTPS/TLS**
6. **Use AWS IAM roles instead of access keys**
7. **Set up log aggregation**
8. **Configure auto-scaling**

## License

MIT License

## Support

For issues and questions, please refer to:
- [AWS SES Documentation](https://docs.aws.amazon.com/ses/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)


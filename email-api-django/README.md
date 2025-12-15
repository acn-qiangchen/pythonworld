# Django Email API Service

A RESTful API service built with **Django** and **Django REST Framework** that sends emails using AWS Simple Email Service (SES). This application is containerized and ready to deploy.

## Features

- ✅ RESTful API with Django REST Framework
- ✅ Email sending via AWS SES
- ✅ Docker containerization
- ✅ Health check endpoint
- ✅ Request validation with DRF serializers
- ✅ Comprehensive error handling
- ✅ Structured logging
- ✅ Browsable API interface
- ✅ Unit tests included
- ✅ Non-root container user for security

## Prerequisites

1. **AWS Account** with SES access
2. **Verified email address** in AWS SES (required for sending emails)
3. **AWS credentials** (Access Key ID and Secret Access Key)
4. **Docker** (for containerized deployment)

## Project Structure

```
email-api-django/
├── email_project/          # Django project settings
│   ├── __init__.py
│   ├── settings.py        # Project configuration
│   ├── urls.py            # Main URL routing
│   ├── wsgi.py            # WSGI application
│   └── asgi.py            # ASGI application
├── email_api/             # Django app for email functionality
│   ├── __init__.py
│   ├── apps.py            # App configuration
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # App URL routing
│   ├── email_service.py   # AWS SES service
│   ├── exceptions.py      # Custom exception handlers
│   ├── models.py          # Models (none for this app)
│   ├── admin.py           # Admin configuration
│   └── tests.py           # Unit tests
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Docker Compose configuration
├── .env.example         # Environment variables template
├── Makefile             # Common commands shortcuts
└── README.md            # This file
```

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

1. **Clone or navigate to the project:**
```bash
cd email-api-django
```

2. **Create environment file:**
```bash
cp .env.example .env
```

3. **Edit `.env` file with your AWS credentials:**
```bash
# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
DEFAULT_SENDER_EMAIL=verified-sender@yourdomain.com
```

4. **Build and run with Docker Compose:**
```bash
docker-compose up -d
```

Or use the Makefile:
```bash
make build
make run
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
export DJANGO_SECRET_KEY=your-secret-key
```

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Run the development server:**
```bash
python manage.py runserver 0.0.0.0:8000
```

Or use the Makefile:
```bash
make install
make migrate
make dev
```

## API Endpoints

### 1. Service Information
```bash
GET /api/
```

**Response:**
```json
{
  "service": "Email API",
  "version": "1.0.0",
  "status": "running",
  "framework": "Django REST Framework"
}
```

### 2. Health Check
```bash
GET /api/health/
```

**Response:**
```json
{
  "status": "healthy",
  "service": "email-api",
  "ses_connection": "ok",
  "statistics": {
    "max_24_hour_send": 200,
    "max_send_rate": 1,
    "sent_last_24_hours": 5
  }
}
```

### 3. Send Email
```bash
POST /api/v1/send-email/
```

**Request Body:**
```json
{
  "to_email": "recipient@example.com",
  "subject": "Hello from Django Email API",
  "body": "This is a test email sent via AWS SES",
  "from_email": "sender@example.com",
  "body_html": "<html><body><h1>Hello!</h1></body></html>"
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
  "success": false,
  "message": "Failed to send email: Sender email domain not verified in SES",
  "message_id": null
}
```

## Usage Examples

### Using cURL

```bash
# Health check
curl http://localhost:8000/api/health/

# Send an email
curl -X POST "http://localhost:8000/api/v1/send-email/" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "recipient@example.com",
    "subject": "Test Email",
    "body": "This is a test email from the Django Email API service",
    "from_email": "verified-sender@yourdomain.com"
  }'
```

### Using Python requests

```python
import requests

url = "http://localhost:8000/api/v1/send-email/"
payload = {
    "to_email": "recipient@example.com",
    "subject": "Test Email",
    "body": "This is a test email from the Django Email API service",
    "from_email": "verified-sender@yourdomain.com"
}

response = requests.post(url, json=payload)
print(response.json())
```

### Using httpie

```bash
http POST localhost:8000/api/v1/send-email/ \
  to_email=recipient@example.com \
  subject="Test Email" \
  body="This is a test email" \
  from_email=verified-sender@yourdomain.com
```

## Browsable API

Django REST Framework provides a browsable API interface. Simply open your browser and navigate to:

- **API Root:** http://localhost:8000/api/
- **Send Email:** http://localhost:8000/api/v1/send-email/
- **Health Check:** http://localhost:8000/api/health/

You can test the API directly from the browser interface!

## Running Tests

```bash
# Run all tests
python manage.py test

# Run with verbose output
python manage.py test --verbosity=2

# Run specific test
python manage.py test email_api.tests.SendEmailViewTest

# Using Makefile
make test
```

## Docker Commands

```bash
# Build image
docker build -t email-api-django:latest .

# Run container
docker run -d --name email-api-django -p 8000:8000 --env-file .env email-api-django:latest

# View logs
docker logs email-api-django

# Follow logs
docker logs -f email-api-django

# Stop container
docker stop email-api-django

# Remove container
docker rm email-api-django

# Using docker-compose
docker-compose up -d      # Start
docker-compose down       # Stop
docker-compose logs -f    # View logs
docker-compose restart    # Restart

# Using Makefile
make build    # Build image
make run      # Start service
make stop     # Stop service
make logs     # View logs
make clean    # Clean up
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | Yes | - |
| `DEBUG` | Debug mode | No | False |
| `ALLOWED_HOSTS` | Allowed hosts | No | localhost,127.0.0.1 |
| `AWS_REGION` | AWS region for SES | Yes | us-east-1 |
| `AWS_ACCESS_KEY_ID` | AWS access key | Yes | - |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Yes | - |
| `DEFAULT_SENDER_EMAIL` | Default sender email | No | - |
| `LOG_LEVEL` | Logging level | No | INFO |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins | No | - |

## Django Admin

This project includes Django admin interface. To use it:

1. **Create a superuser:**
```bash
python manage.py createsuperuser
```

2. **Access admin panel:**
```
http://localhost:8000/admin/
```

## Security Considerations

1. **Never commit `.env` file** - Contains sensitive credentials
2. **Change DJANGO_SECRET_KEY** in production
3. **Set DEBUG=False** in production
4. **Use IAM roles** when running on AWS (EC2/ECS) instead of access keys
5. **Restrict IAM permissions** - Only grant necessary SES permissions
6. **Use HTTPS** in production with reverse proxy (nginx/traefik)
7. **Configure ALLOWED_HOSTS** properly in production
8. **Enable CSRF protection** (enabled by default)
9. **Container runs as non-root user** for security

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
   docker logs email-api-django
   # or
   python manage.py runserver  # See console output
   ```

### Connection errors

1. **Check AWS region**
   - Ensure region matches where your SES is configured

2. **Check network connectivity**
   - Container needs internet access to reach AWS APIs

### Django errors

1. **Run migrations**
   ```bash
   python manage.py migrate
   ```

2. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

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
9. **Use PostgreSQL/MySQL instead of SQLite**
10. **Set up CI/CD pipeline**

## Comparison with FastAPI Version

This Django version provides:

- ✅ **Django ORM** - If you need database models later
- ✅ **Django Admin** - Built-in admin interface
- ✅ **Browsable API** - DRF's interactive API interface
- ✅ **Mature ecosystem** - Extensive Django packages
- ✅ **Authentication** - Built-in auth system
- ✅ **More structure** - Django's opinionated structure

The FastAPI version is:
- ⚡ **Faster** - Better performance
- 📝 **Auto docs** - Automatic OpenAPI/Swagger docs
- 🔄 **Async** - Native async/await support
- 🪶 **Lighter** - Smaller footprint

Choose based on your needs and team preferences!

## License

MIT License

## Support

For issues and questions, please refer to:
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [AWS SES Documentation](https://docs.aws.amazon.com/ses/)
- [Docker Documentation](https://docs.docker.com/)




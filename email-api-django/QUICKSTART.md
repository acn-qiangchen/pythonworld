# Quick Start Guide - Django Email API

This guide will help you get the Django Email API up and running in 5 minutes.

## Prerequisites

- Docker installed on your system
- AWS account with SES access
- At least one verified email address in AWS SES

## Step 1: Verify Email in AWS SES

1. Log in to [AWS Console](https://console.aws.amazon.com/)
2. Navigate to **Simple Email Service (SES)**
3. Click **Verified identities** → **Create identity**
4. Choose **Email address** and enter your email
5. Check your inbox and click the verification link

## Step 2: Get AWS Credentials

You can use the IAM user you created earlier (`SysSESAdmin`):

```bash
# If you haven't created it yet, run:
aws iam create-user --user-name SysSESAdmin
aws iam attach-user-policy \
  --user-name SysSESAdmin \
  --policy-arn arn:aws:iam::aws:policy/AmazonSESFullAccess
aws iam create-access-key --user-name SysSESAdmin
```

Save the `AccessKeyId` and `SecretAccessKey` from the output.

## Step 3: Configure Environment

Create a `.env` file in the `email-api-django` directory:

```bash
cd email-api-django
cat > .env << 'EOF'
# Django Configuration
DJANGO_SECRET_KEY=django-insecure-change-this-in-production-$(openssl rand -base64 32)
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_HERE
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY_HERE

# Email Configuration
DEFAULT_SENDER_EMAIL=your-verified-email@example.com

# Application Configuration
LOG_LEVEL=INFO
EOF
```

**Replace:**
- `YOUR_ACCESS_KEY_HERE` with your AWS Access Key ID
- `YOUR_SECRET_KEY_HERE` with your AWS Secret Access Key
- `your-verified-email@example.com` with your verified SES email

## Step 4: Build and Run

### Option A: Using Makefile (Easiest)

```bash
make build
make run
```

### Option B: Using Docker Compose

```bash
docker-compose up -d
```

### Option C: Using Docker directly

```bash
# Build the image
docker build -t email-api-django:latest .

# Run the container
docker run -d \
  --name email-api-django \
  -p 8000:8000 \
  --env-file .env \
  email-api-django:latest
```

## Step 5: Test the API

### Check if it's running:

```bash
curl http://localhost:8000/api/health/
```

Expected response:
```json
{
  "status": "healthy",
  "service": "email-api",
  "ses_connection": "ok",
  "statistics": {...}
}
```

### Send a test email:

```bash
curl -X POST "http://localhost:8000/api/v1/send-email/" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "recipient@example.com",
    "subject": "Test Email from Django",
    "body": "Hello! This is a test email from Django Email API.",
    "from_email": "your-verified-email@example.com"
  }'
```

**Important Notes:**
- Replace `your-verified-email@example.com` with your verified SES email
- If in **SES Sandbox mode**, `recipient@example.com` must also be verified
- To send to any email, request **production access** in SES Console

## Step 6: Explore the Browsable API

Django REST Framework provides an interactive web interface!

Open your browser and visit:
- **API Root:** http://localhost:8000/api/
- **Send Email (with form):** http://localhost:8000/api/v1/send-email/
- **Health Check:** http://localhost:8000/api/health/

You can test the API directly from the browser using the built-in forms!

## Useful Commands

```bash
# View logs
docker logs email-api-django
# or
make logs

# Follow logs in real-time
docker logs -f email-api-django

# Stop the service
docker-compose down
# or
make stop

# Restart the service
docker-compose restart

# Run tests
make test

# Remove everything
make clean
```

## Troubleshooting

### "Email rejected" or "Not verified"
- Make sure your sender email is verified in AWS SES
- Check AWS SES Console → Verified identities

### "Connection error" or "Credentials invalid"
- Verify your AWS credentials in `.env` file
- Check IAM user has SES permissions

### "Cannot send to recipient"
- If in SES sandbox mode, recipient must be verified
- Request production access in SES Console

### Container won't start
```bash
# Check logs
docker logs email-api-django

# Verify environment variables
docker exec email-api-django env | grep AWS
```

### Django-specific issues
```bash
# Run migrations (if needed)
docker exec email-api-django python manage.py migrate

# Check Django logs
docker logs email-api-django
```

## Development Mode

To run locally for development:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export DEFAULT_SENDER_EMAIL=your-email@example.com
export DJANGO_SECRET_KEY=your-secret-key

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver 0.0.0.0:8000

# Or use Makefile
make install
make migrate
make dev
```

## Django Admin (Optional)

To access the Django admin interface:

```bash
# Create superuser
docker exec -it email-api-django python manage.py createsuperuser

# Access admin at:
# http://localhost:8000/admin/
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Request SES production access to send to any email
- Set up monitoring and logging
- Add authentication/authorization for production use
- Configure rate limiting
- Explore Django REST Framework features

## Differences from FastAPI Version

This Django version includes:
- ✅ **Browsable API** - Interactive web interface
- ✅ **Django Admin** - Built-in admin panel
- ✅ **Django ORM** - If you need database models
- ✅ **More structure** - Django's opinionated architecture

Both versions have the same core functionality for sending emails via AWS SES!

## Support

For more information:
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [AWS SES Documentation](https://docs.aws.amazon.com/ses/)
- [Docker Documentation](https://docs.docker.com/)




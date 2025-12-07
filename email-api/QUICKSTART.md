# Quick Start Guide

This guide will help you get the Email API up and running in 5 minutes.

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

1. Go to **IAM** in AWS Console
2. Create a new user or use existing one
3. Attach policy: `AmazonSESFullAccess`
4. Create **Access Key** and save:
   - Access Key ID
   - Secret Access Key

## Step 3: Configure Environment

Create a `.env` file in the `email-api` directory:

```bash
cd email-api
cat > .env << 'EOF'
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_HERE
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY_HERE
DEFAULT_SENDER_EMAIL=your-verified-email@example.com
LOG_LEVEL=INFO
EOF
```

**Replace:**
- `YOUR_ACCESS_KEY_HERE` with your AWS Access Key ID
- `YOUR_SECRET_KEY_HERE` with your AWS Secret Access Key
- `your-verified-email@example.com` with your verified SES email

## Step 4: Build and Run

### Option A: Using Docker Compose (Easiest)

```bash
docker-compose up -d
```

### Option B: Using Docker directly

```bash
# Build the image
docker build -t email-api:latest .

# Run the container
docker run -d \
  --name email-api \
  -p 8000:8000 \
  --env-file .env \
  email-api:latest
```

## Step 5: Test the API

### Check if it's running:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "email-api",
  "ses_connection": "ok"
}
```

### Send a test email:

```bash
curl -X POST "http://localhost:8000/api/v1/send-email" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "recipient@example.com",
    "subject": "Test Email",
    "body": "Hello! This is a test email from Email API.",
    "from_email": "your-verified-email@example.com"
  }'
```

**Important Notes:**
- Replace `your-verified-email@example.com` with your verified SES email
- If in **SES Sandbox mode**, `recipient@example.com` must also be verified
- To send to any email, request **production access** in SES Console

## Step 6: View Interactive Docs

Open your browser and visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

You can test the API directly from the Swagger UI!

## Useful Commands

```bash
# View logs
docker logs email-api

# Follow logs in real-time
docker logs -f email-api

# Stop the service
docker-compose down
# OR
docker stop email-api

# Restart the service
docker-compose restart
# OR
docker restart email-api

# Remove everything
docker-compose down
docker rmi email-api:latest
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
docker logs email-api

# Verify environment variables
docker exec email-api env | grep AWS
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Request SES production access to send to any email
- Set up monitoring and logging
- Add authentication/authorization for production use
- Configure rate limiting

## Support

For more information:
- [AWS SES Documentation](https://docs.aws.amazon.com/ses/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)


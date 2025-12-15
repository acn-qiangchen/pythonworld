# Complete Integration Guide

## 🎯 Overview

This guide shows you how to set up the complete Email API system with AWS SES using Terraform.

## 📦 What You Have

You now have **three** complete components:

1. **FastAPI Email API** (`email-api/`)
2. **Django Email API** (`email-api-django/`)
3. **Terraform SES Configuration** (`terraform-ses/`)

## 🚀 Complete Setup (Start to Finish)

### Phase 1: Deploy AWS SES Infrastructure

#### Step 1: Configure Terraform

```bash
cd terraform-ses

# Create configuration
cat > terraform.tfvars << 'EOF'
aws_region   = "us-east-1"
environment  = "prod"
sender_email = "noreply@yourdomain.com"

# Monitoring
enable_cloudwatch_events = true
enable_cloudwatch_alarms = true
enable_sns_notifications = true
notification_email = "admin@yourdomain.com"

# IAM
iam_user_name = "SysSESAdmin"

# Security: Restrict sender emails
allowed_sender_emails = [
  "noreply@yourdomain.com",
  "support@yourdomain.com"
]
EOF
```

#### Step 2: Deploy Infrastructure

```bash
# Initialize Terraform
terraform init

# Preview changes
terraform plan

# Deploy (type 'yes')
terraform apply

# Save credentials
terraform output -raw aws_access_key_id > ../AWS_KEY_ID.txt
terraform output -raw aws_secret_access_key > ../AWS_SECRET_KEY.txt
terraform output -raw ses_email_identity > ../SENDER_EMAIL.txt
```

#### Step 3: Verify Email

1. Check inbox for verification email
2. Click verification link
3. Confirm verification:

```bash
aws ses get-identity-verification-attributes \
  --identities noreply@yourdomain.com \
  --region us-east-1
```

#### Step 4: Request Production Access

1. Go to [AWS SES Console](https://console.aws.amazon.com/ses/)
2. Click "Account dashboard" → "Request production access"
3. Fill out form:
   - **Mail Type:** Transactional
   - **Website URL:** Your app URL
   - **Use Case:** Transactional email API
   - **Process:** Monitor via CloudWatch/SNS
4. Submit and wait for approval

### Phase 2: Deploy Email API

Choose **Django** or **FastAPI** (or both!):

#### Option A: Django Version

```bash
cd ../email-api-django

# Create .env file
cat > .env << EOF
# Django
DJANGO_SECRET_KEY=$(openssl rand -base64 32)
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# AWS (from Terraform)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=$(cat ../AWS_KEY_ID.txt)
AWS_SECRET_ACCESS_KEY=$(cat ../AWS_SECRET_KEY.txt)
DEFAULT_SENDER_EMAIL=$(cat ../SENDER_EMAIL.txt)

# Logging
LOG_LEVEL=INFO
EOF

# Build and run
docker-compose up -d

# Check health
curl http://localhost:8000/api/health/
```

#### Option B: FastAPI Version

```bash
cd ../email-api

# Create .env file
cat > .env << EOF
# AWS (from Terraform)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=$(cat ../AWS_KEY_ID.txt)
AWS_SECRET_ACCESS_KEY=$(cat ../AWS_SECRET_KEY.txt)
DEFAULT_SENDER_EMAIL=$(cat ../SENDER_EMAIL.txt)

# Logging
LOG_LEVEL=INFO
EOF

# Build and run
docker-compose up -d

# Check health
curl http://localhost:8000/health
```

### Phase 3: Test the Complete System

#### Test 1: Health Check

```bash
# Django
curl http://localhost:8000/api/health/

# FastAPI
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "email-api",
  "ses_connection": "ok",
  "statistics": {
    "max_24_hour_send": 200,
    "sent_last_24_hours": 0
  }
}
```

#### Test 2: Send Test Email

**While in Sandbox Mode** (send to verified email only):

```bash
# First, verify your test recipient
aws ses verify-email-identity \
  --email-address your-test@example.com \
  --region us-east-1

# Wait for verification email and click link

# Then send test email
curl -X POST "http://localhost:8000/api/v1/send-email/" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "your-test@example.com",
    "subject": "Test Email from Production Setup",
    "body": "This email was sent using Terraform-provisioned AWS SES!",
    "from_email": "noreply@yourdomain.com"
  }'
```

**After Production Access Approved** (send to any email):

```bash
curl -X POST "http://localhost:8000/api/v1/send-email/" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "anyone@example.com",
    "subject": "Production Email",
    "body": "Now we can send to any email address!",
    "from_email": "noreply@yourdomain.com"
  }'
```

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Your Application                         │
│  ┌────────────────┐              ┌────────────────┐         │
│  │   FastAPI      │     OR       │    Django      │         │
│  │   Email API    │              │   Email API    │         │
│  └────────┬───────┘              └────────┬───────┘         │
│           │                               │                  │
│           └───────────────┬───────────────┘                  │
│                           │                                  │
│                    Docker Container                          │
└───────────────────────────┼──────────────────────────────────┘
                            │
                            │ boto3 SDK
                            │ (IAM Credentials)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      AWS Cloud                               │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  AWS SES (Simple Email Service)                      │  │
│  │  - Email Identity: noreply@yourdomain.com           │  │
│  │  - Configuration Set: email-api-prod                │  │
│  │  - Production Access: Approved                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                            │                                 │
│           ┌────────────────┼────────────────┐               │
│           │                │                │               │
│           ▼                ▼                ▼               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │  CloudWatch  │ │  SNS Topic   │ │  IAM User    │       │
│  │  Alarms      │ │  (Bounces)   │ │  SysSESAdmin │       │
│  └──────────────┘ └──────────────┘ └──────────────┘       │
│                                                              │
│  All provisioned by Terraform                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ SMTP
                            ▼
                    ┌───────────────┐
                    │  Recipients   │
                    │  (Any Email)  │
                    └───────────────┘
```

## 🔄 Workflow

### Development Workflow

```bash
# 1. Make changes to Terraform
cd terraform-ses
nano terraform.tfvars
terraform plan
terraform apply

# 2. Update application with new credentials
cd ../email-api-django
# Update .env with new credentials
docker-compose restart

# 3. Test changes
curl http://localhost:8000/api/health/
```

### Production Deployment Workflow

```bash
# 1. Deploy infrastructure
cd terraform-ses
terraform apply

# 2. Build application image
cd ../email-api-django
docker build -t email-api:v1.0.0 .

# 3. Push to registry
docker tag email-api:v1.0.0 your-registry/email-api:v1.0.0
docker push your-registry/email-api:v1.0.0

# 4. Deploy to production
# (Use your deployment method: ECS, K8s, etc.)
```

## 🔐 Security Best Practices

### 1. Credentials Management

**Development:**
```bash
# Store in .env file (gitignored)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

**Production:**
```bash
# Use AWS Secrets Manager
aws secretsmanager create-secret \
  --name email-api/ses-credentials \
  --secret-string '{
    "AWS_ACCESS_KEY_ID":"...",
    "AWS_SECRET_ACCESS_KEY":"..."
  }'

# Or use IAM roles (recommended)
# Attach SES policy to EC2/ECS task role
```

### 2. Network Security

```bash
# Use security groups to restrict access
# Only allow HTTPS traffic
# Use VPC for private communication
```

### 3. Monitoring

```bash
# Set up CloudWatch dashboards
# Configure SNS alerts
# Monitor bounce/complaint rates
# Set up log aggregation
```

## 📈 Scaling Considerations

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  email-api:
    image: email-api:latest
    deploy:
      replicas: 3
    ports:
      - "8000-8002:8000"
```

### Load Balancing

```bash
# Use nginx or AWS ALB
upstream email_api {
    server localhost:8000;
    server localhost:8001;
    server localhost:8002;
}
```

### Rate Limiting

```python
# Add rate limiting to prevent abuse
from fastapi_limiter import FastAPILimiter

@app.post("/api/v1/send-email")
@limiter.limit("100/minute")
async def send_email(...):
    ...
```

## 🧪 Testing Strategy

### 1. Infrastructure Tests

```bash
# Test Terraform configuration
cd terraform-ses
terraform validate
terraform plan

# Test AWS connectivity
aws ses get-send-quota --region us-east-1
```

### 2. Application Tests

```bash
# Django tests
cd email-api-django
python manage.py test

# FastAPI tests
cd email-api
pytest
```

### 3. Integration Tests

```bash
# End-to-end test
./test-integration.sh
```

## 📊 Monitoring Dashboard

### Key Metrics to Monitor

1. **Email Sending**
   - Emails sent per hour
   - Success rate
   - Error rate

2. **SES Health**
   - Bounce rate (< 5%)
   - Complaint rate (< 0.1%)
   - Send quota usage

3. **Application Health**
   - API response time
   - Error rate
   - Container health

4. **Infrastructure**
   - CPU usage
   - Memory usage
   - Network traffic

### CloudWatch Dashboard

```bash
# Create custom dashboard
aws cloudwatch put-dashboard \
  --dashboard-name EmailAPI \
  --dashboard-body file://dashboard.json
```

## 🆘 Troubleshooting Guide

### Issue: Email not sending

**Check:**
```bash
# 1. Verify email identity
aws ses get-identity-verification-attributes \
  --identities noreply@yourdomain.com

# 2. Check sandbox status
aws ses get-account-sending-enabled

# 3. Check application logs
docker logs email-api-django

# 4. Check SES sending quota
aws ses get-send-quota
```

### Issue: High bounce rate

**Actions:**
```bash
# 1. Review bounce notifications
# 2. Validate email addresses before sending
# 3. Remove invalid addresses from list
# 4. Check email content for spam triggers
```

### Issue: Terraform errors

**Solutions:**
```bash
# 1. Re-initialize
terraform init -upgrade

# 2. Check AWS credentials
aws sts get-caller-identity

# 3. Review state
terraform show

# 4. Import existing resources
terraform import aws_ses_email_identity.sender noreply@yourdomain.com
```

## 📚 Additional Resources

- [Terraform Documentation](terraform-ses/README.md)
- [Django API Documentation](email-api-django/README.md)
- [FastAPI Documentation](email-api/README.md)
- [AWS SES Best Practices](https://docs.aws.amazon.com/ses/latest/dg/best-practices.html)

## ✅ Production Checklist

Before going live:

- [ ] Terraform infrastructure deployed
- [ ] Email identity verified
- [ ] Production access approved
- [ ] DNS records configured (if using domain)
- [ ] Application deployed and tested
- [ ] Monitoring configured
- [ ] Alerts set up
- [ ] Credentials secured
- [ ] Bounce/complaint handling process defined
- [ ] Documentation updated
- [ ] Team trained
- [ ] Backup plan ready

## 🎉 You're Done!

You now have a complete, production-ready email API system with:

✅ Infrastructure as Code (Terraform)
✅ Production-grade AWS SES setup
✅ Two API options (Django & FastAPI)
✅ Monitoring and alerting
✅ Security best practices
✅ Complete documentation

**Happy emailing!** 📧




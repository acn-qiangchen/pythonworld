# Terraform SES - Quick Start Guide

Get AWS SES configured for production in **5 minutes**!

## 📋 Prerequisites

- AWS Account
- Terraform installed (`brew install terraform` on Mac)
- AWS CLI configured (`aws configure`)
- Email address you control

## 🚀 Quick Setup

### Step 1: Configure

```bash
cd terraform-ses

# Create your configuration file
cat > terraform.tfvars << 'EOF'
aws_region   = "us-east-1"
environment  = "prod"
sender_email = "noreply@yourdomain.com"

# Optional: Get notifications
notification_email = "admin@yourdomain.com"

# Optional: Verify entire domain
# domain_name = "yourdomain.com"
# route53_zone_id = "Z1234567890ABC"
EOF
```

**Replace:**
- `noreply@yourdomain.com` with your sender email
- `admin@yourdomain.com` with your admin email

### Step 2: Deploy

```bash
# Initialize Terraform
terraform init

# Preview changes
terraform plan

# Deploy (type 'yes' when prompted)
terraform apply
```

### Step 3: Get Credentials

```bash
# View all outputs
terraform output

# Copy these for your application
echo "AWS_ACCESS_KEY_ID=$(terraform output -raw aws_access_key_id)"
echo "AWS_SECRET_ACCESS_KEY=$(terraform output -raw aws_secret_access_key)"
echo "DEFAULT_SENDER_EMAIL=$(terraform output -raw ses_email_identity)"
```

### Step 4: Verify Email

1. Check your inbox (the sender_email you configured)
2. Look for email from AWS with subject "Amazon SES Email Address Verification Request"
3. Click the verification link
4. Done! ✅

### Step 5: Request Production Access

**Important:** By default, you can only send to verified emails.

To send to **any email address**:

1. Go to [AWS SES Console](https://console.aws.amazon.com/ses/)
2. Click **"Account dashboard"**
3. Click **"Request production access"**
4. Fill out the form:
   ```
   Mail Type: Transactional
   Website URL: https://yourapp.com
   Use Case: Email API for sending transactional emails
   Bounce/Complaint Process: We monitor via CloudWatch and SNS
   ```
5. Submit and wait (usually 24-48 hours)

### Step 6: Update Your Application

```bash
# Navigate to your email API
cd ../email-api-django  # or email-api

# Update .env file
cat > .env << EOF
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=$(cd ../terraform-ses && terraform output -raw aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(cd ../terraform-ses && terraform output -raw aws_secret_access_key)
DEFAULT_SENDER_EMAIL=$(cd ../terraform-ses && terraform output -raw ses_email_identity)
DJANGO_SECRET_KEY=your-django-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
EOF

# Start your application
docker-compose up -d
```

### Step 7: Test!

```bash
# Test the API
curl -X POST "http://localhost:8000/api/v1/send-email/" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "your-verified-email@example.com",
    "subject": "Test from Terraform SES",
    "body": "It works! 🎉",
    "from_email": "noreply@yourdomain.com"
  }'
```

## 🎯 What Was Created?

| Resource | Description |
|----------|-------------|
| **IAM User** | `SysSESAdmin` with SES permissions |
| **Access Keys** | Credentials for your application |
| **Email Identity** | Verified sender email |
| **Configuration Set** | For tracking and monitoring |
| **CloudWatch Alarms** | High bounce/complaint alerts |
| **SNS Topic** | Bounce/complaint notifications |

## 📊 View Your Setup

```bash
# See all resources
terraform show

# See specific outputs
terraform output aws_access_key_id
terraform output ses_email_identity
terraform output next_steps

# See sensitive values
terraform output -raw aws_secret_access_key
```

## 🔍 Check Status

```bash
# Check email verification status
aws ses get-identity-verification-attributes \
  --identities noreply@yourdomain.com \
  --region us-east-1

# Check sending quota
aws ses get-send-quota --region us-east-1

# Check if in sandbox mode
aws ses get-account-sending-enabled --region us-east-1
```

## 🌐 Optional: Domain Verification

If you want to verify an entire domain:

```bash
# Update terraform.tfvars
cat >> terraform.tfvars << 'EOF'

# Domain verification
domain_name = "yourdomain.com"

# If using Route53 (optional)
route53_zone_id = "Z1234567890ABC"
EOF

# Apply changes
terraform apply

# Get DNS records to add
terraform output ses_domain_verification_token
terraform output ses_dkim_tokens
```

Then add these records to your DNS:

1. **TXT Record:**
   - Name: `_amazonses.yourdomain.com`
   - Value: `<verification_token>`

2. **CNAME Records** (3 records):
   - Name: `<token>._domainkey.yourdomain.com`
   - Value: `<token>.dkim.amazonses.com`

## 🎁 Bonus Features

### Enable All Monitoring

```bash
# Update terraform.tfvars
cat >> terraform.tfvars << 'EOF'

# Monitoring
enable_cloudwatch_events = true
enable_cloudwatch_alarms = true
enable_sns_notifications = true
notification_email = "admin@yourdomain.com"
EOF

terraform apply
```

### Restrict Sender Emails

```bash
# Update terraform.tfvars
cat >> terraform.tfvars << 'EOF'

# Only allow specific sender emails
allowed_sender_emails = [
  "noreply@yourdomain.com",
  "support@yourdomain.com",
  "alerts@yourdomain.com"
]
EOF

terraform apply
```

## 🔒 Security Tips

1. **Never commit `terraform.tfvars`** - It's in `.gitignore`
2. **Store credentials securely** - Use a password manager
3. **Rotate keys regularly** - Create new access keys periodically
4. **Use IAM roles in production** - On EC2/ECS, use roles instead of keys

## 🧹 Cleanup

To remove everything:

```bash
terraform destroy
```

## 🆘 Troubleshooting

### Email not verified?
```bash
# Resend verification email
aws ses verify-email-identity \
  --email-address noreply@yourdomain.com \
  --region us-east-1
```

### Can't send to external emails?
- You're in sandbox mode
- Request production access (Step 5 above)

### Terraform errors?
```bash
# Re-initialize
terraform init -upgrade

# Check AWS credentials
aws sts get-caller-identity
```

## 📚 Next Steps

1. ✅ Verify your email
2. ✅ Request production access
3. ✅ Update your application with credentials
4. ✅ Test email sending
5. ✅ Monitor bounce/complaint rates
6. ✅ Set up DNS (if using domain)
7. ✅ Review CloudWatch metrics

## 📖 Full Documentation

See [README.md](README.md) for complete documentation.

---

**You're all set!** 🎉 Your AWS SES is now configured for production use.




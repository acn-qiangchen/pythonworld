# AWS SES Terraform Configuration

This Terraform configuration sets up AWS Simple Email Service (SES) for **production use** with your Email API application.

## 🎯 What This Creates

### Core Resources
- ✅ **SES Email Identity** - Verified email address for sending
- ✅ **SES Domain Identity** - Optional domain verification
- ✅ **SES Configuration Set** - For tracking and monitoring
- ✅ **IAM User** - Dedicated user with SES permissions
- ✅ **IAM Policy** - Least-privilege access policy
- ✅ **Access Keys** - Credentials for your application

### Monitoring (Optional)
- ✅ **CloudWatch Alarms** - High bounce/complaint rate alerts
- ✅ **SNS Topic** - Notifications for bounces and complaints
- ✅ **Event Tracking** - Send, bounce, complaint, delivery events

### DNS (Optional)
- ✅ **Route53 Records** - Automatic DNS record creation
- ✅ **DKIM Records** - Improve email deliverability
- ✅ **Domain Verification** - Verify entire domain

## 📋 Prerequisites

1. **AWS Account** with appropriate permissions
2. **Terraform** installed (v1.0+)
3. **AWS CLI** configured with credentials
4. **Email address** or domain you control

## 🚀 Quick Start

### Step 1: Configure AWS Credentials

```bash
# Option 1: Use AWS CLI
aws configure

# Option 2: Set environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

### Step 2: Create Configuration File

```bash
cd terraform-ses

# Copy example configuration
cp terraform.tfvars.example terraform.tfvars

# Edit with your values
nano terraform.tfvars
```

**Minimum required configuration:**

```hcl
# terraform.tfvars
aws_region   = "us-east-1"
environment  = "prod"
sender_email = "noreply@yourdomain.com"

# Optional: Notification email
notification_email = "admin@yourdomain.com"
```

### Step 3: Initialize Terraform

```bash
terraform init
```

### Step 4: Review the Plan

```bash
terraform plan
```

This will show you all resources that will be created.

### Step 5: Apply Configuration

```bash
terraform apply
```

Type `yes` when prompted to create the resources.

### Step 6: Get Your Credentials

```bash
# View all outputs
terraform output

# Get access key ID
terraform output aws_access_key_id

# Get secret access key (sensitive)
terraform output -raw aws_secret_access_key

# Get all environment variables
terraform output -json env_variables
```

### Step 7: Verify Email Address

1. Check your inbox for the verification email from AWS
2. Click the verification link
3. Email identity is now verified!

### Step 8: Request Production Access

**Important:** By default, SES is in sandbox mode. To send to any email address:

1. Go to [AWS SES Console](https://console.aws.amazon.com/ses/)
2. Click **"Account dashboard"**
3. Click **"Request production access"**
4. Fill out the form:
   - **Mail type:** Transactional
   - **Website URL:** Your application URL
   - **Use case description:** Explain your email API use case
   - **Bounce/complaint handling:** Describe your process
5. Submit and wait for approval (usually 24-48 hours)

## 📝 Configuration Options

### Basic Configuration

```hcl
# terraform.tfvars

# AWS Region
aws_region = "us-east-1"

# Environment
environment = "prod"

# Email to verify
sender_email = "noreply@yourdomain.com"

# IAM user name
iam_user_name = "SysSESAdmin"
```

### Domain Verification (Optional)

To verify an entire domain instead of individual emails:

```hcl
# Domain to verify
domain_name = "yourdomain.com"

# If using Route53, provide zone ID for automatic DNS records
route53_zone_id = "Z1234567890ABC"

# Allowed sender emails from this domain
allowed_sender_emails = [
  "noreply@yourdomain.com",
  "support@yourdomain.com",
  "alerts@yourdomain.com"
]
```

### Monitoring Configuration

```hcl
# Enable CloudWatch event tracking
enable_cloudwatch_events = true

# Enable CloudWatch alarms
enable_cloudwatch_alarms = true

# Enable SNS notifications
enable_sns_notifications = true

# Email for notifications
notification_email = "admin@yourdomain.com"
```

## 🔐 Security Best Practices

### 1. Restrict Sender Emails

The IAM policy restricts which email addresses can be used:

```hcl
allowed_sender_emails = [
  "noreply@yourdomain.com",
  "support@yourdomain.com"
]
```

### 2. Store Credentials Securely

**Never commit credentials to git!**

```bash
# Get credentials
terraform output -raw aws_secret_access_key > .secret

# Store in password manager or secrets management system
# AWS Secrets Manager, HashiCorp Vault, etc.
```

### 3. Use IAM Roles in Production

For production deployments on AWS (EC2, ECS, Lambda):

```hcl
# Instead of access keys, use IAM roles
# Attach the SES policy to your EC2/ECS task role
```

### 4. Enable MFA for IAM User

```bash
# Enable MFA for the IAM user
aws iam enable-mfa-device \
  --user-name SysSESAdmin \
  --serial-number arn:aws:iam::ACCOUNT:mfa/SysSESAdmin \
  --authentication-code1 123456 \
  --authentication-code2 789012
```

## 📊 Monitoring and Alerts

### CloudWatch Alarms

Two alarms are created by default:

1. **High Bounce Rate** - Triggers if bounce rate > 5%
2. **High Complaint Rate** - Triggers if complaint rate > 0.1%

### SNS Notifications

Receive email notifications for:
- Bounces
- Complaints
- Delivery issues

### Viewing Metrics

```bash
# View SES sending statistics
aws ses get-send-statistics --region us-east-1

# View send quota
aws ses get-send-quota --region us-east-1
```

## 🌐 DNS Configuration

### If Using Domain Verification

After applying Terraform, you need to add DNS records:

```bash
# Get verification token
terraform output ses_domain_verification_token

# Get DKIM tokens
terraform output ses_dkim_tokens
```

**Manual DNS Configuration:**

1. **Verification TXT Record:**
   - Name: `_amazonses.yourdomain.com`
   - Type: `TXT`
   - Value: `<verification_token>`

2. **DKIM CNAME Records** (3 records):
   - Name: `<token1>._domainkey.yourdomain.com`
   - Type: `CNAME`
   - Value: `<token1>.dkim.amazonses.com`
   - (Repeat for all 3 tokens)

**Automatic DNS (Route53):**

If you provided `route53_zone_id`, DNS records are created automatically!

## 🔄 Updating Configuration

To update your configuration:

```bash
# Edit variables
nano terraform.tfvars

# Preview changes
terraform plan

# Apply changes
terraform apply
```

## 🧪 Testing Your Setup

### 1. Test Email Sending (Sandbox Mode)

While in sandbox mode, you can only send to verified addresses:

```bash
# Verify a test recipient email
aws ses verify-email-identity \
  --email-address test@example.com \
  --region us-east-1

# Send test email
aws ses send-email \
  --from noreply@yourdomain.com \
  --to test@example.com \
  --subject "Test Email" \
  --text "This is a test" \
  --region us-east-1
```

### 2. Test with Your Application

Update your application's `.env` file:

```bash
# Get credentials from Terraform
terraform output -raw aws_access_key_id
terraform output -raw aws_secret_access_key

# Update .env file
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=<from_terraform_output>
AWS_SECRET_ACCESS_KEY=<from_terraform_output>
DEFAULT_SENDER_EMAIL=noreply@yourdomain.com
```

Then test your Email API:

```bash
cd ../email-api-django  # or email-api for FastAPI

# Start the application
docker-compose up -d

# Send test email
curl -X POST "http://localhost:8000/api/v1/send-email/" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "verified-recipient@example.com",
    "subject": "Test from Email API",
    "body": "Testing SES integration!",
    "from_email": "noreply@yourdomain.com"
  }'
```

## 📈 Production Checklist

Before going to production:

- [ ] Email identity verified
- [ ] Production access approved by AWS
- [ ] DNS records configured (if using domain)
- [ ] DKIM enabled for better deliverability
- [ ] CloudWatch alarms configured
- [ ] SNS notifications set up
- [ ] Bounce/complaint handling process defined
- [ ] Credentials stored securely
- [ ] IAM policy reviewed and restricted
- [ ] Monitoring dashboard created
- [ ] Tested email sending
- [ ] Documented runbook for issues

## 🔍 Troubleshooting

### Email Not Verified

```bash
# Check verification status
aws ses get-identity-verification-attributes \
  --identities noreply@yourdomain.com \
  --region us-east-1

# Resend verification email
aws ses verify-email-identity \
  --email-address noreply@yourdomain.com \
  --region us-east-1
```

### Still in Sandbox Mode

- Check AWS SES Console for production access status
- Review your production access request
- Contact AWS Support if delayed

### High Bounce Rate

- Review recipient email addresses
- Check for typos in email addresses
- Implement email validation
- Remove invalid addresses from your list

### DNS Records Not Working

```bash
# Check DNS propagation
dig TXT _amazonses.yourdomain.com
dig CNAME token._domainkey.yourdomain.com

# Wait for DNS propagation (can take up to 48 hours)
```

## 🧹 Cleanup

To destroy all resources:

```bash
# Preview what will be destroyed
terraform plan -destroy

# Destroy all resources
terraform destroy
```

**Warning:** This will delete:
- IAM user and access keys
- SES identities
- Configuration sets
- All monitoring resources

## 📚 Additional Resources

- [AWS SES Documentation](https://docs.aws.amazon.com/ses/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [SES Best Practices](https://docs.aws.amazon.com/ses/latest/dg/best-practices.html)
- [Email Deliverability Guide](https://docs.aws.amazon.com/ses/latest/dg/send-email-concepts-deliverability.html)

## 🆘 Support

For issues:
1. Check AWS SES Console for status
2. Review CloudWatch logs
3. Check SNS notifications
4. Review Terraform state: `terraform show`
5. Contact AWS Support for SES-specific issues

## 📄 License

MIT License




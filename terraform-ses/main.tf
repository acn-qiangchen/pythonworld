/**
 * AWS SES Terraform Configuration
 * 
 * This Terraform configuration sets up AWS SES for production use:
 * - Email identity verification
 * - IAM user with SES permissions
 * - SES configuration set for tracking
 * - Production access (requires manual approval from AWS)
 */

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure AWS Provider
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "EmailAPI"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# Data source for current AWS account
data "aws_caller_identity" "current" {}

# Data source for AWS region
data "aws_region" "current" {}

#############################################
# SES Email Identity Verification
#############################################

# Verify email address for sending
resource "aws_ses_email_identity" "sender" {
  email = var.sender_email
}

# Optional: Verify domain instead of individual email
resource "aws_ses_domain_identity" "domain" {
  count  = var.domain_name != "" ? 1 : 0
  domain = var.domain_name
}

# Domain verification record (add this to your DNS)
resource "aws_route53_record" "ses_verification" {
  count   = var.domain_name != "" && var.route53_zone_id != "" ? 1 : 0
  zone_id = var.route53_zone_id
  name    = "_amazonses.${var.domain_name}"
  type    = "TXT"
  ttl     = 600
  records = [aws_ses_domain_identity.domain[0].verification_token]
}

# DKIM records for domain (improves deliverability)
resource "aws_ses_domain_dkim" "domain" {
  count  = var.domain_name != "" ? 1 : 0
  domain = aws_ses_domain_identity.domain[0].domain
}

resource "aws_route53_record" "dkim" {
  count   = var.domain_name != "" && var.route53_zone_id != "" ? 3 : 0
  zone_id = var.route53_zone_id
  name    = "${aws_ses_domain_dkim.domain[0].dkim_tokens[count.index]}._domainkey.${var.domain_name}"
  type    = "CNAME"
  ttl     = 600
  records = ["${aws_ses_domain_dkim.domain[0].dkim_tokens[count.index]}.dkim.amazonses.com"]
}

#############################################
# SES Configuration Set (for tracking)
#############################################

resource "aws_ses_configuration_set" "main" {
  name = "${var.project_name}-${var.environment}"

  delivery_options {
    tls_policy = "Require"
  }

  reputation_metrics_enabled = true
}

# Event destination for bounce/complaint tracking (optional)
resource "aws_ses_event_destination" "cloudwatch" {
  count                  = var.enable_cloudwatch_events ? 1 : 0
  name                   = "cloudwatch-destination"
  configuration_set_name = aws_ses_configuration_set.main.name
  enabled                = true
  matching_types         = ["send", "reject", "bounce", "complaint", "delivery"]

  cloudwatch_destination {
    default_value  = "default"
    dimension_name = "ses:configuration-set"
    value_source   = "messageTag"
  }
}

#############################################
# IAM User for SES Access
#############################################

# Create IAM user for application
resource "aws_iam_user" "ses_user" {
  name = var.iam_user_name
  path = "/applications/"

  tags = {
    Description = "IAM user for Email API application"
  }
}

# Create access key for the user
resource "aws_iam_access_key" "ses_user" {
  user = aws_iam_user.ses_user.name
}

# IAM Policy for SES access
resource "aws_iam_policy" "ses_sending" {
  name        = "${var.project_name}-ses-sending-policy"
  description = "Policy for sending emails via SES"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail",
          "ses:SendTemplatedEmail",
          "ses:SendBulkTemplatedEmail"
        ]
        Resource = "*"
        Condition = {
          StringEquals = {
            "ses:FromAddress" = var.allowed_sender_emails
          }
        }
      },
      {
        Effect = "Allow"
        Action = [
          "ses:GetSendQuota",
          "ses:GetSendStatistics",
          "ses:GetAccount"
        ]
        Resource = "*"
      }
    ]
  })
}

# Attach policy to user
resource "aws_iam_user_policy_attachment" "ses_user" {
  user       = aws_iam_user.ses_user.name
  policy_arn = aws_iam_policy.ses_sending.policy_arn
}

#############################################
# SES Sending Limits (Informational)
#############################################

# Note: By default, AWS SES starts in sandbox mode with limits:
# - Can only send to verified email addresses
# - Limited to 200 emails per 24 hours
# - Maximum send rate of 1 email per second
#
# To move to production:
# 1. Request production access via AWS Console or CLI
# 2. AWS will review your request (usually 24-48 hours)
# 3. Once approved, you can send to any email address

#############################################
# CloudWatch Alarms (optional)
#############################################

resource "aws_cloudwatch_metric_alarm" "bounce_rate" {
  count               = var.enable_cloudwatch_alarms ? 1 : 0
  alarm_name          = "${var.project_name}-${var.environment}-high-bounce-rate"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "Reputation.BounceRate"
  namespace           = "AWS/SES"
  period              = "300"
  statistic           = "Average"
  threshold           = "0.05" # 5% bounce rate
  alarm_description   = "This metric monitors SES bounce rate"
  treat_missing_data  = "notBreaching"

  dimensions = {
    ConfigurationSet = aws_ses_configuration_set.main.name
  }
}

resource "aws_cloudwatch_metric_alarm" "complaint_rate" {
  count               = var.enable_cloudwatch_alarms ? 1 : 0
  alarm_name          = "${var.project_name}-${var.environment}-high-complaint-rate"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "Reputation.ComplaintRate"
  namespace           = "AWS/SES"
  period              = "300"
  statistic           = "Average"
  threshold           = "0.001" # 0.1% complaint rate
  alarm_description   = "This metric monitors SES complaint rate"
  treat_missing_data  = "notBreaching"

  dimensions = {
    ConfigurationSet = aws_ses_configuration_set.main.name
  }
}

#############################################
# SNS Topic for Bounce/Complaint Notifications
#############################################

resource "aws_sns_topic" "ses_notifications" {
  count = var.enable_sns_notifications ? 1 : 0
  name  = "${var.project_name}-${var.environment}-ses-notifications"
}

resource "aws_sns_topic_subscription" "ses_notifications_email" {
  count     = var.enable_sns_notifications && var.notification_email != "" ? 1 : 0
  topic_arn = aws_sns_topic.ses_notifications[0].arn
  protocol  = "email"
  endpoint  = var.notification_email
}

# SES Identity Notification Topic
resource "aws_ses_identity_notification_topic" "bounce" {
  count                    = var.enable_sns_notifications ? 1 : 0
  topic_arn                = aws_sns_topic.ses_notifications[0].arn
  notification_type        = "Bounce"
  identity                 = aws_ses_email_identity.sender.email
  include_original_headers = true
}

resource "aws_ses_identity_notification_topic" "complaint" {
  count                    = var.enable_sns_notifications ? 1 : 0
  topic_arn                = aws_sns_topic.ses_notifications[0].arn
  notification_type        = "Complaint"
  identity                 = aws_ses_email_identity.sender.email
  include_original_headers = true
}




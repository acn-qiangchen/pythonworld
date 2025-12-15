/**
 * Terraform Variables for AWS SES Configuration
 */

variable "aws_region" {
  description = "AWS region for SES"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "email-api"
}

#############################################
# Email Configuration
#############################################

variable "sender_email" {
  description = "Email address to verify for sending (e.g., noreply@example.com)"
  type        = string
}

variable "allowed_sender_emails" {
  description = "List of email addresses allowed to send from"
  type        = list(string)
  default     = []
}

variable "domain_name" {
  description = "Domain name to verify (optional, leave empty to skip domain verification)"
  type        = string
  default     = ""
}

variable "route53_zone_id" {
  description = "Route53 hosted zone ID for DNS records (optional)"
  type        = string
  default     = ""
}

#############################################
# IAM Configuration
#############################################

variable "iam_user_name" {
  description = "Name for the IAM user that will send emails"
  type        = string
  default     = "SysSESAdmin"
}

#############################################
# Monitoring Configuration
#############################################

variable "enable_cloudwatch_events" {
  description = "Enable CloudWatch event destination for SES"
  type        = bool
  default     = true
}

variable "enable_cloudwatch_alarms" {
  description = "Enable CloudWatch alarms for bounce and complaint rates"
  type        = bool
  default     = true
}

variable "enable_sns_notifications" {
  description = "Enable SNS notifications for bounces and complaints"
  type        = bool
  default     = true
}

variable "notification_email" {
  description = "Email address to receive bounce/complaint notifications"
  type        = string
  default     = ""
}




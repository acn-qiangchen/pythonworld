/**
 * Terraform Outputs for AWS SES Configuration
 */

#############################################
# IAM User Outputs
#############################################

output "iam_user_name" {
  description = "Name of the IAM user created for SES"
  value       = aws_iam_user.ses_user.name
}

output "iam_user_arn" {
  description = "ARN of the IAM user"
  value       = aws_iam_user.ses_user.arn
}

output "aws_access_key_id" {
  description = "AWS Access Key ID for the IAM user (use for application)"
  value       = aws_iam_access_key.ses_user.id
  sensitive   = false
}

output "aws_secret_access_key" {
  description = "AWS Secret Access Key for the IAM user (SENSITIVE - store securely)"
  value       = aws_iam_access_key.ses_user.secret
  sensitive   = true
}

#############################################
# SES Configuration Outputs
#############################################

output "ses_email_identity" {
  description = "Verified email identity"
  value       = aws_ses_email_identity.sender.email
}

output "ses_email_identity_arn" {
  description = "ARN of the verified email identity"
  value       = aws_ses_email_identity.sender.arn
}

output "ses_domain_identity" {
  description = "Verified domain identity (if configured)"
  value       = var.domain_name != "" ? aws_ses_domain_identity.domain[0].domain : null
}

output "ses_domain_verification_token" {
  description = "Domain verification token (add to DNS as TXT record)"
  value       = var.domain_name != "" ? aws_ses_domain_identity.domain[0].verification_token : null
}

output "ses_dkim_tokens" {
  description = "DKIM tokens for domain (add to DNS as CNAME records)"
  value       = var.domain_name != "" ? aws_ses_domain_dkim.domain[0].dkim_tokens : []
}

output "ses_configuration_set_name" {
  description = "Name of the SES configuration set"
  value       = aws_ses_configuration_set.main.name
}

output "ses_configuration_set_arn" {
  description = "ARN of the SES configuration set"
  value       = aws_ses_configuration_set.main.arn
}

#############################################
# Region and Account Info
#############################################

output "aws_region" {
  description = "AWS region where SES is configured"
  value       = var.aws_region
}

output "aws_account_id" {
  description = "AWS account ID"
  value       = data.aws_caller_identity.current.account_id
}

#############################################
# SNS Topic Outputs
#############################################

output "sns_topic_arn" {
  description = "ARN of SNS topic for bounce/complaint notifications"
  value       = var.enable_sns_notifications ? aws_sns_topic.ses_notifications[0].arn : null
}

#############################################
# Environment Variables for Application
#############################################

output "env_variables" {
  description = "Environment variables to use in your application"
  value = {
    AWS_REGION            = var.aws_region
    AWS_ACCESS_KEY_ID     = aws_iam_access_key.ses_user.id
    AWS_SECRET_ACCESS_KEY = aws_iam_access_key.ses_user.secret
    DEFAULT_SENDER_EMAIL  = aws_ses_email_identity.sender.email
    SES_CONFIGURATION_SET = aws_ses_configuration_set.main.name
  }
  sensitive = true
}

#############################################
# Instructions
#############################################

output "next_steps" {
  description = "Next steps after applying Terraform"
  value       = <<-EOT
    
    ✅ SES Configuration Complete!
    
    Next Steps:
    
    1. VERIFY EMAIL:
       - Check your inbox (${var.sender_email})
       - Click the verification link from AWS
    
    2. REQUEST PRODUCTION ACCESS:
       - Go to AWS SES Console
       - Click "Account dashboard" → "Request production access"
       - Fill out the form explaining your use case
       - Wait for approval (usually 24-48 hours)
    
    3. UPDATE YOUR APPLICATION:
       - Use the credentials below in your .env file
       - AWS_ACCESS_KEY_ID: ${aws_iam_access_key.ses_user.id}
       - AWS_SECRET_ACCESS_KEY: (run 'terraform output aws_secret_access_key')
       - DEFAULT_SENDER_EMAIL: ${aws_ses_email_identity.sender.email}
    
    4. TEST YOUR SETUP:
       - While in sandbox mode, you can only send to verified addresses
       - After production access, you can send to any email
    
    5. MONITOR YOUR EMAILS:
       ${var.enable_sns_notifications ? "- Bounce/complaint notifications will be sent to: ${var.notification_email}" : "- Enable SNS notifications for bounce/complaint tracking"}
       ${var.enable_cloudwatch_alarms ? "- CloudWatch alarms are configured for high bounce/complaint rates" : ""}
    
    ${var.domain_name != "" ? "6. DNS CONFIGURATION (if using domain):\n       - Add the verification TXT record to your DNS\n       - Add the DKIM CNAME records to your DNS\n       - Run 'terraform output' to see the DNS records" : ""}
    
    For more information, see: README.md
    
  EOT
}




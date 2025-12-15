.PHONY: help init plan apply destroy output clean validate format

# Default target
help:
	@echo "Terraform SES - Available Commands"
	@echo "===================================="
	@echo "make init      - Initialize Terraform"
	@echo "make validate  - Validate configuration"
	@echo "make format    - Format Terraform files"
	@echo "make plan      - Preview changes"
	@echo "make apply     - Apply changes"
	@echo "make output    - Show outputs"
	@echo "make destroy   - Destroy all resources"
	@echo "make clean     - Clean Terraform files"
	@echo ""

# Initialize Terraform
init:
	@echo "Initializing Terraform..."
	terraform init
	@echo "✓ Initialization complete!"

# Validate configuration
validate:
	@echo "Validating Terraform configuration..."
	terraform validate
	@echo "✓ Configuration is valid!"

# Format Terraform files
format:
	@echo "Formatting Terraform files..."
	terraform fmt -recursive
	@echo "✓ Formatting complete!"

# Preview changes
plan:
	@echo "Planning Terraform changes..."
	terraform plan
	@echo ""
	@echo "Review the plan above before applying."

# Apply changes
apply:
	@echo "Applying Terraform configuration..."
	terraform apply
	@echo ""
	@echo "✓ Configuration applied!"
	@echo ""
	@echo "Next steps:"
	@terraform output next_steps

# Show outputs
output:
	@echo "Terraform Outputs:"
	@echo "=================="
	@terraform output

# Show specific outputs
output-keys:
	@echo "AWS Credentials:"
	@echo "================"
	@echo "AWS_ACCESS_KEY_ID=$(shell terraform output -raw aws_access_key_id)"
	@echo "AWS_SECRET_ACCESS_KEY=$(shell terraform output -raw aws_secret_access_key)"
	@echo "DEFAULT_SENDER_EMAIL=$(shell terraform output -raw ses_email_identity)"

# Destroy all resources
destroy:
	@echo "⚠️  WARNING: This will destroy all SES resources!"
	@echo ""
	terraform destroy

# Clean Terraform files
clean:
	@echo "Cleaning Terraform files..."
	rm -rf .terraform/
	rm -f .terraform.lock.hcl
	rm -f terraform.tfstate*
	@echo "✓ Cleanup complete!"




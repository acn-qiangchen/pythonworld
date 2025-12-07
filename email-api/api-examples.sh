#!/bin/bash
# API Examples - Sample curl commands for testing the Email API

# Configuration - Update these values
API_URL="http://localhost:8000"
FROM_EMAIL="verified-sender@yourdomain.com"  # Must be verified in AWS SES
TO_EMAIL="recipient@example.com"

echo "=========================================="
echo "Email API - Example Commands"
echo "=========================================="
echo ""

# 1. Health Check
echo "1. Health Check"
echo "Command:"
echo "curl -X GET \"${API_URL}/health\""
echo ""
echo "Response:"
curl -X GET "${API_URL}/health" 2>/dev/null | python -m json.tool
echo ""
echo "=========================================="
echo ""

# 2. Root Endpoint
echo "2. Root Endpoint"
echo "Command:"
echo "curl -X GET \"${API_URL}/\""
echo ""
echo "Response:"
curl -X GET "${API_URL}/" 2>/dev/null | python -m json.tool
echo ""
echo "=========================================="
echo ""

# 3. Send Email
echo "3. Send Email"
echo "Command:"
cat << EOF
curl -X POST "${API_URL}/api/v1/send-email" \\
  -H "Content-Type: application/json" \\
  -d '{
    "to_email": "${TO_EMAIL}",
    "subject": "Test Email from API",
    "body": "This is a test email sent via the Email API service.",
    "from_email": "${FROM_EMAIL}"
  }'
EOF
echo ""
echo ""

read -p "Do you want to send a test email? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Sending email..."
    echo "Response:"
    curl -X POST "${API_URL}/api/v1/send-email" \
      -H "Content-Type: application/json" \
      -d "{
        \"to_email\": \"${TO_EMAIL}\",
        \"subject\": \"Test Email from API\",
        \"body\": \"This is a test email sent via the Email API service using AWS SES. Sent at $(date)\",
        \"from_email\": \"${FROM_EMAIL}\"
      }" 2>/dev/null | python -m json.tool
    echo ""
else
    echo "Skipped sending email."
    echo ""
fi

echo "=========================================="
echo ""
echo "More Examples:"
echo ""
echo "# Send email with custom subject"
cat << 'EOF'
curl -X POST "http://localhost:8000/api/v1/send-email" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "user@example.com",
    "subject": "Welcome to our service!",
    "body": "Thank you for signing up. We are excited to have you!",
    "from_email": "noreply@yourdomain.com"
  }'
EOF
echo ""
echo ""

echo "# Send notification email"
cat << 'EOF'
curl -X POST "http://localhost:8000/api/v1/send-email" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "admin@example.com",
    "subject": "System Alert",
    "body": "This is an automated notification from your system.",
    "from_email": "alerts@yourdomain.com"
  }'
EOF
echo ""
echo ""

echo "=========================================="
echo "Interactive API Documentation:"
echo "  Swagger UI: ${API_URL}/docs"
echo "  ReDoc:      ${API_URL}/redoc"
echo "=========================================="


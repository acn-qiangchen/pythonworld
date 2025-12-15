#!/bin/bash
# API Examples - Sample curl commands for testing the Django Email API

# Configuration - Update these values
API_URL="http://localhost:8000/api"
FROM_EMAIL="verified-sender@yourdomain.com"  # Must be verified in AWS SES
TO_EMAIL="recipient@example.com"

echo "=========================================="
echo "Django Email API - Example Commands"
echo "=========================================="
echo ""

# 1. Service Info
echo "1. Service Information"
echo "Command:"
echo "curl -X GET \"${API_URL}/\""
echo ""
echo "Response:"
curl -X GET "${API_URL}/" 2>/dev/null | python -m json.tool
echo ""
echo "=========================================="
echo ""

# 2. Health Check
echo "2. Health Check"
echo "Command:"
echo "curl -X GET \"${API_URL}/health/\""
echo ""
echo "Response:"
curl -X GET "${API_URL}/health/" 2>/dev/null | python -m json.tool
echo ""
echo "=========================================="
echo ""

# 3. Send Email
echo "3. Send Email"
echo "Command:"
cat << EOF
curl -X POST "${API_URL}/v1/send-email/" \\
  -H "Content-Type: application/json" \\
  -d '{
    "to_email": "${TO_EMAIL}",
    "subject": "Test Email from Django API",
    "body": "This is a test email sent via the Django Email API service.",
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
    curl -X POST "${API_URL}/v1/send-email/" \
      -H "Content-Type: application/json" \
      -d "{
        \"to_email\": \"${TO_EMAIL}\",
        \"subject\": \"Test Email from Django API\",
        \"body\": \"This is a test email sent via the Django Email API service using AWS SES. Sent at $(date)\",
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
echo "# Send email with HTML body"
cat << 'EOF'
curl -X POST "http://localhost:8000/api/v1/send-email/" \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "user@example.com",
    "subject": "Welcome to our service!",
    "body": "Thank you for signing up.",
    "body_html": "<html><body><h1>Welcome!</h1><p>Thank you for signing up.</p></body></html>",
    "from_email": "noreply@yourdomain.com"
  }'
EOF
echo ""
echo ""

echo "# Send notification email"
cat << 'EOF'
curl -X POST "http://localhost:8000/api/v1/send-email/" \
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
echo "Browsable API Interface:"
echo "  API Root:    ${API_URL}/"
echo "  Send Email:  ${API_URL}/v1/send-email/"
echo "  Health:      ${API_URL}/health/"
echo ""
echo "Open these URLs in your browser to use the"
echo "interactive Django REST Framework interface!"
echo "=========================================="




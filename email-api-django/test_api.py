"""
Test script for Django Email API
Run this after starting the API server to test the endpoints
"""
import requests
import json

# API base URL
BASE_URL = "http://localhost:8000/api"

def test_root():
    """Test root endpoint"""
    print("\n=== Testing Root Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_health():
    """Test health check endpoint"""
    print("\n=== Testing Health Check Endpoint ===")
    response = requests.get(f"{BASE_URL}/health/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_send_email(to_email, from_email):
    """Test send email endpoint"""
    print("\n=== Testing Send Email Endpoint ===")
    
    payload = {
        "to_email": to_email,
        "subject": "Test Email from Django Email API",
        "body": "This is a test email sent via the Django Email API service using AWS SES.",
        "from_email": from_email
    }
    
    print(f"Sending email to: {to_email}")
    print(f"From: {from_email}")
    
    response = requests.post(f"{BASE_URL}/v1/send-email/", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200

def main():
    """Run all tests"""
    print("=" * 60)
    print("Django Email API Test Suite")
    print("=" * 60)
    
    try:
        # Test basic endpoints
        root_ok = test_root()
        health_ok = test_health()
        
        # Test email sending (update these with your verified emails)
        print("\n" + "=" * 60)
        print("To test email sending, update the email addresses below:")
        print("=" * 60)
        
        # IMPORTANT: Replace these with your verified SES email addresses
        TO_EMAIL = "recipient@example.com"  # Replace with recipient email
        FROM_EMAIL = "verified-sender@yourdomain.com"  # Replace with verified sender
        
        print(f"\nNote: Make sure '{FROM_EMAIL}' is verified in AWS SES")
        print(f"Note: If in SES sandbox mode, '{TO_EMAIL}' must also be verified")
        
        user_input = input("\nDo you want to test email sending? (yes/no): ").strip().lower()
        
        if user_input == 'yes':
            email_ok = test_send_email(TO_EMAIL, FROM_EMAIL)
        else:
            print("\nSkipping email send test.")
            email_ok = None
        
        # Summary
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        print(f"Root Endpoint: {'✓ PASS' if root_ok else '✗ FAIL'}")
        print(f"Health Check: {'✓ PASS' if health_ok else '✗ FAIL'}")
        if email_ok is not None:
            print(f"Send Email: {'✓ PASS' if email_ok else '✗ FAIL'}")
        else:
            print(f"Send Email: SKIPPED")
        print("=" * 60)
        print("\nTip: You can also test the API using the browsable interface:")
        print(f"  - {BASE_URL}/")
        print(f"  - {BASE_URL}/v1/send-email/")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to API server")
        print("Make sure the API server is running on http://localhost:8000")
        print("\nTo start the server, run:")
        print("  docker-compose up -d")
        print("  OR")
        print("  make run")
        print("  OR")
        print("  python manage.py runserver")
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")

if __name__ == "__main__":
    main()




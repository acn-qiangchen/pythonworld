"""
Serializers for Email API
"""
from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    """Serializer for email sending request"""
    to_email = serializers.EmailField(
        required=True,
        help_text="Recipient email address"
    )
    subject = serializers.CharField(
        required=True,
        max_length=200,
        help_text="Email subject"
    )
    body = serializers.CharField(
        required=True,
        help_text="Email body content (plain text)"
    )
    from_email = serializers.EmailField(
        required=False,
        allow_null=True,
        help_text="Sender email address (must be verified in SES)"
    )
    body_html = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text="Optional HTML version of email body"
    )
    
    def validate_subject(self, value):
        """Validate subject is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Subject cannot be empty")
        return value
    
    def validate_body(self, value):
        """Validate body is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Body cannot be empty")
        return value


class EmailResponseSerializer(serializers.Serializer):
    """Serializer for email sending response"""
    success = serializers.BooleanField()
    message = serializers.CharField()
    message_id = serializers.CharField(required=False, allow_null=True)


class HealthCheckSerializer(serializers.Serializer):
    """Serializer for health check response"""
    status = serializers.CharField()
    service = serializers.CharField()
    ses_connection = serializers.CharField()
    statistics = serializers.DictField(required=False)


class ServiceInfoSerializer(serializers.Serializer):
    """Serializer for service information"""
    service = serializers.CharField()
    version = serializers.CharField()
    status = serializers.CharField()
    framework = serializers.CharField()




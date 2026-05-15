"""
Validation Service - Form validation logic
Handles validation for case registration and updates
"""

from typing import Tuple, Dict, Any


class ValidationService:
    """Service for form validation"""
    
    @staticmethod
    def validate_case_registration(
        name: str,
        complainant_name: str,
        complainant_mobile: str,
        city: str,
        last_seen: str
    ) -> Tuple[bool, str]:
        """
        Validate case registration form
        
        Args:
            name: Person's name
            complainant_name: Complainant's name
            complainant_mobile: Complainant's mobile number
            city: City
            last_seen: Last seen location/date
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not name or not complainant_name or not complainant_mobile or not city or not last_seen:
            return False, "❌ Please fill in all required fields marked with *"
        
        if len(complainant_mobile) != 10 or not complainant_mobile.isdigit():
            return False, "❌ Mobile number must be exactly 10 digits"
        
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Validate email format
        
        Args:
            email: Email address
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email:
            return False, "❌ Please provide an email address"
        
        if "@" not in email or "." not in email:
            return False, "❌ Please provide a valid email address"
        
        return True, ""
    
    @staticmethod
    def validate_mobile_number(mobile: str) -> Tuple[bool, str]:
        """
        Validate mobile number
        
        Args:
            mobile: Mobile number
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not mobile:
            return False, "❌ Please provide a mobile number"
        
        if len(mobile) != 10:
            return False, "❌ Mobile number must be exactly 10 digits"
        
        if not mobile.isdigit():
            return False, "❌ Mobile number must contain only digits"
        
        return True, ""
    
    @staticmethod
    def validate_case_update(
        name: str,
        complainant_name: str,
        complainant_mobile: str,
        city: str,
        last_seen: str
    ) -> Tuple[bool, str]:
        """
        Validate case update form (same as registration)
        
        Args:
            name: Person's name
            complainant_name: Complainant's name
            complainant_mobile: Complainant's mobile number
            city: City
            last_seen: Last seen location/date
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        return ValidationService.validate_case_registration(
            name, complainant_name, complainant_mobile, city, last_seen
        )
    
    @staticmethod
    def validate_message_form(
        recipient_email: str,
        subject: str,
        message_body: str
    ) -> Tuple[bool, str]:
        """
        Validate message/email form
        
        Args:
            recipient_email: Recipient's email
            subject: Email subject
            message_body: Email body
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        email_valid, email_error = ValidationService.validate_email(recipient_email)
        if not email_valid:
            return False, email_error
        
        if not subject or not subject.strip():
            return False, "❌ Please provide an email subject"
        
        if not message_body or not message_body.strip():
            return False, "❌ Message body cannot be empty"
        
        return True, ""


# Global instance
validation_service = ValidationService()

"""
Email Validation Module
Validates email addresses to prevent fake/disposable emails
"""

import re
import dns.resolver
from typing import Tuple

class EmailValidator:
    """Validate email addresses for authenticity"""
    
    # Common disposable email domains
    DISPOSABLE_DOMAINS = [
        'tempmail.com', 'throwaway.email', '10minutemail.com', 'guerrillamail.com',
        'mailinator.com', 'maildrop.cc', 'temp-mail.org', 'getnada.com',
        'trashmail.com', 'fakeinbox.com', 'yopmail.com', 'sharklasers.com',
        'guerrillamail.info', 'grr.la', 'guerrillamail.biz', 'guerrillamail.de',
        'spam4.me', 'tmpeml.info', 'emailondeck.com', 'mintemail.com'
    ]
    
    @staticmethod
    def validate_email_format(email: str) -> Tuple[bool, str]:
        """
        Validate email format using regex
        Returns: (is_valid, message)
        """
        if not email:
            return False, "Email is required"
        
        # Basic format check
        if "@" not in email or "." not in email:
            return False, "Invalid email format"
        
        # Regex pattern for email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            return False, "Invalid email format"
        
        return True, "Valid format"
    
    @staticmethod
    def check_disposable_email(email: str) -> Tuple[bool, str]:
        """
        Check if email is from a disposable/temporary email service
        Returns: (is_disposable, message)
        """
        try:
            domain = email.split('@')[1].lower()
            
            if domain in EmailValidator.DISPOSABLE_DOMAINS:
                return True, f"Disposable email domain '{domain}' is not allowed"
            
            return False, "Valid domain"
        
        except Exception:
            return False, "Could not check domain"
    
    @staticmethod
    def verify_domain_exists(email: str) -> Tuple[bool, str]:
        """
        Verify that the email domain has valid MX records
        Returns: (exists, message)
        """
        try:
            domain = email.split('@')[1]
            
            # Check for MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                if mx_records:
                    return True, "Domain has valid mail server"
            except dns.resolver.NoAnswer:
                pass
            except dns.resolver.NXDOMAIN:
                return False, f"Domain '{domain}' does not exist"
            
            # Fallback: Check for A record
            try:
                a_records = dns.resolver.resolve(domain, 'A')
                if a_records:
                    return True, "Domain exists"
            except:
                return False, f"Domain '{domain}' does not exist"
            
            return False, f"Domain '{domain}' has no mail server"
        
        except Exception as e:
            # If DNS check fails, allow it (don't block legitimate emails)
            return True, "Could not verify domain (allowed)"
    
    @staticmethod
    def validate_email(email: str, check_domain: bool = True) -> Tuple[bool, str]:
        """
        Complete email validation
        Returns: (is_valid, message)
        """
        # 1. Format validation
        is_valid, message = EmailValidator.validate_email_format(email)
        if not is_valid:
            return False, message
        
        # 2. Check for disposable email
        is_disposable, message = EmailValidator.check_disposable_email(email)
        if is_disposable:
            return False, message
        
        # 3. Verify domain exists (optional)
        if check_domain:
            domain_exists, message = EmailValidator.verify_domain_exists(email)
            if not domain_exists:
                return False, message
        
        return True, "Email is valid"
    
    @staticmethod
    def is_common_provider(email: str) -> bool:
        """Check if email is from a common trusted provider"""
        common_providers = [
            'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com',
            'icloud.com', 'protonmail.com', 'aol.com', 'mail.com',
            'zoho.com', 'gmx.com', 'yandex.com', 'live.com',
            'msn.com', 'inbox.com', 'fastmail.com'
        ]
        
        try:
            domain = email.split('@')[1].lower()
            return domain in common_providers
        except:
            return False

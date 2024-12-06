from rest_framework import status
from rest_framework.exceptions import APIException
from account.models import Role,OtpVerify
from django.core.mail import EmailMessage
from django.conf import settings
import random
import string


def generate_otp():
    # Generate a random 5-digit number
    return ''.join(random.choices(string.digits, k=6))    



def create_roles():
    # List of roles to be created
    roles = ['Standard User', 'viewer' , "Admin"]

    # Create roles if they do not already exist
    for role in roles:
        Role.objects.get_or_create(name=role)
        
        
def send_otp(email: str, body_type: str) -> bool:
    
    otp = generate_otp()
    otp_obj = OtpVerify(email=email, otp=otp)
    otp_obj.save()
    email_body = f"{body_type} {otp}"
    data = {
        "email_body": email_body,
        "to_email": email,
        "email_subject": "Your OTP Verification Code"
    }
    email=EmailMessage(subject=data['email_subject'], body=data['email_body'],from_email=settings.EMAIL_HOST_USER, to=[data['to_email']])
    email.send()

    return True
import pyotp
from django.core.cache import cache
from django.conf import settings
import logging
import requests


class OTPService:
    def __init__(self, phone_number=None):
        self.phone_number = phone_number
        self.otp_key = f"otp_{phone_number}"
        self.base32_key = f"base32_{phone_number}"  # Consistent base32 key

    def generate_otp(self):
        # Check if base32 key exists in cache, otherwise create it
        base32_key = cache.get(self.base32_key)
        if not base32_key:
            base32_key = pyotp.random_base32()
            cache.set(self.base32_key, base32_key, timeout=None)  # No expiry for base32 key
            logging.debug(f"Base32 key created for {self.phone_number}: {base32_key}")
        else:
            logging.debug(f"Base32 key retrieved for {self.phone_number}: {base32_key}")

        # Generate OTP
        otp = pyotp.TOTP(base32_key).now()
        cache.set(self.otp_key, otp, timeout=settings.CACHE_TTL)
        logging.debug(f"Generated OTP for {self.phone_number}: {otp}")
        return otp

    def send_otp_sms(self, phone_number):
        otp = self.generate_otp()
        url = "https://api.sms.ir/v1/send/verify"
        headers = {
            "x-api-key": "cwSvgHmGQsyQxbI4dOWxRQaAuIRT1k9Q49QrCBvpR9BOymXAKvjCC57fOaoM34AV",
            'ACCEPT': 'application/json',
            'Content-Type': 'application/json'
        }
        payload = {
            "mobile": phone_number,
            "templateId": 100000,
            "parameters": [{"name": "CODE", "value": otp}]
        }
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        if response_data.get('status') != 1:
            logging.error(f"Failed to send OTP via SMS: {response_data}")
            raise Exception("Failed to send OTP via SMS")
        logging.debug(f"OTP sent successfully to {phone_number}")
        return response_data

    def verify_otp(self, otp):
        stored_otp = cache.get(self.otp_key)
        logging.debug(f"Stored OTP for {self.phone_number}: {stored_otp}, Provided OTP: {otp}")
        if stored_otp and stored_otp == otp:
            cache.delete(self.otp_key)
            logging.debug(f"OTP verified successfully for {self.phone_number}")
            return True
        logging.error(f"OTP verification failed for {self.phone_number}")
        return False

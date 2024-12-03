# hmac_generator.py
import hmac
import hashlib

def generate_hmac(challenge: str, application_management_token: str) -> str:
    key = application_management_token.encode('utf-8')
    message = challenge.encode('utf-8')
    return hmac.new(key, message, hashlib.sha256).hexdigest()

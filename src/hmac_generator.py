# src/hmac_generator.py
import hmac
import hashlib

# Funktion som skapar en HMAC (Hash-based Message Authentication Code) 
def generate_hmac(challenge: str, application_management_token: str) -> str:
    # Konverterar application_management_token till en bytes-sträng (utf-8 kodning)
    key = application_management_token.encode('utf-8')
    # Konverterar challenge till en bytes-sträng (utf-8 kodning)
    message = challenge.encode('utf-8')
    # Skapar en HMAC med hjälp av SHA-256, en hexadecimal sträng
    return hmac.new(key, message, hashlib.sha256).hexdigest()
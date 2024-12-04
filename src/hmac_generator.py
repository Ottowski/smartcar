# src/hmac_generator.py
import hmac
import hashlib

def generate_hmac(challenge: str, application_management_token: str) -> str:
    key = application_management_token.encode('utf-8')
    message = challenge.encode('utf-8')
    
    return hmac.new(key, message, hashlib.sha256).hexdigest()

def test_generate_hmac():
    challenge = "test_challenge"
    token = "test_token"
    expected_hmac = "08bffc15e99c2c42c6556480fc807e5698aad5d80a95e1181a7b05d8208d6c44"
    
    result = generate_hmac(challenge, token)
    
    print(f"Calculated HMAC: {result}")
    print(f"Expected HMAC: {expected_hmac}")
    
    assert result == expected_hmac, f"Förväntat {expected_hmac}, men fick {result}"

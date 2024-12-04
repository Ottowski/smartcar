# tests/test_hmac_generator.py
import pytest
from src.hmac_generator import generate_hmac

@pytest.mark.parametrize("challenge, token, expected_hmac", [
    ("test_challenge", "test_token", "08bffc15e99c2c42c6556480fc807e5698aad5d80a95e1181a7b05d8208d6c44")
])
def test_generate_hmac(challenge, token, expected_hmac):
    # Anropa funktionen
    result = generate_hmac(challenge, token)
    
    # Skriv ut resultatet för att hjälpa till med felsökning
    print(f"Resultat: {result}")
    
    # Jämför det faktiska resultatet med det förväntade värdet
    assert result == expected_hmac, f"Förväntat {expected_hmac}, men fick {result}"

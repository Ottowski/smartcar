# tests/test_cache_handler.py
# Testar att MockDatabase returnerar korrekt device_id och shard.
import pytest
from src.cache_handler import MockDatabase

@pytest.mark.asyncio
async def test_get_internal_info():
    mock_db = MockDatabase() 
    result = await mock_db.get_internal_info("00000000-0000-4000-A000-000000000001")  
    # Kontrollerar att resultatet har rätt device_id och shard
    assert result["device_id"] == "aaabe4a9-6d0c-47ef-b944-e91dc2c5a111"
    assert result["shard"] == 1
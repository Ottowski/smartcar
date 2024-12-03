# tests/test_connection_manager.py
import pytest
from src.connection_manager import ConnectionManager

@pytest.mark.asyncio
async def test_send_message(monkeypatch):
    async def mock_send_message(self, shard, public_id, source, sample):
        return {"status": "sent"}
    
    monkeypatch.setattr(ConnectionManager, "send_message", mock_send_message)

    connection_manager = ConnectionManager()
    result = await connection_manager.send_message(
        shard=1,
        public_id="test-device",
        source="smartcar",
        sample={"data": "sample"}
    )
    assert result["status"] == "sent"


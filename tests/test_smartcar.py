# tests/test_smartcar.py
import pytest
from unittest.mock import AsyncMock
from src.mock_db import MockDB
from src.connection_manager import ConnectionManager
from src.smartcar import init_smartcar_router

@pytest.mark.asyncio
async def test_sample():
    # Mocka MockDB och metoden get_internal_info
    mock_db = MockDB()
    mock_db.get_internal_info = AsyncMock(side_effect=[
        {"shard": 1, "device_id": "aaabe4a9-6d0c-47ef-b944-e91dc2c5a111"},
        {"shard": 1, "device_id": "bbbbe4a9-6d0c-47ef-b944-e91dc2c5a222"},
    ])

    # Mocka ConnectionManager och metoden send_message
    connection_manager = ConnectionManager()
    connection_manager.send_message = AsyncMock()

    # Initiera smartcar-router
    smartcar_router = init_smartcar_router(mock_db, connection_manager, None)

    # Exempel på webhook-payload
    payload = {
        "devices": [
            {"vehicleId": "00000000-0000-4000-A000-000000000001", "data": {"key": "value1"}},
            {"vehicleId": "00000000-0000-4000-A000-000000000002", "data": {"key": "value2"}}
        ]
    }

    # Hämta sample-funktionen
    sample_func = smartcar_router["sample_func"]

    # Kör funktionen och verifiera
    result = await sample_func(payload)

    # Verifiera resultatets innehåll
    assert len(result["samples"]) == 2
    assert result["samples"][0] == {
        "device_id": "aaabe4a9-6d0c-47ef-b944-e91dc2c5a111",
        "shard": 1,
        "data": {"key": "value1"}
    }
    assert result["samples"][1] == {
        "device_id": "bbbbe4a9-6d0c-47ef-b944-e91dc2c5a222",
        "shard": 1,
        "data": {"key": "value2"}
    }

    # Kontrollera att send_message har kallats korrekt
    connection_manager.send_message.assert_any_call(
        shard=1,
        public_id="aaabe4a9-6d0c-47ef-b944-e91dc2c5a111",
        source="smartcar",
        sample={
            "device_id": "aaabe4a9-6d0c-47ef-b944-e91dc2c5a111",
            "shard": 1,
            "data": {"key": "value1"}
        }
    )
    connection_manager.send_message.assert_any_call(
        shard=1,
        public_id="bbbbe4a9-6d0c-47ef-b944-e91dc2c5a222",
        source="smartcar",
        sample={
            "device_id": "bbbbe4a9-6d0c-47ef-b944-e91dc2c5a222",
            "shard": 1,
            "data": {"key": "value2"}
        }
    )

    # Kontrollera att send_message kallats två gånger
    assert connection_manager.send_message.call_count == 2

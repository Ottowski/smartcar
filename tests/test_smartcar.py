# test_smartcar.py
import pytest
from src.mock_db import MockDB
from src.connection_manager import ConnectionManager
from src.smartcar import init_smartcar_router

@pytest.mark.asyncio
async def test_sample():
    # Mocka vår proxy_db (mock_db)
    mock_db = MockDB()

    # Skapa en mock av ConnectionManager
    connection_manager = ConnectionManager()

    # Initiera smartcar-router
    smartcar_router = init_smartcar_router(mock_db, connection_manager, None)

    # Exempel på webhook-payload
    payload = {
        "devices": [
            {"vehicleId": "00000000-0000-4000-A000-000000000001", "data": "sample_data_1"},
            {"vehicleId": "00000000-0000-4000-A000-000000000002", "data": "sample_data_2"}
        ]
    }

    # Hämta sample-funktionen
    sample_func = smartcar_router["sample_func"]

    # Kör funktionen och verifiera
    result = await sample_func(payload)
    
    assert len(result["samples"]) == 2
    assert result["samples"][0]["device_id"] == "aaabe4a9-6d0c-47ef-b944-e91dc2c5a111"
    assert result["samples"][1]["device_id"] == "bbbbe4a9-6d0c-47ef-b944-e91dc2c5a222"
    assert result["samples"][0]["shard"] == 1
    assert result["samples"][1]["shard"] == 1


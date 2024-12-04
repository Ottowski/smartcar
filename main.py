# main.py

from src.mock_db import MockDB
from src.connection_manager import ConnectionManager
from src.smartcar import init_smartcar_router

async def main():
    mock_db = MockDB()
    connection_manager = ConnectionManager()

    router = await init_smartcar_router(mock_db, connection_manager, None)
    sample_func = router["sample_func"]

    payload = {
        "vehicles": [
            {"vehicleId": "00000000-0000-4000-A000-000000000001", "data": {"speed": 100}},
            {"vehicleId": "00000000-0000-4000-A000-000000000002", "data": {"speed": 120}},
            {"vehicleId": "00000000-0000-4000-A000-000000000003", "data": {"speed": 140}},
        ]
    }

    result = await sample_func(payload)
    print(result)

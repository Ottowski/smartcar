# src/smartcar.py
import json
import os
from typing import Callable
from src.mock_db import MockDB
from src.connection_manager import ConnectionManager

class SmartCarWebhook:
    def __init__(self, mock_db: MockDB, connection_manager: ConnectionManager, generate_verification: Callable):
        self.mock_db = mock_db
        self.connection_manager = connection_manager
        self.generate_verification = generate_verification

    async def sample(self, payload: dict):
        samples = []

        # Läs in data från vehicle_data.json som ligger i 'data' mappen
        file_path = os.path.join('data', 'vehicle_data.json')
        with open(file_path, 'r') as file:
            vehicle_data = json.load(file)

        # Loopar genom varje enhet i payload
        for device in payload['devices']:
            device_reference = device['vehicleId']
            # Hämta intern information från mock_db
            internal_data = await self.mock_db.get_internal_info(device_reference)

            shard_number = internal_data.get('shard')
            device_id = internal_data.get('device_id')

            # Bygg EDAP-sample med data från vehicle_data.json
            edap_sample = {
                "device_id": device_id,
                "shard": shard_number,
                "edap": {
                    "energy": vehicle_data.get("energy"),
                    "power": vehicle_data.get("power"),
                    "time": vehicle_data.get("time"),
                    "sensors": vehicle_data.get("sensors", {})
                }
            }
            samples.append(edap_sample)

            # Skicka meddelande via connection_manager
            await self.connection_manager.send_message(
                shard=shard_number,
                public_id=device_id,
                source="smartcar",
                sample=edap_sample
            )

        return {"samples": samples}

# Skapa en instans av SmartCarWebhook och returnera den för användning i testet
def init_smartcar_router(mock_db: MockDB, connection_manager: ConnectionManager, generate_verification: Callable):
    smartcar_webhook = SmartCarWebhook(mock_db, connection_manager, generate_verification)
    return {"sample_func": smartcar_webhook.sample}

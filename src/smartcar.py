# smartcar.py
import json
from typing import Callable
from src.mock_db import MockDB  # Antag att mock_db är en modul som importeras
from src.connection_manager import ConnectionManager  # Importera ConnectionManager-klassen

class SmartCarWebhook:
    def __init__(self, mock_db: MockDB, connection_manager: ConnectionManager, generate_verification: Callable):
        self.mock_db = mock_db
        self.connection_manager = connection_manager
        self.generate_verification = generate_verification

    async def sample(self, payload: dict):
        samples = []

        # Loopar genom varje enhet i payload
        for device in payload['devices']:
            device_reference = device['vehicleId']
            # Hämta intern information från mock_db istället för proxy_db
            internal_data = await self.mock_db.get_internal_info(device_reference)

            shard_number = internal_data.get('shard')
            device_id = internal_data.get('device_id')

            # Skapa EDAP-sample för varje enhet
            edap_sample = {
                "device_id": device_id,
                "shard": shard_number,
                "data": device['data']  # Exempel på data i payload
            }
            samples.append(edap_sample)

            # Skicka message via connection_manager
            await self.connection_manager.send_message(
                shard=shard_number,
                public_id=device_id,
                source="smartcar",
                sample=edap_sample
            )

        return {"samples": samples}

def init_smartcar_router(mock_db: MockDB, connection_manager: ConnectionManager, generate_verification: Callable):
    # Skapa en instans av SmartCarWebhook med rätt parametrar
    smartcar_webhook = SmartCarWebhook(mock_db, connection_manager, generate_verification)

    # Returnera en dictionary med referens till sample-metoden
    return {
        "sample_func": smartcar_webhook.sample
    }

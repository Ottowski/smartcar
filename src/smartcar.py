# src/smartcar.py
import json
from typing import Callable, Dict, Any
from src.mock_db import MockDB  # Antag att mock_db är en modul som importeras
from src.connection_manager import ConnectionManager  # Importera ConnectionManager-klassen

class SmartCarWebhook:
    def __init__(self, mock_db: MockDB, connection_manager: ConnectionManager, generate_verification: Callable):
        self.mock_db = mock_db
        self.connection_manager = connection_manager
        self.generate_verification = generate_verification

    async def sample(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hanterar inkommande payload för att generera EDAP-samples och skickar data via connection_manager.

        Args:
            payload (Dict[str, Any]): Innehåller information om enheter och deras data.

        Returns:
            Dict[str, Any]: En samling av genererade EDAP-samples.
        """
        samples = []

        # Kontrollera om payload innehåller förväntade nycklar
        if 'devices' not in payload:
            raise ValueError("Payload saknar nyckeln 'devices'.")

        # Loopar genom varje enhet i payload
        for device in payload['devices']:
            device_reference = device.get('vehicleId')
            if not device_reference:
                raise ValueError("Device saknar 'vehicleId'.")

            # Hämta intern information från mock_db istället för proxy_db
            internal_data = await self.mock_db.get_internal_info(device_reference)

            shard_number = internal_data.get('shard')
            device_id = internal_data.get('device_id')

            if shard_number is None or device_id is None:
                raise ValueError(f"Ingen giltig intern data hittades för device_reference: {device_reference}")

            # Skapa EDAP-sample för varje enhet
            edap_sample = {
                "device_id": device_id,
                "shard": shard_number,
                "data": device.get('data', {})  # Använd tom dictionary som standard om 'data' saknas
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

def init_smartcar_router(mock_db: MockDB, connection_manager: ConnectionManager, generate_verification: Callable) -> Dict[str, Callable]:
    """
    Initialiserar och returnerar en router för SmartCar-webhook.

    Args:
        mock_db (MockDB): Databasanvändare.
        connection_manager (ConnectionManager): Hanterare för meddelandesändning.
        generate_verification (Callable): Funktion för att generera verifieringar.

    Returns:
        Dict[str, Callable]: Referens till metoden för att hantera inkommande samples.
    """
    # Skapa en instans av SmartCarWebhook med rätt parametrar
    smartcar_webhook = SmartCarWebhook(mock_db, connection_manager, generate_verification)

    # Returnera en dictionary med referens till sample-metoden
    return {
        "sample_func": smartcar_webhook.sample
    }

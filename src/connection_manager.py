# src/connection_manager.py
class ConnectionManager:
    async def send_message(self, shard: int, public_id: str, source: str, sample: dict):
        # Skickar ett meddelande, eller skriva logik för att skicka det via Webhook
        print(f"Sending message to shard {shard} for device {public_id} with data: {sample}")


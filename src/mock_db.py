# src/mock_db.py
class MockDB:
    # Här kan vi definiera en enkel mock för att simulera databasfunktionalitet
    @staticmethod
    async def get_internal_info(device_reference: str):
        # Exempel på hur data kan returneras baserat på device_reference
        device_mapping = {
            "00000000-0000-4000-A000-000000000001": {"shard": 1, "device_id": "aaabe4a9-6d0c-47ef-b944-e91dc2c5a111"},
            "00000000-0000-4000-A000-000000000002": {"shard": 1, "device_id": "bbbbe4a9-6d0c-47ef-b944-e91dc2c5a222"},
            "00000000-0000-4000-A000-000000000003": {"shard": 2, "device_id": "cccbe4a9-6d0c-47ef-b944-e91dc2c5a333"}
        }
        return device_mapping.get(device_reference, {"shard": 0, "device_id": None})

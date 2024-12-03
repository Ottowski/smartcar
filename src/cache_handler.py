# src/cache_handler.py
class MockDatabase:
    def __init__(self):
        # Mockad data
        self.data = {
            "00000000-0000-4000-A000-000000000001": {
                "device_id": "aaabe4a9-6d0c-47ef-b944-e91dc2c5a111",
                "shard": 1,
            },
            "00000000-0000-4000-A000-000000000002": {
                "device_id": "bbbbe4a9-6d0c-47ef-b944-e91dc2c5a222",
                "shard": 1,
            },
            "00000000-0000-4000-A000-000000000003": {
                "device_id": "cccbe4a9-6d0c-47ef-b944-e91dc2c5a333",
                "shard": 2,
            },
        }

    async def get_internal_info(self, reference: str):
        """
        Mock function to mimic a database call.
        Returns a dictionary with `device_id` and `shard` for a given reference.
        """
        return self.data.get(reference)

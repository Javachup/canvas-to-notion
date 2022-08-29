from Notion.Client import Client

class NotionObject:
    def __init__(self, client: Client, data) -> None:
        self._client = client
        self.data = data

    def __str__(self) -> str:
        return str(self.data)
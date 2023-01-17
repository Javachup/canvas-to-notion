import requests
from Notion.Property import Property
from Notion.NotionExceptions import DatabaseQueryError

class Client:
    def __init__(self, secretToken: str, notionVersion: str = "2022-06-28") -> None:
        self._token = secretToken
        self._headers = {"Authorization": f"Bearer {self._token}", "Notion-Version": f"{notionVersion}"}

    def get_page(self, pageID: str):
        from Notion.Page import Page
        url = f"https://api.notion.com/v1/pages/{pageID}"

        r = requests.get(url, headers=self._headers)
        if not r.ok: raise DatabaseQueryError(r)
        return Page(self, r.json())

    def get_property(self, pageID: str, propertyID: str):
        url = f"https://api.notion.com/v1/pages/{pageID}/properties/{propertyID}"

        r = requests.get(url, headers=self._headers)
        if not r.ok: raise DatabaseQueryError(r)
        return r.json()

    def append_to_database(self, parentDatabaseID: str, properties: list[Property]):
        url = "https://api.notion.com/v1/pages/"

        data = Property.create_page_data(properties, parentDatabaseID)

        r = requests.post(url, headers=self._headers, json=data)
        if not r.ok: raise DatabaseQueryError(r)
        return r.json()

    def update_page(self, pageID: str, newProperties: list[Property]):
        url = f"https://api.notion.com/v1/pages/{pageID}"

        data = Property.create_page_data(newProperties)

        r = requests.patch(url, headers=self._headers, json=data)
        if not r.ok: raise DatabaseQueryError(r)
        return r.json()

    def get_database(self, databaseID: str):
        url = f"https://api.notion.com/v1/databases/{databaseID}"

        r = requests.get(url, headers=self._headers)
        if not r.ok: raise DatabaseQueryError(r)
        return r.json()

    def query_database(self, databaseID: str, pageSize: int = 100, startCursor: str = None):
        url = f"https://api.notion.com/v1/databases/{databaseID}/query"

        data = {}
        data['page_size'] = pageSize
        if startCursor: data['start_cursor'] = startCursor

        r = requests.post(url, headers=self._headers, json=data)
        if not r.ok: raise DatabaseQueryError(r)
        return r.json()
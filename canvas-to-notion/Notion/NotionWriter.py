from Notion.Client import Client
from Notion.Page import Page
from Notion.Property import Property

TOKEN = 'secret_Sxk4xNWhqQ4ItUSQ9XZ5Sp9q2LlH5te1Tu13OMEIiWt'
DATABASE_ID = 'f3e79eb9754f4d10b79651dd4d1cfe44'

class NotionWriter:
    def __init__(self, token: str, databaseID: str) -> None:
        self._client = Client(token)
        self._databaseID = databaseID
        self.pages = None

    def update_or_append(self, title: str, properties: list[Property]):
        if self.pages == None: self.cache_pages()

        # Look up the title property in hash table 
        if title in self.pages:
            self.pages[title].update(properties)
        else:
            self._client.append_to_database(self._databaseID, properties)

    def _get_all_pages(self) -> list[Page]:
        pages = []

        counter = 0
        startCursor = None
        while True:
            data = self._client.query_database(self._databaseID, startCursor=startCursor)

            for p in data['results']:
                pages.append(Page(self._client, p))

            if not data['has_more']:
                break

            startCursor = data['next_cursor']

            counter += 1
            if (counter > 100):
                raise Exception("Too many loops!")

        return pages

    def cache_pages(self):
        self.pages = self._get_pages_with_names()

    def _get_pages_with_names(self) -> dict[str, Page]:
        result = {}

        pages = self._get_all_pages()

        for p in pages:
            result[p.get_title()] = p

        return result